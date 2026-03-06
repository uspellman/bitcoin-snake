# bitcoin-snake-dev Plugin

A Claude Code plugin for the Bitcoin Snake project. It bundles a black auto-formatter hook and a `/review` slash command to streamline development.

## What It Does

### 1. Black Auto-Formatter Hook
Every time Claude writes a `.py` file, `black` is automatically run on it to enforce consistent code formatting. This happens silently in the background — if `black` is not installed or fails for any reason, the hook exits cleanly without interrupting your workflow.

- **Event:** PostToolUse
- **Trigger:** Write tool
- **Command:** `black "$CLAUDE_TOOL_INPUT_FILE_PATH" 2>/dev/null || true`

### 2. `/review` Slash Command
Invoking `/review` in Claude Code runs the `review_and_commit.sh` pipeline in the project root. Use this to trigger automated code review and commits from within a Claude conversation.

- **File:** `.claude/commands/review.md`
- **Description:** Run automated code review and bug fix pipeline

## How to Install

Copy the `.claude/` folder from this project into your own project root:

```bash
cp -r .claude/ /path/to/your/project/
```

The structure Claude Code expects:

```
your-project/
└── .claude/
    ├── settings.json          # Hooks config (black formatter)
    ├── commands/
    │   └── review.md          # /review slash command
    └── plugins/
        └── bitcoin-snake-dev/
            ├── README.md      # This file
            └── hooks.json     # Hooks config reference
```

## Requirements

- **Claude Code** — CLI must be installed and running
- **Python 3** — required to run the project scripts
- **black** — Python code formatter

Install black with:

```bash
pip install black
```

## Notes

- No API keys or tokens are stored anywhere in this plugin.
- All paths are relative — no hardcoded system paths.
- `.env` files inside `.claude/` are excluded via `.gitignore`.
