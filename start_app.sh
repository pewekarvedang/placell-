#!/usr/bin/env bash
# =====================================================================
# Placell - Unified Server Startup Script (Linux / macOS)
# =====================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "====================================================================="
echo " Placell: AI-Powered Student Placement Experience and Career Analytics"
echo " Solo Developer: Vedang Pewekar (B.Tech CSBS)"
echo "====================================================================="

if [ ! -f "frontend/dist/index.html" ]; then
    echo "[1/2] Compiling frontend static bundle..."
    (cd frontend && npm install && npm run build)
else
    echo "[1/2] Frontend static assets present in frontend/dist/"
fi

export PYTHONPATH="$SCRIPT_DIR/backend"

echo "[2/2] Starting Placell unified server on http://0.0.0.0:8000 ..."
echo "API Docs available at: http://localhost:8000/docs"

exec python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
