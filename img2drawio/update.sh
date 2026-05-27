#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$ROOT/references"

curl -fsSL \
  https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/style-reference.md \
  -o "$ROOT/references/style-reference.md"

curl -fsSL \
  https://raw.githubusercontent.com/jgraph/drawio-mcp/main/shared/mxfile.xsd \
  -o "$ROOT/references/mxfile.xsd"

echo "Updated references/style-reference.md and references/mxfile.xsd"
