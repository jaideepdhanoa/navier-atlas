import argparse, json, os, sys, datetime
from pathlib import Path
from jsonschema import Draft202012Validator

FORBIDDEN_REQUEST_KEYS = {'replaceAllShapesWithImage', 'deleteObjectThenCreateDeck', 'fullDeckReplace', 'pptxRoundTrip'}

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f: return json.load(f)

def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f: json.dump(obj, f, indent=2, ensure_ascii=False); f.write('\n')

def deck_dir(root, deck): return Path(root) / 'decks' / deck

def validate_json(schema_path, data_path):
    schema=load_json(schema_path); data=load_json(data_path)
    v=Draft202012Validator(schema)
    errs=sorted(v.iter_errors(data), key=lambda e: e.path)
    if errs:
        return [f"{data_path}: {'/'.join(map(str,e.path))}: {e.message}" for e in errs]
    return []

def cmd_validate(args):
    root=Path(args.root); errors=[]
    schemas=root/'schemas'
    for d in sorted((root/'decks').iterdir()):
        if not d.is_dir(): continue
        errors += validate_json(schemas/'deck-config.schema.json', d/'deck.config.json')
        errors += validate_json(schemas/'slide-manifest.schema.json', d/'slide-manifest.json')
        errors += validate_json(schemas/'image-manifest.schema.json', d/'image-manifest.json')
        for r in (d/'qa-receipts').glob('*.json'):
            errors += validate_json(schemas/'qa-receipt.schema.json', r)
    for p in (root/'examples'/'edit-plans').glob('*.json'):
        errors += validate_json(schemas/'edit-plan.schema.json', p)
    if errors:
        print('\n'.join(errors), file=sys.stderr); return 1
    print('Deck Studio validation passed.')
    return 0

def load_google_credentials(scopes=None):
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from dotenv import load_dotenv
    except Exception as e:
        raise SystemExit(f'Missing Google dependencies: {e}')
    load_dotenv()
    default_cred_dir = Path.home() / '.config' / 'google-drive-mcp'
    token_path = Path(os.getenv('GOOGLE_TOKEN_PATH') or default_cred_dir / 'tokens.json')
    client_path = Path(os.getenv('GOOGLE_CLIENT_PATH') or default_cred_dir / 'gcp-oauth.keys.json')
    if not token_path.is_file():
        raise SystemExit(f'Set GOOGLE_TOKEN_PATH to an OAuth token JSON with Slides scope. Missing: {token_path}')
    data = load_json(token_path)
    client = load_json(client_path) if client_path.is_file() else {}
    installed = client.get('installed') or client.get('web') or {}
    token_scopes = data.get('scope', '').split() if data.get('scope') else None
    creds = Credentials(
        token=data.get('access_token'),
        refresh_token=data.get('refresh_token'),
        token_uri=installed.get('token_uri', 'https://oauth2.googleapis.com/token'),
        client_id=installed.get('client_id') or data.get('client_id'),
        client_secret=installed.get('client_secret') or data.get('client_secret'),
        scopes=scopes or token_scopes,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        data['access_token'] = creds.token
        if creds.expiry:
            data['expiry_date'] = int(creds.expiry.timestamp() * 1000)
        write_json(token_path, data)
    return creds

def get_slides_service():
    try:
        from googleapiclient.discovery import build
    except Exception as e:
        raise SystemExit(f'Missing Google dependencies: {e}')
    scopes = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive.readonly']
    return build('slides', 'v1', credentials=load_google_credentials(scopes), cache_discovery=False)

def get_drive_service():
    try:
        from googleapiclient.discovery import build
    except Exception as e:
        raise SystemExit(f'Missing Google dependencies: {e}')
    scopes = ['https://www.googleapis.com/auth/drive']
    return build('drive', 'v3', credentials=load_google_credentials(scopes), cache_discovery=False)

def cmd_pull(args):
    root=Path(args.root); cfg=load_json(deck_dir(root,args.deck)/'deck.config.json')
    service=get_slides_service()
    pres=service.presentations().get(presentationId=cfg['deck_id']).execute()
    if args.mode == 'raw':
        out=args.out or str(deck_dir(root,args.deck)/'live-pull-full.json')
        write_json(out, pres); print(out); return 0
    slides=[]
    for i,slide in enumerate(pres.get('slides',[]),1):
        slides.append({'index':i,'slide_object_id':slide.get('objectId'), 'layout_object_id':slide.get('slideProperties',{}).get('layoutObjectId'), 'title':None, 'purpose':'pulled from live deck', 'locked':False, 'allowed_edit_types':['text_replace','image_replace','speaker_notes_update','layout_preserving_insert'], 'known_objects':([] if args.mode=='summary' else [{'object_id':e.get('objectId'), 'kind': next((k for k in ['shape','image','table','line','video','sheetsChart','wordArt','elementGroup'] if k in e), 'unknown'), 'transform': e.get('transform'), 'size': e.get('size')} for e in slide.get('pageElements',[])]), 'notes':'updated by pull'})
    manifest={'deck_key':args.deck,'presentation_id':cfg['deck_id'],'source':'live_google_slides_'+args.mode,'slide_count':len(slides),'page_size':pres.get('pageSize',{}),'object_inventory_status':('summary_only' if args.mode=='summary' else 'full_inventory_pulled'),'slides':slides,'pull_command':f'python -m deck_studio pull --root {args.root} --deck {args.deck} --mode full','qa_notes':['Generated by deck_studio pull.']}
    out=args.out or str(deck_dir(root,args.deck)/'slide-manifest.json')
    write_json(out, manifest); print(out); return 0

def plan_has_forbidden(plan):
    text=json.dumps(plan)
    bad=[k for k in FORBIDDEN_REQUEST_KEYS if k in text]
    safety=plan.get('safety',{})
    for key in ['no_pptx_roundtrip','no_full_deck_replace','preserve_object_ids','human_review_required_for_external_send']:
        if safety.get(key) is not True: bad.append(f'safety.{key}')
    return bad

def cmd_plan(args):
    cfg=load_json(deck_dir(args.root,args.deck)/'deck.config.json')
    request=Path(args.request).read_text(encoding='utf-8') if args.request else 'No request supplied.'
    plan={'deck_key':args.deck,'presentation_id':cfg['deck_id'],'mode':'slides_api_batch_update','request_summary':request[:500], 'safety':{'no_pptx_roundtrip':True,'no_full_deck_replace':True,'preserve_object_ids':True,'human_review_required_for_external_send':True}, 'operations':[], 'qa_gates':['schema_validation','no_full_replace','object_id_check','brand_lint','claim_source_check','render_export'], 'created_at':datetime.datetime.utcnow().isoformat()+'Z'}
    out=args.out or f'out/{args.deck}-edit-plan.json'; write_json(out, plan); print(out); return 0

def cmd_apply(args):
    plan=load_json(args.plan); bad=plan_has_forbidden(plan)
    if bad: raise SystemExit('Refusing unsafe plan: '+', '.join(bad))
    # Validate against known slide ids.
    manifest=load_json(deck_dir(args.root,args.deck)/'slide-manifest.json')
    known={s['slide_object_id'] for s in manifest['slides']}
    for op in plan.get('operations',[]):
        if op['slide_object_id'] not in known:
            raise SystemExit(f"Unknown slide_object_id {op['slide_object_id']}; pull full manifest first.")
    if args.dry_run or not plan.get('operations'):
        print('Plan passed safety checks; no operations applied.' if not plan.get('operations') else 'Dry run passed.')
        return 0
    service=get_slides_service()
    requests=[op['google_slides_request'] for op in plan['operations']]
    service.presentations().batchUpdate(presentationId=plan['presentation_id'], body={'requests':requests}).execute()
    print(f"Applied {len(requests)} Slides API requests.")
    return 0

def cmd_qa(args):
    root=Path(args.root); d=deck_dir(root,args.deck)
    cfg=load_json(d/'deck.config.json'); manifest=load_json(d/'slide-manifest.json'); img=load_json(d/'image-manifest.json')
    checks=[]
    checks.append({'name':'editing_mode','status':'pass' if cfg.get('editing_mode')=='slides_api_only' else 'fail','details':cfg.get('editing_mode','')})
    checks.append({'name':'slide_count_positive','status':'pass' if manifest.get('slide_count',0)==len(manifest.get('slides',[])) else 'fail','details':f"declared={manifest.get('slide_count')} actual={len(manifest.get('slides',[]))}"})
    checks.append({'name':'object_inventory','status':'warning' if manifest.get('object_inventory_status')=='summary_only' else 'pass','details':manifest.get('object_inventory_status','')})
    bad_images=[i['image_key'] for i in img.get('images',[]) if not i.get('provenance_required')]
    checks.append({'name':'image_provenance_required','status':'pass' if not bad_images else 'fail','details':', '.join(bad_images)})
    status='fail' if any(c['status']=='fail' for c in checks) else ('pass_with_flags' if any(c['status']=='warning' for c in checks) else 'pass')
    receipt={'deck_key':args.deck,'status':status,'generated_at':datetime.datetime.utcnow().isoformat()+'Z','checks':checks,'artifacts':[str(d/'deck.config.json'), str(d/'slide-manifest.json'), str(d/'image-manifest.json')]}
    out=args.receipt or str(d/'qa-receipts'/'latest-local-qa.json')
    write_json(out, receipt); print(json.dumps(receipt, indent=2)); return 0 if status!='fail' else 1

def cmd_image_plan(args):
    cfg=load_json(deck_dir(args.root,args.deck)/'deck.config.json')
    job={'deck_key':args.deck,'presentation_id':cfg['deck_id'],'slide_object_id':args.slide_object_id,'kind':'n30_composite','inputs':{'background':None,'vessel':'assets/n30/n30.png','mask':None},'output':None,'provenance':{'provider':None,'prompt':None,'seed':None},'notes':'Fill inputs, run builders/images/n30_composite.py, then create an edit plan to replace target image.'}
    out=args.out or f'out/{args.deck}-image-job.json'; write_json(out, job); print(out); return 0

def main():
    ap=argparse.ArgumentParser(prog='deck_studio')
    sub=ap.add_subparsers(dest='cmd', required=True)
    p=sub.add_parser('validate'); p.add_argument('--root', default='.'); p.set_defaults(func=cmd_validate)
    p=sub.add_parser('pull'); p.add_argument('--root', default='.'); p.add_argument('--deck', required=True); p.add_argument('--mode', choices=['summary','full','raw'], default='summary'); p.add_argument('--out'); p.set_defaults(func=cmd_pull)
    p=sub.add_parser('plan'); p.add_argument('--root', default='.'); p.add_argument('--deck', required=True); p.add_argument('--request'); p.add_argument('--out'); p.set_defaults(func=cmd_plan)
    p=sub.add_parser('apply'); p.add_argument('--root', default='.'); p.add_argument('--deck', required=True); p.add_argument('--plan', required=True); p.add_argument('--dry-run', action='store_true'); p.set_defaults(func=cmd_apply)
    p=sub.add_parser('qa'); p.add_argument('--root', default='.'); p.add_argument('--deck', required=True); p.add_argument('--receipt'); p.set_defaults(func=cmd_qa)
    p=sub.add_parser('image-plan'); p.add_argument('--root', default='.'); p.add_argument('--deck', required=True); p.add_argument('--slide-object-id', required=True); p.add_argument('--out'); p.set_defaults(func=cmd_image_plan)
    args=ap.parse_args(); sys.exit(args.func(args))
