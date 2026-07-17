#!/usr/bin/env python3
"""Live Slides re-apply after Angra/Floripa seal + Brazil/Egypt TAM (#292).

Element-scoped text updates only (Slides API). Bind from generated-deck-economics.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[2]
TOKEN_FILE = Path.home() / ".config/google-drive-mcp/tokens.json"
CLIENT_FILE = Path.home() / ".config/google-drive-mcp/gcp-oauth.keys.json"
NOW = datetime.now(timezone.utc).isoformat()

DECKS = {
    "didi-brazil": "1jHxxDgDd5Oki0eO4YoCfHHfC_aS-akGjb4UfXseIEK8",
    "indrive-brazil": "1QImIe6KAee0Eajsokgh9NmH0I29lir4l2LV63e-9OxE",
    "indrive-egypt": "1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk",
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


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_text(oid: str, new_text: str) -> list[dict]:
    if new_text and not new_text.endswith("\n"):
        new_text += "\n"
    return [
        {"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}},
        {"insertText": {"objectId": oid, "insertionIndex": 0, "text": new_text}},
    ]


def money(usd: float) -> str:
    if usd >= 1e9:
        v = usd / 1e9
        s = f"${v:.2f}B" if v < 10 else f"${v:.1f}B"
        return s.replace(".00B", "B")
    return f"${usd / 1e6:.1f}M".replace(".0M", "M") if usd >= 100e6 else f"${usd / 1e6:.1f}M"


def band(lo: float | None, hi: float | None) -> str:
    if lo is None or hi is None:
        return ""
    return f"{money(lo)}–{money(hi)}"


def format_ue(route: dict) -> str:
    ue = route.get("unit_economics") or {}
    opex = ue.get("opex_lines") or {}
    margin_pct = round(float(ue.get("margin") or 0) * 100)
    rev = int(round(float(ue.get("revenue_per_boat_yr") or 0)))
    opex_tot = int(round(float(ue.get("total_run_cost_yr") or 0)))
    ebitda = int(round(float(ue.get("ebitda_per_boat_yr") or 0)))
    pax = int(round(float(ue.get("annual_one_way_pax_per_boat") or 0)))
    fare = float(ue.get("one_way_fare_usd") or 0)
    payback = ue.get("payback_years")
    nm = ue.get("distance_nm")
    energy = int(round(float(opex.get("energy_usd_yr") or 0)))
    crew = int(round(float(opex.get("crew_usd_yr") or 0)))
    marina = int(round(float(opex.get("marina_overhead_usd_yr") or 0)))
    maint = int(round(float(opex.get("maintenance_usd_yr") or 0)))
    ins = int(round(float(opex.get("insurance_usd_yr") or 0)))
    charge = int(round(float(opex.get("charging_berth_usd_yr") or 0)))
    fare_s = f"${fare:.0f}" if fare == int(fare) else f"${fare:.2f}"
    return "\n".join(
        [
            f"{route.get('label')}. {route.get('desc') or ''}".strip(),
            f"Vessel N30 Pioneer II · {nm} nm · one-way fare {fare_s} · ~{pax:,} passengers per boat per year.",
            f"Revenue per boat ${rev:,} · run cost ${opex_tot:,} · EBITDA ${ebitda:,} · margin {margin_pct}% · payback {payback} years.",
            f"Energy ${energy:,} · Crew ${crew:,} · Marina+overhead ${marina:,} · Maintenance ${maint:,} · Insurance ${ins:,} · Charging berth ${charge:,} → total run cost ${opex_tot:,}.",
        ]
    )


def batch(svc, pid: str, reqs: list[dict], chunk: int = 25):
    for i in range(0, len(reqs), chunk):
        part = reqs[i : i + chunk]
        if part:
            svc.presentations().batchUpdate(presentationId=pid, body={"requests": part}).execute()


def by_id(routes: list[dict]) -> dict[str, dict]:
    return {r["route_id"]: r for r in routes if r.get("route_id")}


def apply_didi(svc, gen: dict) -> dict:
    pid = DECKS["didi-brazil"]
    rungs = gen["tam"]["rungs"]
    ct = gen["country_total"]["values"]
    routes = by_id(gen.get("economics_routes") or [])
    angra = routes.get("rn-7ec802385553")
    r3 = routes.get("rn-36dcca92d821")
    r4 = routes.get("rn-7d157e1300da")
    reqs: list[dict] = []

    # S4 market overview
    reqs += replace_text("g3eec5122801_0_6", "7")
    reqs += replace_text("g3eec5122801_0_7", "sourced Brazil corridors (Rio · Angra · Floripa)")
    reqs += replace_text("g3eec5122801_0_10", money(ct["annual_revenue_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_11",
        f"supported annual route revenue · {ct['vessels_supported']} vessels at scale",
    )
    reqs += replace_text(
        "g3eec5122801_0_14",
        "Rio de Janeiro, Angra dos Reis and Florianópolis: DiDi already owns the street layer "
        "in Brazil's coastal cities — the water leg books in the same app. Seven sourced corridors "
        "anchor today's floor.",
    )
    # pool chip was $367M addressable — update to new pool ~$574M
    reqs += replace_text("g3eec5122801_0_18", "$574M")
    reqs += replace_text("g3eec5122801_0_19", "addressable Brazil water-crossing spend (sourced pool)")

    # S6 Angra signature
    reqs += replace_text(
        "g3eec5122801_0_304",
        "Costa Verde flagship: Angra dos Reis ↔ car-free Ilha Grande (Abraão). "
        "Sourced corridor in the Brazil floor — not a hold.",
    )
    angra_list = (
        "▸  Angra dos Reis → Abraão (Ilha Grande)\n"
        "      ~13.0 nm · car-free island access · $30 fare\n"
        "▸  Unit economics (mid)\n"
        "      $235,092 / boat·yr · 65.3% margin · 3.91 yr payback · 2 boats"
    )
    reqs += replace_text("dbP5_s6_sigb", angra_list)
    reqs += replace_text("dbP5_s6_sigh", "SIGNATURE CROSSING — SOURCED")

    # S7 Floripa
    reqs += replace_text(
        "g3f4cafb4749_0_20",
        "North Bay aquaviário corridors from the Santa Catarina EVTE study — "
        "government pre-viability projection (not observed ridership), now in the Brazil floor.",
    )
    floripa_list = (
        "▸  Barreiros → Miramar (R3)\n"
        "      ~5.0 nm · $20 fare · $235,136 / boat·yr · 65.9% · 3.87 yr · 33 boats\n"
        "▸  Beira Mar → Miramar (R4)\n"
        "      ~4.8 nm · $20 fare · $235,136 / boat·yr · 65.9% · 3.87 yr · 51 boats\n"
        "▸  Demand basis\n"
        "      EVTE SIE SC + IDB/BID government pre-viability projection"
    )
    reqs += replace_text("dbP5_s7_sigb", floripa_list)
    reqs += replace_text("dbP5_s7_sigh", "SIGNATURE CROSSINGS — SOURCED (EVTE)")

    # S9 TAM 5-rung
    r0, r1, r2, r3r, r4r = rungs[0], rungs[1], rungs[2], rungs[3], rungs[4]
    reqs += replace_text(
        "g3eec5122801_0_565",
        gen["tam"].get("headline")
        or "Rio, Angra and Florianópolis are the floor — Brazil's water-crossing market runs far higher",
    )
    reqs += replace_text(
        "g3eec5122801_0_567",
        "Read it bottom-up: what our sourced Brazil routes support today is the floor "
        "(Rio + Angra + Floripa, 199 vessels). Above it — the matured network Navier can serve, "
        "the full marine-mobility opportunity, whole-journey value, and DiDi's platform take.",
    )
    reqs += replace_text("g3eec5122801_0_574", money(r0["value_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_575",
        "Supported today — seven sourced Brazil corridors, 199 vessels at scale",
    )
    reqs += replace_text("g3eec5122801_0_578", money(r1["value_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_579",
        f"Matured Brazil network Navier can serve — mid case, {band(r1.get('value_usd_low'), r1.get('value_usd_high'))} range",
    )
    reqs += replace_text("dbP5_r3val", money(r2["value_usd"]))
    reqs += replace_text(
        "dbP5_r3dsc",
        f"Brazil marine-mobility opportunity — total water-transfer spend at full network width "
        f"({band(r2.get('value_usd_low'), r2.get('value_usd_high'))})",
    )
    reqs += replace_text("dbP5_r4val", money(r3r["value_usd"]))
    reqs += replace_text(
        "dbP5_r4dsc",
        f"Whole-journey value across those crossings — door-to-door worth of every trip that includes one "
        f"({band(r3r.get('value_usd_low'), r3r.get('value_usd_high'))})",
    )
    reqs += replace_text("dbP5_r5val", money(r4r["value_usd"]))
    reqs += replace_text(
        "dbP5_r5dsc",
        f"DiDi platform revenue on the Navier network — DiDi's 18% take on that journey value "
        f"({band(r4r.get('value_usd_low'), r4r.get('value_usd_high'))})",
    )

    batch(svc, pid, reqs)
    return {"deck": "didi-brazil", "pid": pid, "n_reqs": len(reqs)}


def apply_indrive_br(svc, gen: dict) -> dict:
    pid = DECKS["indrive-brazil"]
    rungs = gen["tam"]["rungs"]
    ct = gen["country_total"]["values"]
    reqs: list[dict] = []

    # S3 overview
    reqs += replace_text("g3eec5122801_0_4", "Brazil: Rio, Angra dos Reis and Florianópolis")
    reqs += replace_text("g3eec5122801_0_6", "7")
    reqs += replace_text("g3eec5122801_0_7", "sourced corridors across three cities")
    reqs += replace_text("g3eec5122801_0_10", money(ct["annual_revenue_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_11",
        "in annual revenue across the sourced Brazil routes",
    )
    reqs += replace_text("g3eec5122801_0_15", str(ct["vessels_supported"]))
    reqs += replace_text("g3eec5122801_0_16", "vessels at full network maturity")
    reqs += replace_text("g3eec5122801_0_18", "7")
    reqs += replace_text("g3eec5122801_0_19", "routes covered in this review")
    reqs += replace_text(
        "g3eec5122801_0_20",
        "Brazil's coastal cities move enormous numbers of people across water every day, "
        "but on slow, aging diesel ferries. Rio de Janeiro, Angra dos Reis and Florianópolis "
        "now ground a seven-corridor floor — four Rio cross-bay routes, Angra–Abraão, and two "
        "Florianópolis North Bay corridors (government pre-viability projection).\n\n"
        f"3 coastal cities  ·  7 sourced corridors  ·  {money(ct['annual_revenue_usd'])} supported annual route revenue  ·  "
        f"{ct['vessels_supported']} vessels supported at scale",
    )

    # S5 Angra
    reqs += replace_text(
        "g3eec5122801_0_394",
        "Angra dos Reis is the gateway to car-free Ilha Grande and the Costa Verde islands. "
        "The flagship Angra → Abraão corridor is now sourced in the Brazil floor "
        "($30 fare · ~13 nm · mid $235,092 / boat·yr · 65.3% · 3.91 yr · 2 boats).",
    )

    # S6 Floripa
    reqs += replace_text(
        "g3eec5122801_0_206",
        "North Bay R3 (Barreiros→Miramar) and R4 (Beira Mar→Miramar) from the Santa Catarina EVTE study — "
        "government pre-viability projection, now in the Brazil floor at $20 fare.",
    )
    reqs += replace_text(
        "g3eec5122801_0_209",
        "▸  Barreiros → Miramar (R3)\n"
        "      ~5.0 nm · $20 · $235,136 / boat·yr · 33 boats\n"
        "▸  Beira Mar → Miramar (R4)\n"
        "      ~4.8 nm · $20 · $235,136 / boat·yr · 51 boats\n"
        "▸  Basis\n"
        "      EVTE government pre-viability projection (not observed ridership)",
    )

    # S8 TAM 4-rung
    r0, r1, r2, r3 = rungs[0], rungs[1], rungs[2], rungs[3]
    reqs += replace_text(
        "g3eec5122801_0_565",
        gen["tam"].get("headline")
        or "Rio, Angra and Florianópolis are the floor — Brazil's water-crossing market runs far higher",
    )
    reqs += replace_text(
        "g3eec5122801_0_567",
        "Seven sourced Brazil corridors are today's floor. Above them sits the full Brazilian "
        "water-crossing opportunity — the matured network, the marine-mobility market, and the "
        "whole-journey value it unlocks. (No platform-take rung for inDrive.)",
    )
    reqs += replace_text("g3eec5122801_0_570", money(r0["value_usd"]))
    reqs += replace_text("g3eec5122801_0_571", "What our sourced Brazil routes support today")
    reqs += replace_text("g3eec5122801_0_574", money(r1["value_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_575",
        f"Matured Brazil network Navier can serve ({band(r1.get('value_usd_low'), r1.get('value_usd_high'))})",
    )
    reqs += replace_text("g3eec5122801_0_578", money(r2["value_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_579",
        f"Brazil marine-mobility opportunity ({band(r2.get('value_usd_low'), r2.get('value_usd_high'))})",
    )
    reqs += replace_text("g3eec5122801_0_582", money(r3["value_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_583",
        f"Whole-journey value across those crossings ({band(r3.get('value_usd_low'), r3.get('value_usd_high'))})",
    )

    batch(svc, pid, reqs)
    return {"deck": "indrive-brazil", "pid": pid, "n_reqs": len(reqs)}


def apply_egypt(svc, gen: dict) -> dict:
    pid = DECKS["indrive-egypt"]
    rungs = gen["tam"]["rungs"]
    reqs: list[dict] = []
    headline = gen["tam"].get("headline") or (
        "Two boat-only routes are the floor — the Red Sea, Nile and Alexandria market runs far higher"
    )
    r0, r1, r2, r3 = rungs[0], rungs[1], rungs[2], rungs[3]
    reqs += replace_text("g3eec5122801_0_563", headline)
    reqs += replace_text(
        "g3eec5122801_0_567",
        "The two boat-only routes are today's floor. Above them — Navier's matured Egypt network, "
        "the Egypt marine-mobility opportunity, and whole-journey value (width template on). "
        "No platform-take rung for inDrive.",
    )
    reqs += replace_text("g3eec5122801_0_570", money(r0["value_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_571",
        "Two boat-only routes we can size today (captive pool floor)",
    )
    reqs += replace_text("g3eec5122801_0_574", money(r1["value_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_575",
        f"Matured Egypt network Navier can serve ({band(r1.get('value_usd_low'), r1.get('value_usd_high'))})",
    )
    # third rung was "Context" — repurpose to marine TAM
    reqs += replace_text("g3eec5122801_0_578", money(r2["value_usd"]))
    reqs += replace_text(
        "g3eec5122801_0_579",
        f"Egypt marine-mobility opportunity ({band(r2.get('value_usd_low'), r2.get('value_usd_high'))})",
    )
    # need a 4th rung display — use body if no 4th value chip; add note to 567 already
    # If only 3 chips, append journey GMV into body note on 567 (done) and put journey on r3 if we find another object
    # Check: objects 582/583 may not exist on egypt — append journey into 579 chain by extending 567
    reqs += replace_text(
        "g3eec5122801_0_567",
        "The two boat-only routes are today's floor. "
        f"Above them: matured Egypt network {money(r1['value_usd'])}, "
        f"marine-mobility opportunity {money(r2['value_usd'])}, "
        f"and whole-journey value {money(r3['value_usd'])} "
        f"({band(r3.get('value_usd_low'), r3.get('value_usd_high'))}). "
        "Width template on. No platform-take rung for inDrive.",
    )

    batch(svc, pid, reqs)
    return {"deck": "indrive-egypt", "pid": pid, "n_reqs": len(reqs)}


def main() -> int:
    svc = build("slides", "v1", credentials=get_creds(), cache_discovery=False)
    results = []
    didi = load(ROOT / "deck-studio/decks/didi-brazil/generated-deck-economics.json")
    indrive = load(ROOT / "deck-studio/decks/indrive-brazil/generated-deck-economics.json")
    egypt = load(ROOT / "deck-studio/decks/indrive-egypt/generated-deck-economics.json")
    results.append(apply_didi(svc, didi))
    results.append(apply_indrive_br(svc, indrive))
    results.append(apply_egypt(svc, egypt))
    receipt = {"at": NOW, "results": results, "spec": "handoff/finance/GROK-SPEC-brazil-egypt-tam-2026-07-17.md"}
    write(
        ROOT
        / "handoff/partner-map-model/brazil-tam-2026-07-17"
        / "LIVE-REAPPLY-SEALED-TAM-2026-07-17.json",
        receipt,
    )
    print(json.dumps(receipt, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
