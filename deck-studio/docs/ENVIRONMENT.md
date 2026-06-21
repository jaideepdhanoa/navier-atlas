# Environment

Grok should run this outside Tasklet with its own credentials.

## Python

```bash
cd deck-studio
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Required credentials

Set credentials in the environment or a local `.env` file that is **not committed**.

```bash
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-or-oauth.json
GOOGLE_TOKEN_PATH=/path/to/oauth-token.json
GITHUB_TOKEN=...
SLACK_TOKEN=...
IMAGE_PROVIDER_KEY=...
```

The code intentionally avoids storing secrets in the repository.
