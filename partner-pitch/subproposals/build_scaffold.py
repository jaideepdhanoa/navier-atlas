#!/usr/bin/env python3
"""
Sub-proposal phase + vessel-sizing scaffold generator.
Deterministic. Reads finance/model/corridors.json (real corridors) and emits,
per partner market, a journeys_unlocked + phases scaffold with:
  - range-gated vessel per leg (Grab methodology)
  - Prove / Scale / Mature phase bucketing
  - grounded per-phase fleet sizing
  - featured_routes referencing REAL node_ids; route_id LEFT NULL for Grok to bind
  - model_link = partner economics sheet URL (economics_url binding)
NO narrative prose is invented here; prose fields are emitted empty for Tasklet to author.
"""
import json, os, re

BASE = "/tasklet/agent/home/navier"
corr = json.load(open(f"{BASE}/finance/model/corridors.json"))
markets = corr["markets"]
econ_map = json.load(open("/tmp/subprop/economics_url_map.json"))

# ---- range gate (Grab vessel methodology) ----
def gate(d):
    d = d or 0
    if d <= 70:  return ("Pioneer II", "solid", "now")
    if d <= 150: return ("Quanta-LR", "amber-dashed", "roadmap")
    return ("Quanta-LR", "amber-dashed", "roadmap-review")  # >150nm: flag for review

def norm_vessel(v):
    if not v: return None
    s = v.strip().lower().replace("_","-").replace(" ","-")
    if s.startswith("pioneer"): return "Pioneer II"
    if s.startswith("quanta"):  return "Quanta-LR"
    if s.startswith("n35") or "shuttle" in s: return "N35 Shuttle"
    return v

# grounded fleet sizing per phase by tier (model reconciles final; flagged)
TIER_FLEET = {
    "Anchor":  {"prove":3, "scale":8, "mature":6},
    "A":       {"prove":2, "scale":5, "mature":4},
    "B":       {"prove":2, "scale":3, "mature":3},
    "roll-up": {"prove":2, "scale":3, "mature":2},
}

def slug_market(k):  # bolt-greece -> greece
    return k.split("-",1)[1] if "-" in k else k

def build_market(key, mdef):
    partner = mdef.get("partner")
    tier = mdef.get("_tier","B")
    cors = mdef.get("corridors",[])
    # re-gate every corridor
    legs=[]
    regate_fixed=0
    for co in cors:
        d = co.get("distance_nm") or 0
        plat, render, status = gate(d)
        orig = norm_vessel(co.get("vessel"))
        if orig != plat:
            regate_fixed += 1
        legs.append({
            "from": co.get("from"), "to": co.get("to"),
            "from_node_id": co.get("from_node_id"), "to_node_id": co.get("to_node_id"),
            "distance_nm": d, "archetype": co.get("archetype"),
            "country": co.get("country"),
            "fare_usd_pax": (co.get("L3_locals") or {}).get("comparable_fare_usd_pax"),
            "platform": plat, "render": render, "status": status,
            "route_id": None,  # GROK binds during seal (null beats confidently-wrong)
            "_regated_from": orig if orig!=plat else None,
        })
    # sort by distance for bucketing
    legs_sorted = sorted(legs, key=lambda x: x["distance_nm"])
    pioneer = [l for l in legs_sorted if l["platform"]=="Pioneer II"]
    regional = [l for l in legs_sorted if l["platform"]=="Quanta-LR"]
    fleet = TIER_FLEET.get(tier, TIER_FLEET["B"])
    model_link = econ_map.get(partner)

    def feat(l):
        return {
            "from_label": l["from"], "to_label": l["to"],
            "from_node_id": l["from_node_id"], "to_node_id": l["to_node_id"],
            "distance_nm": l["distance_nm"], "platform": l["platform"],
            "render": l["render"],
            "route_id": None, "model_link": model_link,
        }

    phases=[]
    # Phase 1 Prove: 2-3 shortest pioneer legs on the anchor
    p1 = pioneer[:3]
    if p1:
        phases.append({"n":1,"label":f"Phase 1 — Prove ({p1[0]['from']} anchor, Pioneer II)",
            "boats":fleet["prove"],"cities":sorted({l['from_node_id'] for l in p1 if l['from_node_id']}|{l['to_node_id'] for l in p1 if l['to_node_id']}),
            "route_scope":"intra","timeline":"2026 H2","vessel":"N30 Pioneer II (8 pax, commercial now)",
            "narrative":"", "rationale":"",
            "featured_routes":[feat(l) for l in p1],
            "use_cases":[], "fleet_confidence":"grounded" if tier in ("Anchor","A") else "med"})
    # Phase 2 Scale: remaining pioneer legs
    p2 = pioneer[3:]
    if p2:
        phases.append({"n":2,"label":"Phase 2 — Scale the Pioneer II network (N30 + N35 Shuttle on dense legs)",
            "boats":fleet["scale"],"cities":sorted({l['from_node_id'] for l in p2 if l['from_node_id']}|{l['to_node_id'] for l in p2 if l['to_node_id']}),
            "route_scope":"intra","timeline":"2027","vessel":"N30 Pioneer II + N35 Shuttle (12–15 pax, 2027) on dense legs",
            "narrative":"", "rationale":"",
            "featured_routes":[feat(l) for l in p2[:6]],
            "use_cases":[], "fleet_confidence":"med"})
    # Phase 3 Mature/Regional
    if regional:
        phases.append({"n":len(phases)+1,"label":"Phase 3 — Regional reach (Quanta-LR, 75–150nm) + mature in-app capture",
            "boats":fleet["mature"],"cities":sorted({l['from_node_id'] for l in regional if l['from_node_id']}|{l['to_node_id'] for l in regional if l['to_node_id']}),
            "route_scope":"inter","timeline":"H2 2026+ (Quanta-LR roadmap)","vessel":"N35-led mix; Quanta-LR on 75–150nm regional legs",
            "narrative":"", "rationale":"",
            "featured_routes":[feat(l) for l in regional[:6]],
            "use_cases":[], "fleet_confidence":"roadmap"})
    else:
        phases.append({"n":len(phases)+1,"label":"Phase 3 — Mature: induced demand + default-operator capture + in-app monetization",
            "boats":fleet["mature"],"cities":sorted({l['from_node_id'] for l in pioneer if l['from_node_id']}),
            "route_scope":"intra","timeline":"Year 4+","vessel":"N35-led mix",
            "narrative":"", "rationale":"",
            "featured_routes":[], "use_cases":[], "fleet_confidence":"med"})

    # journeys_unlocked: top representative legs (mix archetypes)
    journeys=[]
    seen=set()
    for l in legs_sorted:
        a=l["archetype"]
        if a in seen and len(journeys)>=4: continue
        seen.add(a)
        journeys.append({"from":l["from"],"to":l["to"],"today":"","with_navier":"",
            "distance_nm":l["distance_nm"],"platform":l["platform"],"archetype":a,
            "from_node_id":l["from_node_id"],"to_node_id":l["to_node_id"],"route_id":None})
        if len(journeys)>=6: break

    return {
        "id": slug_market(key), "market_key": key, "partner": partner,
        "label": mdef.get("label"), "region": mdef.get("region"), "tier": tier,
        "anchor_cities": sorted({l['from_node_id'] for l in legs if l['from_node_id']} | {l['to_node_id'] for l in legs if l['to_node_id']}),
        "capture_rate": mdef.get("capture_rate"),
        "corridor_count": len(cors), "regate_fixed": regate_fixed,
        "regional_leg_count": len(regional),
        "vessel_sizing": {
            "headline":"Right vessel for every leg — corridor range picks the hull.",
            "classes":[
                {"class":"N30 Pioneer II","pax":8,"range_nm":70,"status":"commercial now","role":"Capillary corridors ≤ 70nm. Workhorse of Prove + Scale.","render":"solid"},
                {"class":"N35 Shuttle","pax":"12–15","range_nm":70,"status":"2027","role":"Doubles throughput per hull on dense corridors; ~halves payback.","render":"solid"},
                {"class":"Quanta-LR Hybrid","pax":"12–15","range_nm":700,"status":"H2 2026+","role":"Regional legs 75–150nm beyond Pioneer range.","render":"amber-dashed"},
            ],
            "range_gate_note":"≤ 70nm → Pioneer II (now). 75–150nm → Quanta-LR (roadmap). Long legs never faked on a 70nm boat.",
        },
        # prose fields for Tasklet to author:
        "summary":"", "hero":{"title":"","subtitle":"","what_we_do_together":""},
        "why_now":"", "multimodal_fit":"", "partner_context":"", "why_navier_now":"",
        "differentiation":"", "proof_points":[], "objections":[],
        "the_ask":"", "close":"", "end_state":"",
        "journeys_unlocked": journeys,
        "phases": phases,
    }

out={}
regate_report={}
for k,v in markets.items():
    if not (k.startswith("bolt-") or k.startswith("yango-")): continue
    m=build_market(k,v)
    out[k]=m
    regate_report[k]={"corridors":m["corridor_count"],"regated_fixed":m["regate_fixed"],"regional_legs":m["regional_leg_count"]}

os.makedirs("/tmp/subprop/out", exist_ok=True)
json.dump(out, open("/tmp/subprop/out/scaffold-all.json","w"), indent=1, ensure_ascii=False)
json.dump(regate_report, open("/tmp/subprop/out/regate-report.json","w"), indent=1, ensure_ascii=False)
print("markets scaffolded:", len(out))
print("\nRE-GATE corrections (legs whose vessel violated the range rule):")
tot=0
for k,r in sorted(regate_report.items()):
    tot+=r["regated_fixed"]
    flag=" <-- FIXES" if r["regated_fixed"] else ""
    print(f"  {k:22} corr={r['corridors']:3} regated={r['regated_fixed']:2} regional={r['regional_legs']:2}{flag}")
print("TOTAL vessel re-gate fixes:", tot)
