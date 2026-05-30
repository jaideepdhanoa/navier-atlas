#!/usr/bin/env python3
"""
Entity manifest + referential-integrity linter.
READ-ONLY: reads all data layers, writes ONE manifest + a lint report.
Does NOT modify any source file. Safe to run anytime; intended for seal/build pre-flight.

Catches the recurring bug class: content-layer ids that don't resolve to graph nodes,
routes with dangling endpoints, partner refs to unknown cities.
"""
import json, glob, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # .../navier
def J(p):
    try:
        with open(os.path.join(ROOT,p)) as f: return json.load(f)
    except Exception as e: return {"__err__":str(e)}

def node_id_set():
    d = J("app/data-spine/output/nodes.json")
    feats = d.get("features", d.get("nodes", [])) if isinstance(d,dict) else d
    ids=set()
    for f in feats:
        nid = f.get("id") or (f.get("properties",{}) or {}).get("id")
        if nid: ids.add(nid)
    return ids, len(feats)

def edge_list():
    d = J("app/data-spine/output/edges.json")
    e = d.get("edges", d.get("features", d)) if isinstance(d,dict) else d
    return list(e.values()) if isinstance(e,dict) else (e if isinstance(e,list) else [])

def main():
    report = {"generated": datetime.datetime.now(datetime.timezone.utc).isoformat(), "errors": [], "warnings": [], "stats": {}}
    try: gaps = json.load(open(os.path.join(ROOT,"atlas-external/integrity/known-gaps.json")))
    except Exception: gaps = {}
    allow_ep = {g["id"] for g in gaps.get("unresolved_edge_endpoints",[])}
    allow_brief = {g["city_id"] for g in gaps.get("dangling_briefs",[])}
    nodes, nfeat = node_id_set()
    edges = edge_list()
    report["stats"]["node_features"] = nfeat
    report["stats"]["edges"] = len(edges)

    # 1. edge endpoint integrity
    dangling=[]
    for e in edges:
        for k in ("from_node_id","to_node_id"):
            v=e.get(k)
            if v and v not in nodes: dangling.append({"edge":e.get("id"),"missing":k,"value":v})
    new_d=[x for x in dangling if x["value"] not in allow_ep]
    known_d=[x for x in dangling if x["value"] in allow_ep]
    if new_d:
        report["errors"].append({"check":"edge_endpoints_resolve","fail_count":len(new_d),"sample":new_d[:8]})
    if known_d:
        report["warnings"].append({"check":"edge_endpoints_resolve_KNOWN_GAP","count":len(known_d),"ids":sorted({x["value"] for x in known_d})})

    # 2. brief -> node integrity (the recurring bug)
    briefs=glob.glob(os.path.join(ROOT,"partner-pitch/city_briefs/*.json"))
    brief_index={}
    for b in briefs:
        try: d=json.load(open(b))
        except Exception as ex:
            report["errors"].append({"check":"brief_parses","file":os.path.basename(b),"err":str(ex)}); continue
        cid=d.get("city_id"); brief_index[os.path.basename(b)]=cid
    report["stats"]["briefs"]=len(briefs)
    dangling_briefs=[{"file":f,"city_id":c} for f,c in brief_index.items() if c and c not in nodes]
    new_b=[x for x in dangling_briefs if x["city_id"] not in allow_brief]
    known_b=[x for x in dangling_briefs if x["city_id"] in allow_brief]
    if new_b:
        report["errors"].append({"check":"brief_city_id_resolves_to_node","fail_count":len(new_b),"items":new_b})
    if known_b:
        report["warnings"].append({"check":"brief_city_id_KNOWN_GAP","count":len(known_b),"items":known_b})

    # 3. partner -> city refs (phases may name city_ids)
    partners=glob.glob(os.path.join(ROOT,"partner-pitch/partners/*.json"))
    report["stats"]["partners"]=len(partners)
    bad_partner_refs=[]
    for p in partners:
        try: d=json.load(open(p))
        except Exception as ex:
            report["errors"].append({"check":"partner_parses","file":os.path.basename(p),"err":str(ex)}); continue
        # scan any *_city_id / city_id fields recursively
        def walk(o,path=""):
            if isinstance(o,dict):
                for k,v in o.items():
                    if k.endswith("city_id") and isinstance(v,str) and v and v not in nodes:
                        bad_partner_refs.append({"partner":os.path.basename(p),"path":path+"/"+k,"value":v})
                    walk(v,path+"/"+k)
            elif isinstance(o,list):
                for i,x in enumerate(o): walk(x,path+f"[{i}]")
        walk(d)
    if bad_partner_refs:
        report["warnings"].append({"check":"partner_city_id_resolves","count":len(bad_partner_refs),"items":bad_partner_refs[:12]})

    # 4. coverage: anchor nodes without briefs (informational)
    brief_cids={c for c in brief_index.values() if c}
    report["stats"]["briefs_resolving"]=len(brief_cids & nodes)
    report["stats"]["nodes_without_brief"]=len(nodes - brief_cids)

    out=os.path.join(ROOT,"atlas-external/integrity/lint-report.json")
    json.dump(report,open(out,"w"),indent=2)
    nerr=sum(x.get("fail_count",1) for x in report["errors"]); nwarn=len(report["warnings"])
    print(f"INTEGRITY: {len(report['errors'])} error-checks, {nwarn} warning-checks")
    for e in report["errors"]: print("  ERROR:", e.get("check"), e.get("fail_count",""))
    for w in report["warnings"]: print("  WARN :", w.get("check"), w.get("count",""))
    print("report ->", out)
    sys.exit(1 if report["errors"] else 0)

if __name__=="__main__": main()
