# Deployment Guide - GitHub to Hugging Face Spaces

This guide explains how to pull updates from GitHub and deploy them to Hugging Face Spaces.

## Repository Setup

### GitHub Repository
- **URL**: https://github.com/7kash/Legally_AI
- **Local Path**: `/Users/ekaterinamatyushina/Legally_AI`
- **Purpose**: Main development repository with all documentation and code

### Hugging Face Space
- **URL**: https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI
- **Local Path**: `/Users/ekaterinamatyushina/Legally_AI/prototype`
- **Purpose**: Live deployment of the prototype

## Git Remote Structure

The project uses **two separate git repositories**:

### 1. Main Repository (Parent)
```bash
Location: /Users/ekaterinamatyushina/Legally_AI
Remote "origin": GitHub (7kash/Legally_AI)
```

### 2. Prototype Repository (Subfolder)
```bash
Location: /Users/ekaterinamatyushina/Legally_AI/prototype
Remote "hf": Hugging Face Spaces (7Kash-FluffyHedgehog/Legally_AI)
```

**Note**: The `prototype/` folder is a SEPARATE git repository from the parent folder.

---

## Standard Workflow: GitHub → Hugging Face

### Step 1: Pull Latest Changes from GitHub

```bash
# Navigate to main repository
cd /Users/ekaterinamatyushina/Legally_AI

# Check current status
git status

# Pull latest changes from GitHub
git fetch origin
git pull origin main

# Or if working with a specific branch (e.g., Claude's fix branch)
git fetch origin claude/fix-hffolder-import-error-011CUrqJ4XHZNzds1gS41u9E
git merge origin/claude/fix-hffolder-import-error-011CUrqJ4XHZNzds1gS41u9E
```

### Step 2: Verify Changes

```bash
# Check what changed
git log --oneline -5

# View specific file changes if needed
git diff HEAD~1 prototype/

# Check the prototype folder specifically
cd prototype
ls -la
```

### Step 3: Deploy to Hugging Face Spaces

```bash
# Navigate to prototype folder
cd /Users/ekaterinamatyushina/Legally_AI/prototype

# Check git status (should be clean after pulling from parent)
git status

# Stage all changes
git add .

# Commit with descriptive message
git commit -m "Update prototype with latest fixes from GitHub"

# Push to Hugging Face Spaces
git push hf main
```

### Step 4: Verify Deployment

1. **Check Build Logs**:
   - Go to: https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI/logs
   - Wait for build to complete (~2-5 minutes, or ~5-7 minutes if OCR dependencies changed)

2. **Verify Files Updated**:
   - Go to: https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI/tree/main
   - Check that your files are updated (look at timestamps)

3. **Test the Application**:
   - Open: https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI
   - Upload a test contract
   - Verify the analysis works correctly

---

## Quick Commands Cheat Sheet

### Check Remotes
```bash
# Main repo
cd /Users/ekaterinamatyushina/Legally_AI
git remote -v
# Should show: origin -> GitHub

# Prototype repo
cd /Users/ekaterinamatyushina/Legally_AI/prototype
git remote -v
# Should show: hf -> Hugging Face
```

### Pull from GitHub
```bash
cd /Users/ekaterinamatyushina/Legally_AI
git pull origin main
```

### Push to HF Spaces
```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype
git add .
git commit -m "Your message here"
git push hf main
```

### View Recent Changes
```bash
# Main repo
cd /Users/ekaterinamatyushina/Legally_AI
git log --oneline -10

# Prototype repo
cd prototype
git log --oneline -10
```

---

## Common Scenarios

### Scenario 1: Claude Fixed a Bug on GitHub

```bash
# 1. Pull the fix
cd /Users/ekaterinamatyushina/Legally_AI
git fetch origin claude/fix-branch-name
git merge origin/claude/fix-branch-name

# 2. Deploy to HF
cd prototype
git add .
git commit -m "Apply bug fix from GitHub"
git push hf main
```

### Scenario 2: Update Only Specific Files

```bash
# 1. Pull from GitHub
cd /Users/ekaterinamatyushina/Legally_AI
git pull origin main

# 2. Check what changed in prototype
cd prototype
git status

# 3. Stage only specific files
git add src/parsers.py src/constants.py

# 4. Commit and push
git commit -m "Update parsers and constants"
git push hf main
```

### Scenario 3: Test Locally Before Deploying

```bash
# 1. Pull from GitHub
cd /Users/ekaterinamatyushina/Legally_AI
git pull origin main

# 2. Navigate to prototype
cd prototype

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install/update dependencies
pip install -r requirements.txt --upgrade

# 5. Test locally
python app.py
# Open http://localhost:7860 and test

# 6. If tests pass, deploy
git add .
git commit -m "Update after successful local testing"
git push hf main
```

### Scenario 4: Rollback if Deployment Fails

```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype

# Check recent commits
git log --oneline -5

# Rollback to previous commit
git reset --hard HEAD~1

# Force push to HF
git push hf main --force
```

---

## Troubleshooting

### Issue: "Git push rejected"

```bash
# Usually means HF Space has changes you don't have locally
cd /Users/ekaterinamatyushina/Legally_AI/prototype

# Pull from HF first
git pull hf main

# Then push
git push hf main
```

### Issue: "Merge conflict"

```bash
# If you get conflicts when pulling from GitHub
cd /Users/ekaterinamatyushina/Legally_AI

# Check which files have conflicts
git status

# Option 1: Accept their changes
git checkout --theirs path/to/file

# Option 2: Accept your changes
git checkout --ours path/to/file

# Option 3: Manually edit the file
# Open the file, resolve conflicts, then:
git add path/to/file
git commit -m "Resolve merge conflict"
```

### Issue: "HF Space build failing"

1. **Check build logs**: https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI/logs
2. **Common causes**:
   - Missing dependency in `requirements.txt`
   - Missing system package in `packages.txt`
   - Python syntax error
   - File path error
3. **Fix and redeploy**:
   ```bash
   cd /Users/ekaterinamatyushina/Legally_AI/prototype
   # Fix the issue
   git add .
   git commit -m "Fix build issue"
   git push hf main
   ```

### Issue: "Changes not showing on HF"

1. **Clear browser cache** and refresh
2. **Check file actually updated** on https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI/tree/main
3. **Wait for build to complete** (check logs)
4. **Force restart** the space (Factory reboot button in Settings)

---

## File Sync Checklist

When updating HF Spaces, these files are critical:

### Always Check These Files:
- ✅ `requirements.txt` - Python dependencies
- ✅ `packages.txt` - System dependencies (OCR, poppler, etc.)
- ✅ `app.py` - Main application
- ✅ `src/` - All source code files
- ✅ `README.md` - Space description (shows on HF page)

### Optional But Useful:
- `.env.example` - Example environment variables
- `QUICKSTART.md` - Deployment instructions

### Do NOT Push:
- `.env` - Contains secrets (API keys)
- `venv/` - Virtual environment
- `__pycache__/` - Python cache
- `.DS_Store` - Mac system files

---

## Environment Variables

### Setting Secrets on HF Spaces:

1. Go to: https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI/settings
2. Scroll to **Repository secrets**
3. Add secret:
   - **Name**: `GROQ_API_KEY`
   - **Value**: Your Groq API key (starts with `gsk_`)
4. Click **Add**
5. Restart the space

**Note**: Secrets are injected as environment variables at runtime. The app reads them via `os.getenv("GROQ_API_KEY")`.

---

## Branch Strategy

### Main Branch (`main`)
- Stable, tested code
- Direct pushes to main

### Claude's Fix Branches (`claude/*`)
- Format: `claude/description-sessionID`
- Example: `claude/fix-hffolder-import-error-011CUrqJ4XHZNzds1gS41u9E`
- Merge into main after testing

### Workflow:
1. Claude creates fix branch on GitHub
2. You pull and test locally
3. Deploy to HF from the fix branch (or merge to main first)

---

## Emergency Procedures

### Quick Rollback:
```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype
git reset --hard HEAD~1
git push hf main --force
```

### Deploy Last Known Good Version:
```bash
cd /Users/ekaterinamatyushina/Legally_AI/prototype
git log --oneline -10
# Find the good commit hash (e.g., abc1234)
git reset --hard abc1234
git push hf main --force
```

### Completely Fresh Deploy:
```bash
# Delete prototype folder
rm -rf /Users/ekaterinamatyushina/Legally_AI/prototype

# Clone fresh from HF
cd /Users/ekaterinamatyushina/Legally_AI
git clone https://huggingface.co/spaces/7Kash-FluffyHedgehog/Legally_AI prototype

# Or clone from GitHub's prototype folder
# (if you keep prototype in GitHub too)
```

---

## Best Practices

1. **Always Pull Before Push**:
   ```bash
   git pull origin main  # Pull from GitHub first
   git pull hf main      # Pull from HF before pushing
   ```

2. **Test Locally When Possible**:
   - Run `python app.py` locally
   - Test with sample contracts
   - Then deploy to HF

3. **Use Descriptive Commit Messages**:
   - ❌ "update"
   - ✅ "Fix DOCX table extraction and add OCR support"

4. **Monitor Build Logs**:
   - Always check logs after pushing
   - Don't assume it worked

5. **Keep Dependencies Pinned**:
   - Use specific versions in `requirements.txt`
   - Example: `groq>=0.13.0` not `groq`

---

## Additional Resources

- **HF Spaces Documentation**: https://huggingface.co/docs/hub/spaces
- **Git Documentation**: https://git-scm.com/doc
- **Project Documentation**: See `/docs/` in main repository

---

**Last Updated**: 2025-11-06
**Maintained By**: Ekaterina Matyushina
**Session**: 011CUrqJ4XHZNzds1gS41u9E
