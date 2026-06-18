#!/bin/bash
set -e

if [ ! -f uv.lock ] && [ ! -f pyproject.toml ]; then
    echo "Initializing uv project..."
    uv init --bare
    uv add django
    uv add --dev djlint
fi

echo "Syncing dependencies..."
uv sync