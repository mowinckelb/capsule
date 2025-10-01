# Branching Strategy

## Overview
Capsule uses a feature branch workflow with `develop` as the integration branch and `main` as production.

## Branch Structure

```
main (production)
  └── develop (integration)
       ├── feature/api
       ├── feature/authentication
       ├── feature/chat
       ├── feature/config
       ├── feature/database
       ├── feature/frontend
       ├── feature/llm
       └── feature/web
```

## Workflow Rules

### When Working on Feature Branches

1. **Start work**: Always branch from latest `develop`
   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/your-feature
   ```

2. **Sync with develop regularly**: Pull develop changes into your feature branch at least daily or before starting work
   ```bash
   git checkout feature/your-feature
   git merge develop
   # Resolve any conflicts
   git push origin feature/your-feature
   ```

3. **Before creating PR**: Always sync with latest develop
   ```bash
   git checkout develop
   git pull origin develop
   git checkout feature/your-feature
   git merge develop
   # Resolve conflicts, test
   git push origin feature/your-feature
   ```

4. **After PR merged**: Update your local develop
   ```bash
   git checkout develop
   git pull origin develop
   ```

### When Develop is Updated

**Rule: Sync ALL feature branches within 24 hours of develop updates**

```bash
# For each active feature branch:
git checkout feature/branch-name
git merge develop
# Resolve conflicts
# Test that everything still works
git push origin feature/branch-name
```

### Conflict Resolution Priority

When merging develop into feature branches:
1. **Keep develop's**: agents.md, lessons.md, shared configs
2. **Keep feature's**: Module-specific code (unless develop has critical fixes)
3. **Merge both**: When both have valid changes (like database.py with optimizations + timestamps)

## PR Guidelines

1. **Title format**: `[module] brief description`
   - Example: `[frontend] add minimal monochrome ux`

2. **Description must include**:
   - What changed
   - Why it changed
   - How to test it
   - Any breaking changes

3. **Before merging**:
   - All tests pass
   - No merge conflicts
   - At least one review (for critical changes)
   - Locally tested

## Automation Rules for AI Agents

- **After every develop merge to main**: Alert to sync all feature branches
- **Before creating PR**: Automatically check if develop has new commits
- **During PR creation**: Auto-add checklist for sync status
