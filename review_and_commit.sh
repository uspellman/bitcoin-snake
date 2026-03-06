#!/usr/bin/env bash
# review_and_commit.sh
#
# Automated code review and bug-fix pipeline for bitcoin_snake.py and game_config.py.
# Step 1: Uses Claude (headless) to review the files and write findings to code_review.md.
# Step 2: Uses Claude (headless) to read code_review.md and fix the single highest-priority bug.
# Step 3: Stages all changed files and commits with a descriptive conventional commit message.
#
# Usage: ./review_and_commit.sh
# Requires: claude CLI installed and authenticated (no API keys needed in this script).

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REVIEW_FILE="$REPO_DIR/code_review.md"

cd "$REPO_DIR"

# ─── Step 1: Code Review ──────────────────────────────────────────────────────
echo ""
echo "==> Step 1: Running Claude code review on bitcoin_snake.py and game_config.py..."
echo "    Writing findings to code_review.md..."

claude -p \
  "You are a Python code reviewer. Read the files bitcoin_snake.py and game_config.py in the current directory. Then write a structured code review to code_review.md with exactly three sections: '## Bugs', '## Code Quality', and '## Suggested Improvements'. Under '## Bugs', list each bug with a short title, a description of the problem, and a severity label (Critical, High, Medium, or Low). Be specific and reference line numbers where possible. Do not fix anything — only review and write the report." \
  --allowedTools "Read,Write" \
|| { echo "ERROR: Step 1 (code review) failed. Aborting."; exit 1; }

echo "    Code review written to code_review.md."

# ─── Step 2: Bug Fix ──────────────────────────────────────────────────────────
echo ""
echo "==> Step 2: Running Claude to fix the single highest-priority bug..."

claude -p \
  "You are a Python bug fixer. Read code_review.md and identify the single highest-priority bug listed under the '## Bugs' section (the one with the highest severity, or the first one if severities are equal). Then read the relevant source file (bitcoin_snake.py or game_config.py) and apply only that one fix. Add a short inline comment directly above or on the changed line(s) in the format: '# BUG FIX: <brief description of what was fixed and why'. Do not fix any other bugs. Do not refactor or improve anything else. Do not modify code_review.md." \
  --allowedTools "Read,Write" \
|| { echo "ERROR: Step 2 (bug fix) failed. Aborting."; exit 1; }

echo "    Bug fix applied."

# ─── Step 3: Git Commit ───────────────────────────────────────────────────────
echo ""
echo "==> Step 3: Staging changes and committing..."

git add -A

# Build the commit message by asking Claude what it fixed, then use it
COMMIT_MSG=$(claude -p \
  "Read code_review.md. Look at the single highest-priority bug that was listed under '## Bugs'. Output ONLY a single conventional commit message line (no explanation, no markdown, no quotes) in the format: 'fix(<scope>): <short description of the bug that was fixed>' where <scope> is either bitcoin_snake or game_config depending on which file contained the bug. Keep the description under 72 characters total." \
  --allowedTools "Read" \
) || { echo "ERROR: Step 3 (generating commit message) failed. Aborting."; exit 1; }

# Sanitize: strip any surrounding whitespace or quotes
COMMIT_MSG="$(echo "$COMMIT_MSG" | tr -d '\r' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | head -n 1)"

if [ -z "$COMMIT_MSG" ]; then
  COMMIT_MSG="fix: apply highest-priority bug fix from automated code review"
fi

echo "    Commit message: $COMMIT_MSG"
git commit -m "$COMMIT_MSG"

echo ""
echo "==> Done. All steps completed successfully."
echo "    Review: $REVIEW_FILE"
echo "    Committed: $COMMIT_MSG"
