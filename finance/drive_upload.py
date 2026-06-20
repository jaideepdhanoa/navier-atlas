#!/usr/bin/env python3
"""
In-place Google Sheet refresh via Drive multipart upload.

Uses OAuth tokens from ~/.config/google-drive-mcp/ (same creds as the Grok
google-drive MCP). Replaces an existing spreadsheet ID with a local .xlsx,
converting to native Google Sheets so formulas stay live. Preserves the file ID
so economics_url_map.json / TAM-ladder links do not break.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

DEFAULT_CRED_DIR = Path.home() / ".config" / "google-drive-mcp"
DEFAULT_TOKEN_FILE = DEFAULT_CRED_DIR / "tokens.json"
DEFAULT_CLIENT_FILE = DEFAULT_CRED_DIR / "gcp-oauth.keys.json"

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
SHEET_MIME = "application/vnd.google-apps.spreadsheet"


def _load_credentials(
    token_file: Path = DEFAULT_TOKEN_FILE,
    client_file: Path = DEFAULT_CLIENT_FILE,
) -> Credentials:
    if not token_file.is_file():
        raise FileNotFoundError(f"missing OAuth tokens: {token_file}")
    data = json.loads(token_file.read_text())
    client = json.loads(client_file.read_text()) if client_file.is_file() else {}
    installed = client.get("installed") or client.get("web") or {}
    creds = Credentials(
        token=data.get("access_token"),
        refresh_token=data.get("refresh_token"),
        token_uri=installed.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=installed.get("client_id"),
        client_secret=installed.get("client_secret"),
        scopes=data.get("scope", "").split() or None,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        data["access_token"] = creds.token
        if creds.expiry:
            data["expiry_date"] = int(creds.expiry.timestamp() * 1000)
        token_file.write_text(json.dumps(data, indent=2))
    return creds


def _drive_service(creds: Optional[Credentials] = None):
    return build("drive", "v3", credentials=creds or _load_credentials(), cache_discovery=False)


def get_file_name(file_id: str, service=None) -> str:
    svc = service or _drive_service()
    meta = svc.files().get(fileId=file_id, fields="name").execute()
    return meta["name"]


def replace_spreadsheet(
    local_path: str,
    sheet_id: str,
    *,
    preserve_name: bool = True,
    dry_run: bool = False,
) -> dict:
    """Upload .xlsx in-place over an existing Google Sheet ID."""
    local = Path(local_path)
    if not local.is_file():
        raise FileNotFoundError(local_path)

    if dry_run:
        return {
            "status": "dry-run",
            "sheet_id": sheet_id,
            "local": str(local),
            "action": "fileIdToReplace+uploadMimeType=spreadsheet",
        }

    svc = _drive_service()
    prior_name = get_file_name(sheet_id, svc) if preserve_name else None

    media = MediaFileUpload(str(local), mimetype=XLSX_MIME, resumable=True)
    updated = (
        svc.files()
        .update(
            fileId=sheet_id,
            body={"mimeType": SHEET_MIME},
            media_body=media,
            fields="id,name,mimeType,webViewLink",
            supportsAllDrives=True,
        )
        .execute()
    )

    # Drive may rename to the local basename; restore the prior display name.
    if preserve_name and prior_name and updated.get("name") != prior_name:
        svc.files().update(fileId=sheet_id, body={"name": prior_name}, fields="name").execute()
        updated["name"] = prior_name

    return {
        "status": "uploaded",
        "sheet_id": sheet_id,
        "local": str(local),
        "name": updated.get("name"),
        "mimeType": updated.get("mimeType"),
        "webViewLink": updated.get("webViewLink"),
    }


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("local_path")
    ap.add_argument("sheet_id")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    print(json.dumps(replace_spreadsheet(args.local_path, args.sheet_id, dry_run=args.dry_run), indent=2))