#!/usr/bin/env bash
# tools/get-agent-token.sh
#
# Generates a short-lived GitHub App installation access token.
# Claude runs this at the start of each session to authenticate gh CLI.
#
# Usage:
#   gh auth login --with-token <<< $(bash tools/get-agent-token.sh)
#
# Required env vars:
#   GITHUB_APP_ID              — numeric App ID (from GitHub App settings page)
#   GITHUB_APP_INSTALLATION_ID — numeric Installation ID (from /settings/installations/...)
#   GITHUB_APP_KEY_PATH        — path to the downloaded .pem private key file

set -euo pipefail

APP_ID="${GITHUB_APP_ID:?GITHUB_APP_ID is not set}"
INSTALLATION_ID="${GITHUB_APP_INSTALLATION_ID:?GITHUB_APP_INSTALLATION_ID is not set}"
PRIVATE_KEY_PATH="${GITHUB_APP_KEY_PATH:?GITHUB_APP_KEY_PATH is not set}"

if [[ ! -f "$PRIVATE_KEY_PATH" ]]; then
  echo "Private key not found at $PRIVATE_KEY_PATH" >&2
  exit 1
fi

# Build JWT (header.payload.signature)
now=$(date +%s)
exp=$((now + 540))  # 9-minute expiry (max allowed is 10)

b64url() {
  openssl base64 -A | tr '+/' '-_' | tr -d '='
}

header=$(echo -n '{"alg":"RS256","typ":"JWT"}' | b64url)
payload=$(echo -n "{\"iat\":$now,\"exp\":$exp,\"iss\":\"$APP_ID\"}" | b64url)
sig=$(echo -n "$header.$payload" | openssl dgst -sha256 -sign "$PRIVATE_KEY_PATH" -binary | b64url)

jwt="$header.$payload.$sig"

# Exchange JWT for installation access token, print just the token string
curl -s -X POST \
  -H "Authorization: Bearer $jwt" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/app/installations/$INSTALLATION_ID/access_tokens" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['token'])"
