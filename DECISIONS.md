# Decisions and Current State

## Core Approach
- **Decision:** Use `update_addon.py` script for addon.xml generation instead of semantic-release's native template system
- **Reason:** Semantic-release templates had undefined variable issues (`'unreleased' is undefined`)
- **Status:** ✅ Working locally, produces correct addon.xml output

## Configuration
- **build_command:** `python update_addon.py` - runs script during semantic-release build phase
- **Templates config:** Removed from changelog section (not using semantic-release templating)
- **Version source:** Script reads version from pyproject.toml
- **Commit parsing:** Script parses git log for conventional commits (feat, fix, perf)

## What Works
- ✅ Script generates correct addon.xml with version and commit-based news
- ✅ Conventional commit parsing (feat → [new], fix → [fix])
- ✅ Semantic-release version bumping and changelog generation
- ✅ GitHub Actions workflow with conditional build/upload
- ✅ Template uses correct variables for script rendering
- ✅ Script integration with semantic-release build process
- ✅ Version updated correctly in addon.xml during release process

## What Needs Testing
- ✅ Integration: Script running correctly within semantic-release build process
- ✅ Version timing: Script gets updated version from pyproject.toml during release
- CI/CD: Full workflow in GitHub Actions (ready to test)

## Previous Attempts (Don't Revert To)
- ❌ Semantic-release templates with `ctx.history.unreleased.items()`
- ❌ Template variables like `unreleased` or `commits` in semantic-release context
- ❌ Pip install + templates config approach

## Files
- `update_addon.py`: Main script for addon.xml generation
- `templates/addon.xml.j2`: Template used by script (not semantic-release)
- `pyproject.toml`: semantic-release config with script build_command