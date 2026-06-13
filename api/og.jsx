/* eslint-disable @next/next/no-img-element */
import { ImageResponse } from '@vercel/og';

export const config = { runtime: 'edge' };

const FONT = 'Inter, system-ui, sans-serif';

export default function handler(req) {
  const { searchParams } = new URL(req.url);
  const title = (searchParams.get('title') || 'Navier Atlas').slice(0, 90);
  const subtitle = (searchParams.get('subtitle') || 'Electric-hydrofoil mobility network').slice(0, 120);
  const badge = (searchParams.get('badge') || 'Mobility').slice(0, 36);
  const type = searchParams.get('type') || 'share';

  const accent = type === 'cluster' ? '#7dd3fc' : type === 'city' ? '#6ee7b7' : type === 'market' ? '#e0cb8f' : '#a78bfa';

  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '56px 64px',
          background: 'linear-gradient(145deg, #0a0e14 0%, #121820 45%, #0d1520 100%)',
          fontFamily: FONT,
          color: '#f1f5f9',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <div
            style={{
              width: 52,
              height: 52,
              borderRadius: 14,
              background: '#0a0a0a',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              border: '1px solid rgba(255,255,255,0.12)',
            }}
          >
            <svg width="28" height="28" viewBox="0 0 180 180" fill="white">
              <path d="M130.16 117.84L120.18 135.12A0.39 0.39 0 0 1 119.50 135.11L68.16 44.06A0.39 0.39 0 0 1 68.50 43.48L88.22 43.48A0.39 0.39 0 0 1 88.56 43.68L130.16 117.46A0.39 0.39 0 0 1 130.16 117.84Z" />
            </svg>
          </div>
          <div style={{ fontSize: 22, fontWeight: 600, letterSpacing: '-0.02em', opacity: 0.92 }}>Navier Atlas</div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 20, maxWidth: 1000 }}>
          <div
            style={{
              display: 'inline-flex',
              alignSelf: 'flex-start',
              fontSize: 18,
              fontWeight: 600,
              color: accent,
              background: `${accent}22`,
              border: `1px solid ${accent}55`,
              borderRadius: 999,
              padding: '8px 18px',
            }}
          >
            {badge}
          </div>
          <div style={{ fontSize: 58, fontWeight: 700, lineHeight: 1.08, letterSpacing: '-0.03em' }}>{title}</div>
          <div style={{ fontSize: 26, lineHeight: 1.35, color: 'rgba(241,245,249,0.72)', maxWidth: 920 }}>{subtitle}</div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
          <div style={{ fontSize: 18, color: 'rgba(241,245,249,0.45)' }}>Pioneer II · Quanta-LR · Interactive map</div>
          <div
            style={{
              width: 180,
              height: 4,
              borderRadius: 2,
              background: `linear-gradient(90deg, ${accent}, transparent)`,
            }}
          />
        </div>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}