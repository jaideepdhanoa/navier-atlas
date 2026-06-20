#!/usr/bin/env bash
# One-time Google Drive MCP setup for Grok sheet-upload lane (Option B).
set -euo pipefail

CRED_DIR="${HOME}/.config/google-drive-mcp"
CRED_FILE="${CRED_DIR}/gcp-oauth.keys.json"
TOKEN_FILE="${CRED_DIR}/tokens.json"

echo "→ Google Drive MCP setup"
echo "  credentials: ${CRED_FILE}"
echo "  tokens:      ${TOKEN_FILE}"

mkdir -p "${CRED_DIR}"

if [[ ! -f "${CRED_FILE}" ]]; then
  echo ""
  echo "✗ Missing OAuth credentials."
  echo ""
  echo "1. Go to https://console.cloud.google.com/apis/credentials"
  echo "2. Create OAuth client → Application type: Desktop app"
  echo "3. Enable APIs: Drive, Docs, Sheets, Slides"
  echo "4. Download JSON → save as:"
  echo "   ${CRED_FILE}"
  echo ""
  echo "Template: ${CRED_DIR}/gcp-oauth.keys.example.json"
  exit 1
fi

echo "→ Running OAuth (browser opens on first run)"
GOOGLE_DRIVE_OAUTH_CREDENTIALS="${CRED_FILE}" \
  npx -y @piotr-agier/google-drive-mcp auth

echo "→ Verifying Grok MCP registration"
grok mcp list 2>/dev/null | grep -i google || grok mcp list

if command -v grok >/dev/null 2>&1; then
  echo "→ MCP doctor"
  grok mcp doctor google-drive 2>&1 || true
fi

echo ""
echo "✓ Setup complete."
echo "  In Grok TUI: /mcps → select google-drive → Authenticate (if needed)"
echo "  Then ask Grok to run the finance sheet-upload lane."