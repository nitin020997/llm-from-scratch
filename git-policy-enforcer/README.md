# 🛡️ Git Branch & Commit Policy Enforcer

A lightweight, configurable CLI tool that enforces **branch naming conventions** and **commit message standards** at the git hook layer — no external CI system required.

Built for teams that want to shift policy enforcement **left** — catching violations before code ever hits a pipeline.

---

## 🚀 Features

- ✅ Enforces branch naming patterns (`feature/*`, `bugfix/*`, `hotfix/*`, etc.)
- ✅ Blocks direct pushes to protected branches (`main`, `master`, `production`)
- ✅ Validates commit messages against configurable format rules (Conventional Commits)
- ✅ Works via **git hooks** (`commit-msg`, `pre-push`) — zero pipeline dependency
- ✅ Fully configurable via a single `policy.yaml`
- ✅ Standalone CLI for manual checks or CI/CD integration

---

## 📁 Project Structure
```
git-policy-enforcer/
├── enforce_policy.py     # Core validator (branch + commit message)
├── policy.yaml           # All rules defined here
├── install.sh            # One-liner hook installer
├── requirements.txt
└── hooks/
    ├── commit-msg        # Auto-validates commit message on git commit
    └── pre-push          # Blocks push to protected branches
```

---

## ⚙️ Setup

### 1. Clone & install dependencies
```bash
git clone https://github.com/nitin020997/git-policy-enforcer.git
cd git-policy-enforcer
pip install -r requirements.txt
```

### 2. Install hooks into your repo
```bash
chmod +x install.sh
./install.sh
```

---

## 🧪 CLI Usage

### Validate current branch
```bash
python enforce_policy.py
```

### Validate a specific branch
```bash
python enforce_policy.py --branch "random-branch"
```

### Validate a commit message
```bash
python enforce_policy.py --commit-msg "feat(auth): add JWT token refresh"
```

### Validate both together
```bash
python enforce_policy.py --branch "feature/login" --commit-msg "feat(login): add OAuth2 support"
```

---

## 📋 Sample Output

**Pass:**
```
━━━  Git Policy Enforcer  ━━━

Branch:  feature/add-oauth
✅  Branch Policy: PASS
  Branch 'feature/add-oauth' matches allowed pattern.

Commit:  feat(auth): add OAuth2 login support
✅  Commit Message Policy: PASS
  Commit message is valid.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  All checks passed. Good to go! 🚀
```

**Fail:**
```
━━━  Git Policy Enforcer  ━━━

Branch:  random-stuff
❌  Branch Policy: FAIL
  Branch 'random-stuff' does not match any allowed pattern.
  Allowed:
  ^feature/[a-z0-9_-]+
  ^bugfix/[a-z0-9_-]+
  ...

Commit:  wip
❌  Commit Message Policy: FAIL
  Commit message too short (3 chars). Minimum: 10.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Policy violations found. Push blocked.
```

---

## 🔧 Configuration — `policy.yaml`
```yaml
protected_branches:
  - main
  - master
  - production

allowed_branch_patterns:
  - "^feature/[a-z0-9_-]+"
  - "^bugfix/[a-z0-9_-]+"
  - "^hotfix/[a-z0-9_-]+"
  - "^release/[0-9]+\\.[0-9]+"
  - "^chore/[a-z0-9_-]+"

commit_message:
  min_length: 10
  max_length: 100
  pattern: "^(feat|fix|hotfix|chore|docs|refactor|test|ci)(\\([a-z0-9_-]+\\))?: .+"
  pattern_hint: "Type(scope): description  →  e.g. feat(auth): add JWT validation"

direct_push_to_protected: false
```

---

## 🔗 CI/CD Integration
```bash
# Jenkins / any shell step
python enforce_policy.py --branch "${GIT_BRANCH}" --commit-msg "${GIT_COMMIT_MSG}"
if [ $? -ne 0 ]; then
  echo "Policy check failed. Aborting."
  exit 1
fi
```

---

## 💡 Use Cases

| Scenario | How this helps |
|---|---|
| No formal SDLC | Enforces structure before bad habits form |
| Multi-vendor teams | Consistent conventions across all contributors |
| Pre-CI validation | Catch violations locally, not in the pipeline |
| Audit & compliance | Traceable, policy-driven commit history |

---

## 🛠️ Requirements

- Python 3.8+
- `pyyaml`
- Git

---

## 📄 License

MIT