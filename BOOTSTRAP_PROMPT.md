# homelab - Quick Start Guide

🤖 **AI-NATIVE PROJECT** - homelab monitoring system

## Immediate Context

- **Server**: http://localhost:5000
- **Environment**: `.venv/bin/python` (never system python)
- **Testing**: `quick_test.py` (dev) → `run-tests.sh` (pre-commit)
- **Git**: Feature branches → immediate merge → cleanup

## Essential Commands

```bash
./manage.sh setup              # One-time environment setup
./manage.sh start              # Start homelab
.venv/bin/python tests/quick_test.py  # Fast testing (2s)
./scripts/run-tests.sh         # Full testing (~30s)
```

## Git Workflow (AI + User Collaboration)

```bash
# AI creates branch and makes changes
./scripts/create-branch.sh feature-name "Description of work"
# ... AI implements feature ...
# ... AI shows user the results ...

# User approves, AI finalizes
./scripts/merge-to-main.sh "Final commit message"
# Auto: tests → commit → merge → push → cleanup
```

## Adding Features (DRY Pattern)

1. **Backend**: Add function to appropriate module
2. **Test**: Add to `test_suite.py` using dictionary format
3. **API**: Add endpoint to `homelab.py`
4. **Frontend**: Update templates/JS if needed

## Discovery Process (IMPORTANT)

**When starting a new project**: Conduct **conversational discovery** - ask ONE question at a time, listen to the answer, ask follow-ups, then move to the next topic. Fill PROJECT_GOALS.md as you learn, then create ROADMAP.md.

**Don't**: Dump all questions at once or assume what the user wants.

## Documentation (Auto-Maintained)

- **Primary**: `.github/copilot-instructions.md` (streamlined AI guide)
- **User**: `README.md` (auto-updated with live data)
- **Testing**: `TESTING.md` (consolidated test guide)
- **Roadmap**: `ROADMAP.md` (development plan and progress)
- **Goals**: `PROJECT_GOALS.md` (requirements and discovery results)

## Current Project Status

- **Status**: Starting Development
- **Features**: Basic Structure
- **Testing**: Template Ready

**Philosophy**: Practical development with AI collaboration
