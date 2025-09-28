@echo off
echo Starting git organization...

REM First, commit all changes to develop branch
echo.
echo === Step 1: Committing file reorganization to develop ===
git add .
git commit -m "feat: Complete modular reorganization - moved files to proper modules

- Moved web application from develop/web_original.py to web/web.py
- Created frontend/ module with components and static files
- Created chat/ module with CLI and message handlers
- Created config/ module with centralized configuration
- Updated develop/ integration files to use new module structure
- Removed duplicate and misplaced files
- Maintained backward compatibility"

REM Create and populate frontend branch
echo.
echo === Step 2: Creating feature/frontend branch ===
git checkout -b feature/frontend
git add frontend/
git commit -m "feat(frontend): Add dedicated frontend module

- Created frontend/components/ with landing.html and interface.html
- Added frontend/static/js/ with app.js and config.js
- Implemented FrontendService with clean interface
- Added comprehensive configuration and documentation
- Responsive design with authentication and memory management"

REM Create and populate chat branch
echo.
echo === Step 3: Creating feature/chat branch ===
git checkout develop
git checkout -b feature/chat
git add chat/
git commit -m "feat(chat): Add modular chat interface system

- Created chat/cli.py with interactive command-line interface
- Added chat/handlers.py for multi-platform message handling
- Implemented extensible architecture for Web, Slack, Discord
- Added comprehensive command parsing and formatting
- Includes authentication and session management"

REM Create and populate config branch
echo.
echo === Step 4: Creating feature/config branch ===
git checkout develop
git checkout -b feature/config
git add config/
git commit -m "feat(config): Add centralized configuration management

- Created config/settings.py with app, server, and feature settings
- Added config/providers.py for LLM and database configurations
- Implemented config/environment.py with variable validation
- Added comprehensive configuration service interface
- Support for multiple environments and feature flags"

REM Return to develop and show status
echo.
echo === Step 5: Returning to develop branch ===
git checkout develop

echo.
echo === Git organization complete! ===
echo.
echo Created branches:
git branch --list | findstr "feature/"
echo.
echo Current branch:
git branch --show-current
echo.
echo Recent commits:
git log --oneline -5

pause
