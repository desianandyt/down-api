#!/usr/bin/env bash
set -e
pip install -r requirements.txt
if command -v npm &> /dev/null; then
    npm install --omit=dev || true
fi
