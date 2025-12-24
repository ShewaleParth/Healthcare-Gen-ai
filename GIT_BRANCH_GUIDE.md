# Git Branch Workflow Guide

## 🌿 Creating and Pushing a New Branch

### Step 1: Check Current Status
```bash
git status
```
This shows what files have been modified.

### Step 2: Create a New Branch
```bash
# Create and switch to new branch
git checkout -b feature/ml-pneumonia-detection

# Or use the newer syntax
git switch -c feature/ml-pneumonia-detection
```

**Branch Naming Conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `enhancement/` - Improvements
- `docs/` - Documentation

### Step 3: Stage Your Changes
```bash
# Stage all changes
git add .

# Or stage specific files
git add Backend/app/agents/diagnostic_agent.py
git add Backend/app/routes/diagnosis.py
git add requirements.txt
```

### Step 4: Commit Your Changes
```bash
git commit -m "feat: integrate Groq AI for pneumonia detection

- Added diagnostic agent with Llama 3.3 70B
- Implemented medical expert prompting
- Updated diagnosis routes
- Added ML dependencies to requirements.txt
- Enhanced frontend with heatmap support"
```

### Step 5: Push to Remote
```bash
# First time pushing this branch
git push -u origin feature/ml-pneumonia-detection

# Subsequent pushes
git push
```

---

## 🔄 Complete Workflow

```bash
# 1. Create branch
git checkout -b feature/ml-pneumonia-detection

# 2. Stage changes
git add .

# 3. Commit
git commit -m "feat: integrate AI-powered pneumonia detection"

# 4. Push
git push -u origin feature/ml-pneumonia-detection
```

---

## 📋 What to Include in Your Commit

### Files Modified:
- `Backend/app/agents/diagnostic_agent.py` - AI diagnostic agent
- `Backend/app/routes/diagnosis.py` - API routes
- `Backend/app/models/` - ML model files
- `Backend/app/utils/gradcam.py` - Explainability
- `requirements.txt` - Dependencies
- `Frontend/src/pages/Diagnostics.jsx` - UI updates

### Commit Message Format:
```
feat: add AI-powered pneumonia detection

- Integrated Groq Llama 3.3 70B for medical analysis
- Added diagnostic agent with expert prompting
- Implemented Grad-CAM visualization support
- Enhanced frontend with heatmap display
- Updated API routes for image analysis
- Added comprehensive medical reporting
```

---

## 🎯 Quick Commands

```bash
# Create branch and push in one go
git checkout -b feature/ml-pneumonia-detection
git add .
git commit -m "feat: integrate AI pneumonia detection system"
git push -u origin feature/ml-pneumonia-detection
```

---

## 🔍 Useful Git Commands

```bash
# See what branch you're on
git branch

# See all branches (local and remote)
git branch -a

# Switch to existing branch
git checkout main
git checkout feature/ml-pneumonia-detection

# Delete local branch
git branch -d feature/ml-pneumonia-detection

# See commit history
git log --oneline

# See what files changed
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

---

## 🚀 After Pushing

1. **Go to GitHub** (or your Git hosting)
2. **Create Pull Request** from your branch
3. **Add description** of changes
4. **Request review** if needed
5. **Merge** when approved

---

## ⚠️ Before Pushing

### Check These:
- [ ] Remove sensitive data (API keys, passwords)
- [ ] Update `.gitignore` if needed
- [ ] Test your code works
- [ ] Write clear commit message
- [ ] Review `git status` output

### Important Files to NOT Commit:
- `.env` (API keys)
- `node_modules/`
- `__pycache__/`
- `*.pyc`
- Virtual environment folders

---

## 📝 Recommended Branch Name

For your current work:
```bash
git checkout -b feature/ai-pneumonia-detection
```

Or:
```bash
git checkout -b enhancement/ml-diagnostic-system
```

---

**Ready to push? Run the commands above!** 🚀
