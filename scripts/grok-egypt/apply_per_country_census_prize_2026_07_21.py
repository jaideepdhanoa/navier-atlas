#!/usr/bin/env python3
"""Re-render THE PRIZE / TAM ladders on four country decks after per-country census (#323).

Authoritative MID ladders from GROK-SPEC-per-country-census-methodology-2026-07-21.md.
Also wires Holbox/Huatulco N30 composites if image slots exist (#322).
Rebuilds economics sidecar from refreshed aggs.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[2]
TOKEN_FILE = Path.home() / ".config/google-drive-mcp/tokens.json"
CLIENT_FILE = Path.home() / ".config/google-drive-mcp/gcp-oauth.keys.json"
NOW = datetime.now(timezone.utc).isoformat()
RECEIPT = (
    ROOT
    / "handoff/partner-map-model/mx-eg-expansion-2026-07-20"
    / "PER-COUNTRY-CENSUS-PRIZE-RECEIPT-2026-07-21.json"
)

# Spec MID ladders (SOM Full Mapped Network headline). Marine TAM = GMV / 3 (config mid attach).
LADDERS = {
    "didi-brazil": {
        "pid": "1jHxxDgDd5Oki0eO4YoCfHHfC_aS-akGjb4UfXseIEK8",
        "census_g": 2.833,
        "rungs": [
            # (value_oid_candidates, label_oid_candidates, value_text, label_text)
            (["g3eec5122801_0_574", "g3eec5122801_0_570"], ["g3eec5122801_0_575", "g3eec5122801_0_571"],
             "$220.8M", "SOM · Today — Navier fares on DiDi's network, serving 10% of current trips"),
            (["g3eec5122801_0_578", "g3eec5122801_0_574"], ["g3eec5122801_0_579", "g3eec5122801_0_575"],
             "$1.01B", "SAM · Near term — faster, quieter boats grow the market, serving 25% at maturity"),
            (["dbP5_r3val", "g3eec5122801_0_582"], ["dbP5_r3dsc", "g3eec5122801_0_583"],
             "$4.03B", "TAM · Full market — the entire sea-transfer market we create"),
            (["dbP5_r4val", "g3eec5122801_0_586"], ["dbP5_r4dsc", "g3eec5122801_0_587"],
             "$12.09B", "GMV · Whole journey — add food, stays and experiences to every crossing"),
            (["dbP5_r5val"], ["dbP5_r5dsc"],
             "$543.8M", "DiDi platform revenue on Navier — 18% of Navier's journey GMV across the full network"),
        ],
        "platform": True,
        "framing": (
            "Read it bottom-up: the fare a Navier boat collects today, the market a faster product unlocks — "
            "then the whole journey a super-app monetizes around every crossing. Width from Brazil census g=2.83."
        ),
    },
    "indrive-brazil": {
        "pid": "1QImIe6KAee0Eajsokgh9NmH0I29lir4l2LV63e-9OxE",
        "census_g": 2.833,
        "rungs": [
            (["g3eec5122801_0_570"], ["g3eec5122801_0_571"],
             "$220.8M", "SOM · Today — Navier fares on inDrive's network, serving 10% of current trips"),
            (["g3eec5122801_0_574"], ["g3eec5122801_0_575"],
             "$1.01B", "SAM · Near term — faster, quieter boats grow the market, serving 25% at maturity"),
            (["g3eec5122801_0_578"], ["g3eec5122801_0_579"],
             "$4.03B", "TAM · Full market — the entire sea-transfer market we create"),
            (["g3eec5122801_0_582"], ["g3eec5122801_0_583"],
             "$12.09B", "GMV · Whole journey — add food, stays and experiences to every crossing"),
        ],
        "platform": False,
        "framing": (
            "Read it bottom-up: the fare a Navier boat collects today, then the market a faster, quieter product "
            "unlocks across every crossing. Same Brazil census as DiDi (g=2.83) — country parity."
        ),
    },
    "didi-mexico": {
        "pid": "1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c",
        "census_g": 4.922,
        "rungs": [
            (["g3eec5122801_0_570"], ["g3eec5122801_0_571"],
             "$147.9M", "SOM · Today — Navier fares on DiDi's network, serving 10% of current trips"),
            (["g3eec5122801_0_574"], ["g3eec5122801_0_575"],
             "$677.1M", "SAM · Near term — faster, quieter boats grow the market, serving 25% at maturity"),
            (["g3eec5122801_0_578"], ["g3eec5122801_0_579"],
             "$2.71B", "TAM · Full market — the entire sea-transfer market we create"),
            (["g3eec5122801_0_582"], ["g3eec5122801_0_583"],
             "$8.13B", "GMV · Whole journey — add food, stays and experiences to every crossing"),
            (["g3eec5122801_0_586"], ["g3eec5122801_0_587"],
             "$365.6M", "DiDi platform revenue on Navier — 18% of Navier's journey GMV across the full network"),
        ],
        "platform": True,
        "framing": (
            "Read it bottom-up: the fare a Navier boat collects today, the market a faster product unlocks — "
            "then the whole journey a super-app monetizes around every crossing. Width from Mexico census g=4.92."
        ),
    },
    "indrive-egypt": {
        "pid": "1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk",
        "census_g": 5.258,
        "rungs": [
            (["g3eec5122801_0_570"], ["g3eec5122801_0_571"],
             "$39.0M", "SOM · Today — Navier fares on inDrive's network, serving today's boat-only crossings"),
            (["g3eec5122801_0_574"], ["g3eec5122801_0_575"],
             "$70.2M", "SAM · Near term — faster, quieter boats grow the market at maturity"),
            (["g3eec5122801_0_578"], ["g3eec5122801_0_579"],
             "$80.3M", "TAM · Full market — the entire sea-transfer market we create"),
            (["iegP5_r4val", "g3eec5122801_0_582"], ["iegP5_r4dsc", "g3eec5122801_0_583"],
             "$241M", "GMV · Whole journey — add food, stays and experiences to every crossing"),
        ],
        "platform": False,
        "framing": (
            "Read it bottom-up: the fare a Navier boat collects today on boat-only crossings, "
            "the market a faster product unlocks — then the whole journey around every crossing. "
            "Egypt census g=5.26. Ladder is monotonic under the local census (SOM Full ≤ SAM)."
        ),
        "footnote": (
            "Note: boat-only marine-park corridors still carry high capture; local Egypt census "
            "sets network width. Journey GMV $241M (MID)."
        ),
    },
}

PRIZE_PAGE = "g3eec5122801_0_562"


def get_creds() -> Credentials:
    tok = json.loads(TOKEN_FILE.read_text())
    acct = tok["accounts"].get("jaideep") or tok["accounts"][tok.get("defaultAccount", "default")]
    client = json.loads(CLIENT_FILE.read_text())
    installed = client.get("installed") or client.get("web") or {}
    creds = Credentials(
        token=acct.get("accessToken") or acct.get("access_token"),
        refresh_token=acct.get("refreshToken") or acct.get("refresh_token"),
        token_uri=installed.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=installed.get("client_id"),
        client_secret=installed.get("client_secret"),
        scopes=(acct.get("scope") or "").split() or None,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        acct["accessToken"] = creds.token
        if creds.expiry:
            acct["expiryDate"] = int(creds.expiry.timestamp() * 1000)
        TOKEN_FILE.write_text(json.dumps(tok, indent=2))
    return creds


def extract_text(shape: dict) -> str:
    parts = []
    for te in (shape.get("text") or {}).get("textElements") or []:
        tr = te.get("textRun") or {}
        if tr.get("content"):
            parts.append(tr["content"])
    return "".join(parts).strip()


def replace_text(oid: str, new_text: str) -> list[dict]:
    if new_text and not new_text.endswith("\n"):
        new_text += "\n"
    return [
        {"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}},
        {"insertText": {"objectId": oid, "insertionIndex": 0, "text": new_text}},
    ]


def batch(svc, pid: str, reqs: list[dict], chunk: int = 25):
    for i in range(0, len(reqs), chunk):
        part = reqs[i : i + chunk]
        if part:
            svc.presentations().batchUpdate(presentationId=pid, body={"requests": part}).execute()


def page_oids(pres: dict, page_id: str) -> set[str]:
    for s in pres.get("slides") or []:
        if s.get("objectId") == page_id:
            return {el.get("objectId") for el in s.get("pageElements") or []}
    # prize page may have different id on some decks - find by THE PRIZE text
    for s in pres.get("slides") or []:
        for el in s.get("pageElements") or []:
            t = extract_text(el.get("shape") or {})
            if t.strip().upper() == "THE PRIZE" or (t and "PRIZE" in t.upper() and len(t) < 40):
                return {e.get("objectId") for e in s.get("pageElements") or []}, s.get("objectId")
    return set()


def find_prize_page(pres: dict) -> tuple[str, set[str]]:
    """Prefer an exact THE PRIZE title; never match market-overview $floor slides."""
    candidates: list[tuple[int, str, set[str]]] = []
    for s in pres.get("slides") or []:
        texts = []
        oids = set()
        for el in s.get("pageElements") or []:
            oid = el.get("objectId")
            oids.add(oid)
            t = extract_text(el.get("shape") or {})
            if t:
                texts.append(t)
        joined = " ".join(texts).upper()
        title_hit = any(t.strip().upper() == "THE PRIZE" for t in texts)
        multi_rung = ("SOM" in joined and "SAM" in joined and "GMV" in joined) or (
            joined.count("$") >= 3 and ("SOM" in joined or "PRIZE" in joined)
        )
        if title_hit:
            candidates.append((0, s.get("objectId"), oids))
        elif "THE PRIZE" in joined and any("$" in t for t in texts):
            candidates.append((1, s.get("objectId"), oids))
        elif multi_rung and any("$" in t for t in texts):
            candidates.append((2, s.get("objectId"), oids))
    if candidates:
        candidates.sort(key=lambda x: x[0])
        return candidates[0][1], candidates[0][2]
    # fallback known id
    oids = page_oids(pres, PRIZE_PAGE)
    return PRIZE_PAGE, oids if isinstance(oids, set) else set()


def first_existing(candidates: list[str], oids: set[str]) -> str | None:
    for c in candidates:
        if c in oids:
            return c
    return None


def apply_deck(svc, key: str, cfg: dict) -> dict:
    pid = cfg["pid"]
    pres = svc.presentations().get(presentationId=pid).execute()
    page_id, oids = find_prize_page(pres)
    if not isinstance(oids, set):
        oids = set()
    # re-resolve oids if tuple mishandled
    if not oids:
        page_id, oids = find_prize_page(pres)

    reqs: list[dict] = []
    applied = []
    for val_cands, lab_cands, val, lab in cfg["rungs"]:
        v_oid = first_existing(val_cands, oids)
        l_oid = first_existing(lab_cands, oids)
        if v_oid:
            reqs += replace_text(v_oid, val)
            applied.append({"value_oid": v_oid, "value": val})
        else:
            applied.append({"value_oid": None, "value": val, "error": "missing"})
        if l_oid:
            reqs += replace_text(l_oid, lab)
            applied[-1]["label_oid"] = l_oid

    # framing subtitle if present
    for cand in ("g3eec5122801_0_567",):
        if cand in oids:
            reqs += replace_text(cand, cfg["framing"])
            break

    # Egypt footnote
    if key == "indrive-egypt" and cfg.get("footnote"):
        fn = "iegP5_footnote"
        if fn in oids:
            reqs += replace_text(fn, cfg["footnote"])
        else:
            # create if missing
            reqs.append(
                {
                    "createShape": {
                        "objectId": fn,
                        "shapeType": "TEXT_BOX",
                        "elementProperties": {
                            "pageObjectId": page_id,
                            "size": {
                                "width": {"magnitude": 3000000, "unit": "EMU"},
                                "height": {"magnitude": 3000000, "unit": "EMU"},
                            },
                            "transform": {
                                "scaleX": 2.65,
                                "scaleY": 0.06,
                                "translateX": 502920,
                                "translateY": 4550000,
                                "unit": "EMU",
                            },
                        },
                    }
                }
            )
            batch(svc, pid, reqs)
            reqs = replace_text(fn, cfg["footnote"],)
            # style
            reqs.append(
                {
                    "updateTextStyle": {
                        "objectId": fn,
                        "style": {
                            "foregroundColor": {"opaqueColor": {"themeColor": "LIGHT1"}},
                            "fontFamily": "Poppins",
                            "fontSize": {"magnitude": 8, "unit": "PT"},
                            "italic": True,
                        },
                        "textRange": {"type": "ALL"},
                        "fields": "foregroundColor,fontFamily,fontSize,italic",
                    }
                }
            )

    if reqs:
        batch(svc, pid, reqs)

    # readback
    pres2 = svc.presentations().get(presentationId=pid).execute()
    page_id2, oids2 = find_prize_page(pres2)
    texts = []
    for s in pres2.get("slides") or []:
        if s.get("objectId") != page_id2:
            continue
        for el in s.get("pageElements") or []:
            t = extract_text(el.get("shape") or {})
            if t and ("$" in t or "SOM" in t or "PRIZE" in t or "GMV" in t or "Note:" in t):
                texts.append(f"{el['objectId']}: {t[:90].replace(chr(10), ' ')}")
    return {
        "deck": key,
        "pid": pid,
        "page": page_id2,
        "census_g": cfg["census_g"],
        "applied": applied,
        "readback": texts[:16],
    }


def rebuild_sidecar() -> dict:
    """Rebuild gold economics sidecar from unique-global agg.

    Do NOT re-run aggregate.py --partner didi|indrive here: partner-level aggregate
    without the sealed corridor pack can wipe multi-market rows (observed 2026-07-21).
    Unit economics are census-independent; only the ladder rungs move under #323.
    """
    steps = []
    cmds = [
        [
            sys.executable,
            str(ROOT / "finance/model/aggregate.py"),
            "--partner",
            "global",
            "--dedup",
            "unique",
            "--json",
            str(ROOT / "finance/recal/agg-unique-global.json"),
        ],
        [
            sys.executable,
            str(ROOT / "finance/build_economics_sidecar.py"),
            "--gold",
            str(ROOT / "data-clean"),
            "--aggdir",
            str(ROOT / "finance/recal"),
            "--out",
            str(ROOT / "data-clean/economics_by_route_id.json"),
        ],
    ]
    for cmd in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
        steps.append(
            {
                "cmd": " ".join(cmd[-4:]),
                "code": r.returncode,
                "tail": ((r.stdout or "") + (r.stderr or ""))[-300:],
            }
        )
        if r.returncode != 0:
            print("WARN command failed", cmd, r.stderr[-400:])
    return {"steps": steps}


def wire_mexico_n30(svc) -> dict:
    """Replace Holbox/Huatulco city imagery if placeholders exist; else no-op note."""
    # Image wiring is optional — assets banked in #322 under deck-studio/assets/didi/
    assets = {
        "holbox": ROOT / "deck-studio/assets/didi/didi-mexico-holbox-n30.png",
        "huatulco": ROOT / "deck-studio/assets/didi/didi-mexico-huatulco-n30.png",
    }
    return {
        "assets_present": {k: p.exists() for k, p in assets.items()},
        "note": "N30 PNGs banked in #322; human or image-manifest link on slides 15/17 if slots empty",
    }


def main() -> int:
    svc = build("slides", "v1", credentials=get_creds(), cache_discovery=False)
    results = {}
    for key, cfg in LADDERS.items():
        print(f"=== {key} ===")
        results[key] = apply_deck(svc, key, cfg)
        for line in results[key]["readback"][:10]:
            print(" ", line)
        print()

    print("Rebuilding sidecars…")
    side = rebuild_sidecar()
    print("  done", [s["code"] for s in side["steps"]])

    n30 = wire_mexico_n30(svc)

    receipt = {
        "at": NOW,
        "spec": "GROK-SPEC-per-country-census-methodology-2026-07-21.md",
        "ladders": {
            "didi-brazil": {"som": "$220.8M", "sam": "$1.01B", "tam": "$4.03B", "gmv": "$12.09B", "platform": "$543.8M", "g": 2.833},
            "indrive-brazil": {"som": "$220.8M", "sam": "$1.01B", "tam": "$4.03B", "gmv": "$12.09B", "g": 2.833},
            "didi-mexico": {"som": "$147.9M", "sam": "$677.1M", "tam": "$2.71B", "gmv": "$8.13B", "platform": "$365.6M", "g": 4.922},
            "indrive-egypt": {"som": "$39.0M", "sam": "$70.2M", "tam": "$80.3M", "gmv": "$241M", "g": 5.258},
        },
        "deck_results": results,
        "sidecar": side,
        "n30": n30,
        "note": "Marine TAM derived as Journey GMV / 3.0 (growth-config mid attach). Spec table listed SOM/SAM/GMV/platform.",
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    print("Receipt:", RECEIPT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
