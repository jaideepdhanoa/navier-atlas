/* Network Shift — Tasklet reference implementation (verbatim drawing).
 * Source: docs/invest/reference-impl/network-shift.html (PR #387 d59f244)
 * DO NOT redesign geometry. Site binds scroll via window.setNetworkMix(m).
 */
(function (global) {
  'use strict';

  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }

  /**
   * Mount Network Shift into `root` (element that will contain canvas + HUD).
   * Drawing code ported from reference-impl — geometry unchanged.
   */
  function initNetworkShift(root, opts) {
    opts = opts || {};
    const chips = opts.chips || {};
    // Build structure
    root.innerHTML = '';
    root.classList.add('ns-root');
    const stage = document.createElement('div');
    stage.className = 'ns-canvas-stage';
    stage.id = 'ns-stage';
    const cv = document.createElement('canvas');
    cv.id = 'ns-canvas';
    stage.appendChild(cv);
    root.appendChild(stage);

    const hud = document.createElement('div');
    hud.className = 'ns-hud';
    hud.innerHTML = `
      <div class="ns-chip today" id="ns-chipA">
        <div class="k">${esc(chips.aLabel || 'Shipping today')}</div>
        <div class="h">${esc(chips.aLine || '')}</div>
        <div class="s">${esc(chips.aStats || '')}</div>
      </div>
      <div class="ns-toggles">
        <button type="button" id="ns-btnA" class="on-a">${esc(chips.aLabel || 'Shipping today')}</button>
        <button type="button" id="ns-btnB">${esc(chips.bLabel || 'The Navier network')}</button>
      </div>
      <div class="ns-chip network" id="ns-chipB" style="opacity:.25">
        <div class="k">${esc(chips.bLabel || 'The Navier network')}</div>
        <div class="h">${esc(chips.bLine || '')}</div>
        <div class="s">${esc(chips.bStats || '')}</div>
      </div>`;
    root.appendChild(hud);

    function esc(s) {
      return String(s == null ? '' : s)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    const ctx = cv.getContext('2d');
    let W = 0, H = 0, DPR = 1;
    let seed = 7;
    function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }

    let coastPts = [], islands = [], harbors = [], megaports = [], trunk = [], arcs = [], vessels = [], ships = [];
    function smooth(pts, n) {
      const out = [];
      for (let i = 0; i < n; i++) {
        const t = (i / (n - 1)) * (pts.length - 1);
        const k = Math.min(Math.floor(t), pts.length - 2), f = t - k;
        const p0 = pts[Math.max(k - 1, 0)], p1 = pts[k], p2 = pts[k + 1], p3 = pts[Math.min(k + 2, pts.length - 1)];
        out.push([
          0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * f + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * f * f + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * f * f * f),
          0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * f + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * f * f + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * f * f * f),
        ]);
      }
      return out;
    }

    function buildWorld() {
      seed = 7; harbors = []; islands = []; arcs = []; vessels = []; ships = [];
      const y = (f) => H * f, x = (f) => W * f;
      const ctrl = [
        [x(-0.05), y(0.2)], [x(0.07), y(0.26)], [x(0.16), y(0.22)], [x(0.28), y(0.3)],
        [x(0.36), y(0.21)], [x(0.5), y(0.27)], [x(0.58), y(0.33)], [x(0.7), y(0.24)],
        [x(0.83), y(0.29)], [x(0.93), y(0.22)], [x(1.05), y(0.27)],
      ];
      coastPts = smooth(ctrl, 240);
      islands = [
        [x(0.17), y(0.58), W * 0.042, H * 0.032, 0.3],
        [x(0.42), y(0.68), W * 0.055, H * 0.042, -0.2],
        [x(0.57), y(0.52), W * 0.028, H * 0.024, 0.6],
        [x(0.72), y(0.63), W * 0.034, H * 0.028, 0.8],
        [x(0.88), y(0.55), W * 0.046, H * 0.036, 0.1],
      ];
      megaports = [coastPts[36], coastPts[196]];
      trunk = [megaports[0], [x(0.3), y(0.4)], [x(0.48), y(0.46)], [x(0.66), y(0.44)], megaports[1]];
      const coastIdx = [8, 22, 36, 52, 66, 80, 95, 110, 124, 138, 152, 166, 180, 196, 210, 224, 234];
      coastIdx.forEach((i, k) => {
        const p = coastPts[i];
        harbors.push({
          x: p[0] + (rnd() - 0.5) * 8,
          y: p[1] + 6 + rnd() * 10,
          r: k % 5 === 2 ? 5.2 : 2.6 + rnd() * 1.6,
          th: 0.12 + (k / coastIdx.length) * 0.55 + rnd() * 0.15,
        });
      });
      islands.forEach((s, k) => {
        const n = k === 1 ? 3 : 2;
        for (let j = 0; j < n; j++) {
          const a = rnd() * Math.PI * 2;
          harbors.push({
            x: s[0] + Math.cos(a) * s[2] * 1.05,
            y: s[1] + Math.sin(a) * s[3] * 1.05,
            r: 2.4 + rnd() * 2.2,
            th: 0.3 + rnd() * 0.5,
          });
        }
      });
      const coastY = (px) => {
        const i = clamp(Math.round(((px + 20) / (W + 40)) * (coastPts.length - 1)), 0, coastPts.length - 1);
        return coastPts[i][1];
      };
      for (let i = 0; i < harbors.length; i++) {
        for (let j = i + 1; j < harbors.length; j++) {
          const a = harbors[i], b = harbors[j], d = Math.hypot(a.x - b.x, a.y - b.y);
          if (d > W * 0.08 && d < W * 0.3 && rnd() < 0.42) {
            const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
            const bow = d * (0.1 + rnd() * 0.14);
            let cy = Math.max(my + bow * 0.7, coastY(mx) + H * 0.045);
            cy = Math.min(cy, my + d * 0.42);
            arcs.push({ a, b, cx: mx + (rnd() - 0.5) * d * 0.2, cy, th: Math.min(a.th, b.th) });
          }
        }
      }
      for (let v = 0; v < 58; v++) {
        const arc = arcs[Math.floor(rnd() * arcs.length)];
        vessels.push({ arc, t: rnd(), sp: (0.0016 + rnd() * 0.0022) * (rnd() < 0.5 ? 1 : -1), trail: [] });
      }
      ships = [
        { t: 0.15, sp: 0.00022 },
        { t: 0.48, sp: 0.00019 },
        { t: 0.8, sp: 0.00024 },
      ];
    }

    function qbez(a, c, b, t) {
      const u = 1 - t;
      return [u * u * a.x + 2 * u * t * c[0] + t * t * b.x, u * u * a.y + 2 * u * t * c[1] + t * t * b.y];
    }
    function trunkPt(t) {
      const segs = trunk.length - 1, s = Math.min(Math.floor(t * segs), segs - 1), f = t * segs - s;
      const p = trunk[s], q = trunk[s + 1];
      return [p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f];
    }
    const smoothstep = (e0, e1, v) => {
      const t = clamp((v - e0) / (e1 - e0), 0, 1);
      return t * t * (3 - 2 * t);
    };

    function resize() {
      const rect = stage.getBoundingClientRect();
      DPR = Math.min(window.devicePixelRatio || 1, 2);
      W = Math.max(320, rect.width || window.innerWidth);
      H = Math.max(320, rect.height || Math.min(window.innerHeight * 0.85, 720));
      cv.width = W * DPR;
      cv.height = H * DPR;
      cv.style.width = W + 'px';
      cv.style.height = H + 'px';
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      buildWorld();
    }

    let mix = 0, target = 0;
    let raf = 0;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const chipA = hud.querySelector('#ns-chipA');
    const chipB = hud.querySelector('#ns-chipB');
    const btnA = hud.querySelector('#ns-btnA');
    const btnB = hud.querySelector('#ns-btnB');

    function draw(now) {
      if (!reduceMotion) mix += (target - mix) * 0.06;
      else mix = target;
      ctx.clearRect(0, 0, W, H);
      const g = ctx.createLinearGradient(0, 0, 0, H);
      g.addColorStop(0, '#070a0f');
      g.addColorStop(1, '#04060a');
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, W, H);
      ctx.beginPath();
      ctx.moveTo(-20, -20);
      ctx.lineTo(-20, coastPts[0][1]);
      coastPts.forEach((p) => ctx.lineTo(p[0], p[1]));
      ctx.lineTo(W + 20, -20);
      ctx.closePath();
      ctx.fillStyle = '#121926';
      ctx.fill();
      ctx.beginPath();
      coastPts.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])));
      ctx.strokeStyle = 'rgba(170,185,205,0.45)';
      ctx.lineWidth = 1.6;
      ctx.stroke();
      ctx.strokeStyle = 'rgba(120,140,165,0.12)';
      ctx.lineWidth = 7;
      ctx.stroke();
      islands.forEach((s) => {
        ctx.save();
        ctx.translate(s[0], s[1]);
        ctx.rotate(s[4]);
        ctx.beginPath();
        ctx.ellipse(0, 0, s[2], s[3], 0, 0, Math.PI * 2);
        ctx.fillStyle = '#121926';
        ctx.fill();
        ctx.strokeStyle = 'rgba(170,185,205,0.38)';
        ctx.lineWidth = 1.3;
        ctx.stroke();
        ctx.restore();
      });

      const A = 1 - mix, B = mix;
      if (A > 0.01) {
        ctx.globalAlpha = A * 0.55;
        ctx.beginPath();
        for (let i = 0; i <= 60; i++) {
          const p = trunkPt(i / 60);
          i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]);
        }
        ctx.strokeStyle = '#5b6572';
        ctx.lineWidth = 3;
        ctx.stroke();
        megaports.forEach((mp) => {
          ctx.globalAlpha = A;
          for (let r = 0; r < 3; r++) {
            ctx.beginPath();
            ctx.arc(mp[0], mp[1], 7 + r * 7, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(139,149,163,${0.5 - r * 0.15})`;
            ctx.lineWidth = 1.4;
            ctx.stroke();
          }
          ctx.beginPath();
          ctx.arc(mp[0], mp[1], 5, 0, Math.PI * 2);
          ctx.fillStyle = '#aeb6c2';
          ctx.fill();
        });
        ships.forEach((s) => {
          if (!reduceMotion) s.t = (s.t + s.sp) % 1;
          const p = trunkPt(s.t), q = trunkPt(Math.min(s.t + 0.01, 1));
          const ang = Math.atan2(q[1] - p[1], q[0] - p[0]);
          ctx.save();
          ctx.translate(p[0], p[1]);
          ctx.rotate(ang);
          ctx.globalAlpha = A * 0.35;
          const wk = ctx.createLinearGradient(-150, 0, -46, 0);
          wk.addColorStop(0, 'rgba(139,149,163,0)');
          wk.addColorStop(1, 'rgba(139,149,163,0.5)');
          ctx.strokeStyle = wk;
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.moveTo(-150, 0);
          ctx.lineTo(-46, 0);
          ctx.stroke();
          ctx.globalAlpha = A * 0.95;
          ctx.beginPath();
          ctx.moveTo(-46, -9);
          ctx.lineTo(34, -9);
          ctx.lineTo(52, 0);
          ctx.lineTo(34, 9);
          ctx.lineTo(-46, 9);
          ctx.closePath();
          ctx.fillStyle = '#69737f';
          ctx.fill();
          ctx.fillStyle = '#535d69';
          ctx.fillRect(-30, -15, 26, 7);
          ctx.restore();
        });
      }
      if (B > 0.01) {
        arcs.forEach((arc) => {
          const on = smoothstep(arc.th, arc.th + 0.18, B);
          if (on <= 0) return;
          ctx.globalAlpha = on * 0.16;
          ctx.beginPath();
          ctx.moveTo(arc.a.x, arc.a.y);
          ctx.quadraticCurveTo(arc.cx, arc.cy, arc.b.x, arc.b.y);
          ctx.strokeStyle = '#d4af5f';
          ctx.lineWidth = 0.8;
          ctx.stroke();
        });
        harbors.forEach((h) => {
          const on = smoothstep(h.th, h.th + 0.15, B);
          if (on <= 0) return;
          const pulse = reduceMotion ? 1 : 1 + 0.18 * Math.sin(now * 0.002 + h.x);
          ctx.globalAlpha = on * 0.9;
          ctx.beginPath();
          ctx.arc(h.x, h.y, h.r * pulse, 0, Math.PI * 2);
          ctx.fillStyle = '#d4af5f';
          ctx.fill();
          ctx.globalAlpha = on * 0.25;
          ctx.beginPath();
          ctx.arc(h.x, h.y, h.r * 2.6 * pulse, 0, Math.PI * 2);
          ctx.fillStyle = '#d4af5f';
          ctx.fill();
        });
        vessels.forEach((v) => {
          const on = smoothstep(v.arc.th, v.arc.th + 0.2, B);
          if (on <= 0) return;
          if (!reduceMotion) {
            v.t += v.sp;
            if (v.t > 1 || v.t < 0) {
              v.arc = arcs[Math.floor(Math.random() * arcs.length)];
              v.t = v.sp > 0 ? 0 : 1;
              v.trail = [];
            }
          }
          const p = qbez(v.arc.a, [v.arc.cx, v.arc.cy], v.arc.b, clamp(v.t, 0, 1));
          if (!reduceMotion) {
            v.trail.push(p);
            if (v.trail.length > 9) v.trail.shift();
          }
          (v.trail || [p]).forEach((tp, i) => {
            const trail = v.trail || [p];
            ctx.globalAlpha = on * (i / trail.length) * 0.5;
            ctx.beginPath();
            ctx.arc(tp[0], tp[1], 1.1, 0, Math.PI * 2);
            ctx.fillStyle = '#e9cf8f';
            ctx.fill();
          });
          ctx.globalAlpha = on;
          ctx.beginPath();
          ctx.arc(p[0], p[1], 1.8, 0, Math.PI * 2);
          ctx.fillStyle = '#f4e3b2';
          ctx.fill();
        });
      }
      ctx.globalAlpha = 1;
      chipA.style.opacity = (0.25 + A * 0.75).toFixed(2);
      chipB.style.opacity = (0.25 + B * 0.75).toFixed(2);
      btnA.className = A > 0.5 ? 'on-a' : '';
      btnB.className = B >= 0.5 ? 'on-b' : '';
      raf = requestAnimationFrame(draw);
    }

    btnA.onclick = () => { target = 0; };
    btnB.onclick = () => { target = 1; };

    function setNetworkMix(m) {
      target = clamp(Number(m) || 0, 0, 1);
    }
    global.setNetworkMix = setNetworkMix;

    const ro = new ResizeObserver(() => resize());
    ro.observe(stage);
    resize();
    raf = requestAnimationFrame(draw);

    return {
      setNetworkMix,
      destroy() {
        cancelAnimationFrame(raf);
        ro.disconnect();
        if (global.setNetworkMix === setNetworkMix) delete global.setNetworkMix;
      },
    };
  }

  global.initNetworkShift = initNetworkShift;
})(typeof window !== 'undefined' ? window : globalThis);
