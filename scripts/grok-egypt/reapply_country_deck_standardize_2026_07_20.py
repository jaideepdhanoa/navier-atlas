#!/usr/bin/env python3
"""Country-deck standardization live apply (GROK-SPEC 2026-07-20).

1. inDrive Egypt THE PRIZE regen (4 rungs + non-monotonic capture footnote)
2. WHAT ONE BOAT EARNS · {CITY} titles (inDrive BR/Egypt, DiDi Mexico)
3. Link chips (Interactive / Model deepdive / Detailed market sizing)
4. inDrive Brazil backup restructure (mirror DiDi Brazil)
5. slide-manifest sync from live

Slides API only. Sheet MID column authoritative for prize rungs.
"""
from __future__ import annotations

import json
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
    / "handoff/partner-map-model/brazil-expansion-2026-07-19"
    / "COUNTRY-DECK-STANDARDIZE-RECEIPT-2026-07-20.json"
)

DECKS = {
    "didi-brazil": "1jHxxDgDd5Oki0eO4YoCfHHfC_aS-akGjb4UfXseIEK8",
    "indrive-brazil": "1QImIe6KAee0Eajsokgh9NmH0I29lir4l2LV63e-9OxE",
    "didi-mexico": "1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c",
    "indrive-egypt": "1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk",
}

SHEETS = {
    "didi-brazil": "13BViN3uXgVK8uO8KXRIVwgAZnPrDedNfaRnTIjhpbLA",
    "didi-mexico": "1AtoSyNtAZtYiW-duU0oxZTgdtpWW4Al3xuUAHnqlFg0",
    "indrive-brazil": "1N1pPyZrJFa_mV_3MTMxw1eEs6yC-oeBl2jyd93kvvWY",
    "indrive-egypt": "1qD2uF6v3ZnPhLtDnmwnf-hV70nq745PYXiF11p_ZpUU",
}

ATLAS = {
    "didi-brazil": "https://navier-atlas.vercel.app/didi/brazil",
    "indrive-brazil": "https://navier-atlas.vercel.app/indrive",
    "didi-mexico": "https://navier-atlas.vercel.app/didi/mexico-caribbean",
    "indrive-egypt": "https://navier-atlas.vercel.app/indrive/egypt-red-sea",
}

CHIP_STYLE = {
    "foregroundColor": {"opaqueColor": {"themeColor": "LIGHT1"}},
    "bold": False,
    "italic": False,
    "fontFamily": "Poppins",
    "fontSize": {"magnitude": 9.5, "unit": "PT"},
    "underline": True,
    "weightedFontFamily": {"fontFamily": "Poppins", "weight": 400},
}

CHIP_BOX = {
    "size": {
        "width": {"magnitude": 3000000, "unit": "EMU"},
        "height": {"magnitude": 3000000, "unit": "EMU"},
    },
    "transform": {
        "scaleX": 0.4909,
        "scaleY": 0.0487,
        "translateX": 521200,
        "translateY": 576350,
        "unit": "EMU",
    },
}


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


def replace_text(oid: str, new_text: str, *, empty: bool = False) -> list[dict]:
    if new_text and not new_text.endswith("\n"):
        new_text += "\n"
    if empty:
        return [{"insertText": {"objectId": oid, "insertionIndex": 0, "text": new_text}}]
    return [
        {"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}},
        {"insertText": {"objectId": oid, "insertionIndex": 0, "text": new_text}},
    ]


def batch(svc, pid: str, reqs: list[dict], chunk: int = 30):
    for i in range(0, len(reqs), chunk):
        part = reqs[i : i + chunk]
        if part:
            svc.presentations().batchUpdate(presentationId=pid, body={"requests": part}).execute()


def sheet_url(slug: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{SHEETS[slug]}/edit"


def make_chip(page_id: str, oid: str, label: str, url: str) -> list[dict]:
    """Create a linked text-box chip matching DiDi Brazil style."""
    style = dict(CHIP_STYLE)
    style["link"] = {"url": url}
    text = label if label.endswith("\n") else label + "\n"
    return [
        {
            "createShape": {
                "objectId": oid,
                "shapeType": "TEXT_BOX",
                "elementProperties": {
                    "pageObjectId": page_id,
                    "size": CHIP_BOX["size"],
                    "transform": CHIP_BOX["transform"],
                },
            }
        },
        {"insertText": {"objectId": oid, "insertionIndex": 0, "text": text}},
        {
            "updateTextStyle": {
                "objectId": oid,
                "style": style,
                "textRange": {"type": "ALL"},
                "fields": "foregroundColor,bold,italic,fontFamily,fontSize,underline,weightedFontFamily,link",
            }
        },
    ]


def oid_exists(slide: dict, oid: str) -> bool:
    return any(el.get("objectId") == oid for el in slide.get("pageElements") or [])


# ── 1. Egypt THE PRIZE ──────────────────────────────────────────────────────


def apply_egypt_prize(svc) -> dict:
    pid = DECKS["indrive-egypt"]
    page = "g3eec5122801_0_562"
    pres = svc.presentations().get(presentationId=pid).execute()
    slide = next(s for s in pres["slides"] if s["objectId"] == page)
    existing = {el["objectId"] for el in slide.get("pageElements") or []}

    # Targets from sheet MID (spec table)
    rungs = [
        (
            "g3eec5122801_0_570",
            "g3eec5122801_0_571",
            "$36.4M",
            "SOM · Today — Navier fares on inDrive's network, serving today's boat-only crossings",
        ),
        (
            "g3eec5122801_0_574",
            "g3eec5122801_0_575",
            "$18.7M",
            "SAM · Near term — faster, quieter boats grow the market at maturity",
        ),
        (
            "g3eec5122801_0_578",
            "g3eec5122801_0_579",
            "$75.0M",
            "TAM · Full market — the entire sea-transfer market we create",
        ),
    ]
    gmv_val, gmv_dsc = "$224.9M", "GMV · Whole journey — add food, stays and experiences to every crossing"
    footnote = (
        "Note: SOM sits above SAM because Egypt's boat-only marine-park corridors "
        "carry ~87% capture today — the floor already reflects high share."
    )
    title = "THE PRIZE"
    subtitle = "A new multi-hundred-million-dollar vertical for inDrive Egypt"
    framing = (
        "Read it bottom-up: the fare a Navier boat collects today on boat-only crossings, "
        "the market a faster product unlocks — then the whole journey around every crossing. "
        "SOM > SAM is intentional (see footnote)."
    )

    reqs: list[dict] = []
    reqs += replace_text("g3eec5122801_0_563", title)
    reqs += replace_text("g3eec5122801_0_565", subtitle)
    reqs += replace_text("g3eec5122801_0_567", framing)
    for val_oid, dsc_oid, val, dsc in rungs:
        reqs += replace_text(val_oid, val)
        reqs += replace_text(dsc_oid, dsc)

    # 4th rung (Journey GMV) — clone geometry of rung 3, offset +493776 EMU
    DY = 493776
    r4_ids = {
        "bg": "iegP5_r4bg",
        "gd": "iegP5_r4gd",
        "val": "iegP5_r4val",
        "dsc": "iegP5_r4dsc",
    }
    # Source rung-3 elements
    src = {
        "bg": "g3eec5122801_0_576",
        "gd": "g3eec5122801_0_577",
        "val": "g3eec5122801_0_578",
        "dsc": "g3eec5122801_0_579",
    }
    el_by_id = {el["objectId"]: el for el in slide.get("pageElements") or []}

    if r4_ids["val"] not in existing:
        for key, src_oid in src.items():
            el = el_by_id[src_oid]
            tr = dict(el.get("transform") or {})
            tr["translateY"] = float(tr.get("translateY") or 0) + DY
            tr["unit"] = tr.get("unit") or "EMU"
            size = el.get("size") or {
                "width": {"magnitude": 3000000, "unit": "EMU"},
                "height": {"magnitude": 3000000, "unit": "EMU"},
            }
            new_oid = r4_ids[key]
            reqs.append(
                {
                    "createShape": {
                        "objectId": new_oid,
                        "shapeType": (el.get("shape") or {}).get("shapeType") or "TEXT_BOX",
                        "elementProperties": {
                            "pageObjectId": page,
                            "size": size,
                            "transform": tr,
                        },
                    }
                }
            )
            # copy fill for bar backgrounds when present
            fill = ((el.get("shape") or {}).get("shapeProperties") or {}).get("shapeBackgroundFill")
            if fill and fill.get("solidFill") and key in ("bg", "gd"):
                reqs.append(
                    {
                        "updateShapeProperties": {
                            "objectId": new_oid,
                            "shapeProperties": {"shapeBackgroundFill": fill},
                            "fields": "shapeBackgroundFill",
                        }
                    }
                )

        # insert values after create
        batch(svc, pid, reqs)
        reqs = []
        reqs += replace_text(r4_ids["val"], gmv_val, empty=True)
        reqs += replace_text(r4_ids["dsc"], gmv_dsc, empty=True)
        # style value/desc to match rung 3
        for key, src_oid in (("val", src["val"]), ("dsc", src["dsc"])):
            el = el_by_id[src_oid]
            style = None
            for te in ((el.get("shape") or {}).get("text") or {}).get("textElements") or []:
                if (te.get("textRun") or {}).get("style"):
                    style = te["textRun"]["style"]
                    break
            if style:
                # drop link if any; keep visual fields
                fields = []
                clean = {}
                for f in (
                    "foregroundColor",
                    "bold",
                    "italic",
                    "fontFamily",
                    "fontSize",
                    "weightedFontFamily",
                    "underline",
                ):
                    if f in style:
                        clean[f] = style[f]
                        fields.append(f)
                if clean:
                    reqs.append(
                        {
                            "updateTextStyle": {
                                "objectId": r4_ids[key],
                                "style": clean,
                                "textRange": {"type": "ALL"},
                                "fields": ",".join(fields),
                            }
                        }
                    )
    else:
        reqs += replace_text(r4_ids["val"], gmv_val)
        reqs += replace_text(r4_ids["dsc"], gmv_dsc)

    # Footnote
    fn_oid = "iegP5_footnote"
    if fn_oid not in existing:
        reqs.append(
            {
                "createShape": {
                    "objectId": fn_oid,
                    "shapeType": "TEXT_BOX",
                    "elementProperties": {
                        "pageObjectId": page,
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
        reqs = []
        reqs += replace_text(fn_oid, footnote, empty=True)
        reqs.append(
            {
                "updateTextStyle": {
                    "objectId": fn_oid,
                    "style": {
                        "foregroundColor": {"opaqueColor": {"themeColor": "LIGHT1"}},
                        "fontFamily": "Poppins",
                        "fontSize": {"magnitude": 8, "unit": "PT"},
                        "italic": True,
                        "weightedFontFamily": {"fontFamily": "Poppins", "weight": 400},
                    },
                    "textRange": {"type": "ALL"},
                    "fields": "foregroundColor,fontFamily,fontSize,italic,weightedFontFamily",
                }
            }
        )
    else:
        reqs += replace_text(fn_oid, footnote)

    # Detailed market sizing chip on prize slide
    chip_oid = "iegP5_chip_sizing"
    if chip_oid not in existing:
        reqs += make_chip(page, chip_oid, "Detailed market sizing", sheet_url("indrive-egypt"))

    if reqs:
        batch(svc, pid, reqs)

    return {
        "page": page,
        "rungs": ["$36.4M", "$18.7M", "$75.0M", "$224.9M"],
        "footnote": footnote,
        "chip": chip_oid,
    }


# ── 2. Econ titles ──────────────────────────────────────────────────────────


ECON_TITLE_MAP = {
    # deck_slug -> list of (element_id, new_title)
    "indrive-egypt": [
        ("g3eec5122801_0_203", "WHAT ONE BOAT EARNS · HURGHADA"),
        ("g3eec5122801_0_449", "WHAT ONE BOAT EARNS · SHARM EL SHEIKH"),
    ],
    "didi-mexico": [
        ("g3eec5122801_0_703", "WHAT ONE BOAT EARNS · ISLA MUJERES"),
        ("mxcoz_title", "WHAT ONE BOAT EARNS · COZUMEL"),
    ],
    "indrive-brazil": [
        ("g3eec5122801_0_298", "WHAT ONE BOAT EARNS · RIO DE JANEIRO"),
        ("ibAtitle", "WHAT ONE BOAT EARNS · ANGRA DOS REIS"),
        ("ibFtitle", "WHAT ONE BOAT EARNS · FLORIANÓPOLIS"),
        ("iek_salvador", "WHAT ONE BOAT EARNS · SALVADOR"),
        ("iek_ilhabela", "WHAT ONE BOAT EARNS · ILHABELA"),
        ("iek_santos", "WHAT ONE BOAT EARNS · SANTOS–GUARUJÁ"),
        ("iek_vitoria", "WHAT ONE BOAT EARNS · VITÓRIA"),
        ("iek_ilhamel", "WHAT ONE BOAT EARNS · ILHA DO MEL"),
    ],
}


def apply_econ_titles(svc) -> dict:
    out = {}
    for slug, pairs in ECON_TITLE_MAP.items():
        pid = DECKS[slug]
        reqs: list[dict] = []
        for oid, title in pairs:
            reqs += replace_text(oid, title)
        batch(svc, pid, reqs)
        out[slug] = [{"oid": o, "title": t} for o, t in pairs]
    return out


# ── 3. Link chips ───────────────────────────────────────────────────────────


def apply_chips(svc) -> dict:
    """Add Interactive / Model deepdive / Detailed market sizing chips where missing.

    Placement mirrors DiDi Brazil:
    - Interactive on market-overview + city deep-dives
    - Model deepdive on unit-econ slides
    - Detailed market sizing on THE PRIZE
    """
    out: dict = {}

    # inDrive Egypt
    pid = DECKS["indrive-egypt"]
    pres = svc.presentations().get(presentationId=pid).execute()
    slides = {s["objectId"]: s for s in pres["slides"]}
    reqs: list[dict] = []
    atlas = ATLAS["indrive-egypt"]
    sheet = sheet_url("indrive-egypt")

    # market overview
    ov = "g3eec5122801_0_0"
    if not oid_exists(slides[ov], "ieg_chip_interactive"):
        reqs += make_chip(ov, "ieg_chip_interactive", "Interactive link", atlas)
    # city slides
    for page, oid in [
        ("g3eec5122801_0_106", "ieg_chip_int_hurghada"),
        ("g3eec5122801_0_391", "ieg_chip_int_sharm"),
    ]:
        if not oid_exists(slides[page], oid):
            reqs += make_chip(page, oid, "Interactive link", atlas)
    # econ slides
    for page, oid in [
        ("g3eec5122801_0_201", "ieg_chip_model_hurghada"),
        ("g3eec5122801_0_448", "ieg_chip_model_sharm"),
    ]:
        if not oid_exists(slides[page], oid):
            reqs += make_chip(page, oid, "Model deepdive", sheet)
    # prize chip already handled in apply_egypt_prize
    if reqs:
        batch(svc, pid, reqs)
    out["indrive-egypt"] = {"atlas": atlas, "sheet": sheet, "n_reqs": len(reqs)}

    # DiDi Mexico
    pid = DECKS["didi-mexico"]
    pres = svc.presentations().get(presentationId=pid).execute()
    slides = {s["objectId"]: s for s in pres["slides"]}
    reqs = []
    atlas = ATLAS["didi-mexico"]
    sheet = sheet_url("didi-mexico")
    for page, oid, label, url in [
        ("g3eec5122801_0_0", "dmx_chip_interactive", "Interactive link", atlas),
        ("g3eec5122801_0_106", "dmx_chip_int_isla", "Interactive link", atlas),
        ("g3eec5122801_0_391", "dmx_chip_int_coz", "Interactive link", atlas),
        ("g3eec5122801_0_201", "dmx_chip_int_extra1", "Interactive link", atlas),
        ("g3eec5122801_0_296", "dmx_chip_int_extra2", "Interactive link", atlas),
        ("g3eec5122801_0_701", "dmx_chip_model_isla", "Model deepdive", sheet),
        ("mxcoz_econ", "dmx_chip_model_coz", "Model deepdive", sheet),
        ("g3eec5122801_0_562", "dmx_chip_sizing", "Detailed market sizing", sheet),
    ]:
        if page in slides and not oid_exists(slides[page], oid):
            reqs += make_chip(page, oid, label, url)
    if reqs:
        batch(svc, pid, reqs)
    out["didi-mexico"] = {"atlas": atlas, "sheet": sheet, "n_reqs": len(reqs)}

    # inDrive Brazil
    pid = DECKS["indrive-brazil"]
    pres = svc.presentations().get(presentationId=pid).execute()
    slides = {s["objectId"]: s for s in pres["slides"]}
    reqs = []
    atlas = ATLAS["indrive-brazil"]
    sheet = sheet_url("indrive-brazil")
    city_pages = [
        "g3eec5122801_0_0",
        "g3eec5122801_0_106",
        "g3eec5122801_0_391",
        "g3eec5122801_0_201",
        "idSlide_salvador",
        "idSlide_ilhabela",
        "idSlide_santos",
        "idSlide_vitoria",
        "idSlide_ilhamel",
    ]
    econ_pages = [
        "g3eec5122801_0_296",
        "ibAngraEcon",
        "ibFlorEcon",
        "ieSlide_salvador",
        "ieSlide_ilhabela",
        "ieSlide_santos",
        "ieSlide_vitoria",
        "ieSlide_ilhamel",
    ]
    for i, page in enumerate(city_pages):
        oid = f"ibr_chip_int_{i}"
        if page in slides and not oid_exists(slides[page], oid):
            reqs += make_chip(page, oid, "Interactive link", atlas)
    for i, page in enumerate(econ_pages):
        oid = f"ibr_chip_model_{i}"
        if page in slides and not oid_exists(slides[page], oid):
            reqs += make_chip(page, oid, "Model deepdive", sheet)
    prize = "g3eec5122801_0_562"
    if prize in slides and not oid_exists(slides[prize], "ibr_chip_sizing"):
        reqs += make_chip(prize, "ibr_chip_sizing", "Detailed market sizing", sheet)
    if reqs:
        batch(svc, pid, reqs)
    out["indrive-brazil"] = {"atlas": atlas, "sheet": sheet, "n_reqs": len(reqs)}

    return out


# ── 4. inDrive Brazil backup restructure ────────────────────────────────────


def restructure_indrive_brazil_backup(svc) -> dict:
    """Mirror DiDi Brazil: main spine = Rio/Angra/Floripa + econs + prize + close;
    backup = expansion cities + their unit-econ slides after close.
    """
    pid = DECKS["indrive-brazil"]
    pres = svc.presentations().get(presentationId=pid).execute()
    slides = pres["slides"]
    order = [s["objectId"] for s in slides]

    # Target order
    main = [
        "p1",
        "narr2_page",
        "g3eec5122801_0_0",  # overview
        "g3eec5122801_0_106",  # Rio
        "g3eec5122801_0_391",  # Angra
        "g3eec5122801_0_201",  # Floripa
        "g3eec5122801_0_296",  # Rio econ
        "ibAngraEcon",
        "ibFlorEcon",
        "g3eec5122801_0_562",  # THE PRIZE
        "g3ea5e0fb254_4_357",  # how we work
        "g3f139a0b6ec_0_0",  # phased
        "g3ea5e0fb254_4_442",  # ask
        "g3ea5e0fb254_4_270",  # next
    ]
    backup = [
        "idSlide_salvador",
        "idSlide_ilhabela",
        "idSlide_santos",
        "idSlide_vitoria",
        "idSlide_ilhamel",
        "ieSlide_salvador",
        "ieSlide_ilhabela",
        "ieSlide_santos",
        "ieSlide_vitoria",
        "ieSlide_ilhamel",
    ]
    target = main + backup

    # Validate all present
    missing = [x for x in target if x not in order]
    extra = [x for x in order if x not in target]
    if missing or extra:
        return {
            "status": "skip",
            "reason": "slide set mismatch",
            "missing": missing,
            "extra": extra,
            "current": order,
        }

    if order == target:
        return {"status": "already_ordered", "order": target}

    # updateSlidesPosition: move each slide to its target index.
    # Process from back to front so indices stay stable, or use insertionIndex carefully.
    reqs = []
    # Strategy: for each slide that is not already at the right place, move it.
    # Slides API: updateSlidesPosition with slideObjectIds and insertionIndex
    # (index among remaining slides after removing the moved ones).
    # Simplest: rebuild by placing each in order from index 0.
    for i, sid in enumerate(target):
        reqs.append(
            {
                "updateSlidesPosition": {
                    "slideObjectIds": [sid],
                    "insertionIndex": i,
                }
            }
        )
    batch(svc, pid, reqs, chunk=1)  # sequential for position stability

    # verify
    pres2 = svc.presentations().get(presentationId=pid).execute()
    new_order = [s["objectId"] for s in pres2["slides"]]
    return {
        "status": "reordered" if new_order == target else "partial",
        "before": order,
        "after": new_order,
        "target": target,
    }


# ── 5. Manifest sync ────────────────────────────────────────────────────────


PURPOSE_BY_TITLE = [
    ("THE PRIZE", "tam-ladder"),
    ("WHAT ONE BOAT EARNS", "unit-economics"),
    ("Route economics", "unit-economics"),
    ("PHASED", "rollout"),
    ("NEXT STEP", "close"),
    ("How ", "integration"),
    ("HOW WE WORK", "integration"),
    ("joint route", "ask"),
    ("THE ASK", "ask"),
    ("water-mobility opportunity", "market-overview"),
    ("water mobility matters", "why-partner"),
    ("PARTNER PROPOSAL", "why-partner"),
    ("OWN THE EDGE", "cover"),
    ("Own the Edge", "close"),
]


def guess_purpose(title: str, index: int) -> str:
    if index == 1:
        return "cover"
    u = (title or "").upper()
    for needle, purpose in PURPOSE_BY_TITLE:
        if needle.upper() in u:
            return purpose
    # city deep-dives often have city names as titles
    if index <= 3:
        return "why-partner" if index == 2 else "market-overview"
    return "city-deepdive"


def sync_manifest(svc, slug: str) -> dict:
    pid = DECKS[slug]
    pres = svc.presentations().get(presentationId=pid).execute()
    slides_out = []
    for i, s in enumerate(pres["slides"], 1):
        texts = []
        for el in s.get("pageElements") or []:
            t = extract_text(el.get("shape") or {})
            if t:
                texts.append(t.replace("\n", " ").strip())
        title = texts[0] if texts else ""
        # prefer known title patterns
        for t in texts:
            if any(
                k in t.upper()
                for k in (
                    "WHAT ONE BOAT",
                    "THE PRIZE",
                    "ROUTE ECONOMICS",
                    "PHASED",
                    "NEXT STEP",
                    "HOW ",
                    "OWN THE",
                )
            ):
                title = t
                break
        slides_out.append(
            {
                "index": i,
                "slide_object_id": s["objectId"],
                "layout_object_id": (s.get("slideProperties") or {}).get("layoutObjectId"),
                "title": title[:120],
                "purpose": guess_purpose(title, i),
                "allowed_edit_types": ["replace_text", "replace_linked_image"],
                "locked": False,
                "notes": f"Live inventory read back after country-deck standardize 2026-07-20",
            }
        )

    path = ROOT / f"deck-studio/decks/{slug}/slide-manifest.json"
    prev = {}
    if path.exists():
        prev = json.loads(path.read_text(encoding="utf-8"))

    # Spine note for indrive-brazil backup
    if slug == "indrive-brazil":
        spine = (
            "cover, why-partner, market-overview, main city deep-dives (Rio/Angra/Floripa) + "
            "unit-econ, THE PRIZE, integration, rollout, ask, close; BACKUP: expansion cities "
            "(Salvador/Ilhabela/Santos/Vitória/Ilha do Mel) + unit-econ"
        )
    elif slug == "indrive-egypt":
        spine = (
            "cover, why-partner, market-overview, Hurghada/Sharm deep-dives, unit-econ, "
            "THE PRIZE (4-rung non-monotonic SOM>SAM + footnote), integration, rollout, ask, close"
        )
    elif slug == "didi-mexico":
        spine = (
            "cover, why-partner, market-overview, city deep-dives, unit-econ, THE PRIZE "
            "(SOM/SAM/TAM/GMV + platform), integration, rollout, ask, close"
        )
    else:
        spine = prev.get("spine") or "live readback"

    manifest = {
        "deck_key": slug,
        "presentation_id": pid,
        "source": "live_google_slides_full_after_country_deck_standardize_2026-07-20",
        "slide_count": len(slides_out),
        "spine": spine,
        "object_inventory_status": "full_inventory_pulled",
        "slides": slides_out,
        "synced_at": NOW,
    }
    # preserve any extra keys that matter
    for k in ("qa", "economics_binding", "locked_spine_note"):
        if k in prev:
            manifest[k] = prev[k]

    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # light deck.config touch
    cfg_path = ROOT / f"deck-studio/decks/{slug}/deck.config.json"
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["notes"] = (
            f"Live deck synchronized after country-deck standardize 2026-07-20 "
            f"({len(slides_out)} slides)."
        )
        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return {"slug": slug, "slide_count": len(slides_out), "path": str(path.relative_to(ROOT))}


def main() -> int:
    svc = build("slides", "v1", credentials=get_creds(), cache_discovery=False)
    receipt: dict = {"at": NOW, "spec": "GROK-SPEC-country-deck-standardize-2026-07-20.md", "steps": {}}

    print("1/5 Egypt THE PRIZE regen…")
    receipt["steps"]["egypt_prize"] = apply_egypt_prize(svc)
    print("   ", receipt["steps"]["egypt_prize"]["rungs"])

    print("2/5 Econ titles…")
    receipt["steps"]["econ_titles"] = apply_econ_titles(svc)
    for slug, items in receipt["steps"]["econ_titles"].items():
        print(f"   {slug}: {len(items)} titles")

    print("3/5 Link chips…")
    receipt["steps"]["chips"] = apply_chips(svc)
    for slug, info in receipt["steps"]["chips"].items():
        print(f"   {slug}: {info}")

    print("4/5 inDrive Brazil backup restructure…")
    receipt["steps"]["indrive_brazil_backup"] = restructure_indrive_brazil_backup(svc)
    print("   ", receipt["steps"]["indrive_brazil_backup"].get("status"))

    print("5/5 Manifest sync…")
    receipt["steps"]["manifests"] = []
    for slug in ("indrive-egypt", "didi-mexico", "indrive-brazil", "didi-brazil"):
        m = sync_manifest(svc, slug)
        receipt["steps"]["manifests"].append(m)
        print(f"   {slug}: {m['slide_count']} slides → {m['path']}")

    # verify Egypt prize readback
    print("\nVerify Egypt prize…")
    pid = DECKS["indrive-egypt"]
    pres = svc.presentations().get(presentationId=pid).execute()
    slide = next(s for s in pres["slides"] if s["objectId"] == "g3eec5122801_0_562")
    texts = []
    for el in slide.get("pageElements") or []:
        t = extract_text(el.get("shape") or {})
        if t:
            texts.append(f"{el['objectId']}: {t[:100]}")
    receipt["egypt_prize_readback"] = texts
    for t in texts:
        print("  ", t)

    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nReceipt: {RECEIPT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
