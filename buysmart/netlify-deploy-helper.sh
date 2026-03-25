#!/usr/bin/env bash
set -euo pipefail

# Helper script: builds frontend and deploys to Netlify.
# Usage:
#   bash netlify-deploy-helper.sh <NETLIFY_SITE_ID>
#     or without args to get interactive site selection.

SITE_ID=${1:-""}
FRONTEND_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/frontend"

cd "$FRONTEND_DIR"

echo "Installing dependencies..."
npm install

echo "Building frontend..."
npm run build

if [ -n "$SITE_ID" ]; then
  echo "Deploying to Netlify site ID: $SITE_ID"
  netlify deploy --prod --dir .next --site "$SITE_ID"
else
  echo "Deploying to Netlify (interactive)..."
  netlify deploy --prod --dir .next
fi

echo "Deployment done. Should output public URL above."

# optional check if site URL appears in netlify status
SITE_URL=$(netlify status --json 2>/dev/null | jq -r '.site.url // empty' || true)
if [ -n "$SITE_URL" ]; then
  echo "Your site URL: $SITE_URL"
fi

echo "If you see 404, ensure NEXT_PUBLIC_BACKEND_URL is correct in Netlify settings."
