#!/bin/bash

# Run three Claude agents in parallel

# Agent 1: Add MAX_SPEED=30 to game_config.py
claude --dangerously-skip-permissions -p "Add the line MAX_SPEED=30 to game_config.py in the current directory. Insert it as a new constant alongside the existing constants." &

# Agent 2: Create README.md with project features
claude --dangerously-skip-permissions -p "Create a README.md file in the current directory for a Bitcoin-themed Snake game project built with pygame. Include sections: Project Overview, Features, How to Play, Dependencies, and File Structure. Base it on these facts: the main game file is bitcoin_snake.py, it uses pygame, the snake is gold-colored, food is white, screen is 800x600, block size is 20px, speed is 10 FPS, SPACEBAR starts the game, arrow keys move the snake, wall or self-collision ends the game, and the project also includes btc_top_bottom_indicator.py for Bitcoin trading signals." &

# Agent 3: Create CHANGELOG.md
claude --dangerously-skip-permissions -p "Create a CHANGELOG.md file in the current directory for a Bitcoin-themed Snake game project. Include an Unreleased section and the following versions with brief descriptions: v1.0.0 - initial release with basic snake gameplay and Bitcoin theme, v1.1.0 - added levels and leaderboard system, v1.2.0 - added game_config.py for centralized configuration, v1.3.0 - fixed infinite loop bug in place_food when board is full. Use standard Keep a Changelog format." &

# Wait for all background agents to finish
wait

echo "All agents completed."
