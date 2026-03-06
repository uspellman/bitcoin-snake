#!/usr/bin/env bash
# build.sh — Package bitcoin_snake.py into a standalone Mac .app
# Requires: pip install pyinstaller
# Usage: bash build.sh

set -e

echo "Building Bitcoin Snake.app..."

pyinstaller \
  --windowed \
  --onefile \
  --name "Bitcoin Snake" \
  --add-data "bitcoin_logo.png:." \
  --add-data "eat.wav:." \
  --add-data "gameover.wav:." \
  --add-data "highscore.txt:." \
  bitcoin_snake.py

echo ""
echo "Done! Your app is at: dist/Bitcoin Snake.app"
echo "Double-click it to play — no Python required."
