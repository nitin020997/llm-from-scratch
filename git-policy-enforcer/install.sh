#!/bin/bash
set -e
HOOKS_SRC="$(cd "$(dirname "$0")/hooks" && pwd)"
GIT_HOOKS_DIR="$(git rev-parse --show-toplevel)/.git/hooks"

echo "━━━  Git Policy Enforcer — Hook Installer  ━━━"

if ! python3 -c "import yaml" &>/dev/null; then
  echo "Installing pyyaml..."
  pip install pyyaml --quiet
fi

for hook in commit-msg pre-push; do
  dst="$GIT_HOOKS_DIR/$hook"
  [ -f "$dst" ] && mv "$dst" "$dst.bak" && echo "Backed up existing $hook"
  cp "$HOOKS_SRC/$hook" "$dst"
  chmod +x "$dst"
  echo "✅  Installed: $hook"
done

echo "Done. Edit policy.yaml to customise rules."