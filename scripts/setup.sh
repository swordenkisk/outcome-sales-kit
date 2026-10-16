#!/usr/bin/env sh
set -eu

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

printf '\nSetup complete. Activate the environment with:\n'
printf '  . .venv/bin/activate\n'
printf 'Then run:\n'
printf '  outcome-sales --help\n'
