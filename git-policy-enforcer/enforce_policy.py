#!/usr/bin/env python3
import re
import sys
import subprocess
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml. Run: pip install pyyaml")
    sys.exit(1)

RESET  = "\033[0m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"

def load_policy(policy_path="policy.yaml"):
    path = Path(policy_path)
    if not path.exists():
        print(f"{RED}Policy file not found: {policy_path}{RESET}")
        sys.exit(1)
    with open(path) as f:
        return yaml.safe_load(f)

def get_current_branch():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"{RED}Not inside a git repository.{RESET}")
        sys.exit(1)

def validate_branch(branch, policy):
    protected = policy.get("protected_branches", [])
    patterns  = policy.get("allowed_branch_patterns", [])
    if branch in protected:
        if not policy.get("direct_push_to_protected", False):
            return False, f"Direct push to protected branch '{branch}' is not allowed."
        return True, f"Branch '{branch}' is protected but direct push is permitted."
    for pattern in patterns:
        if re.match(pattern, branch):
            return True, f"Branch '{branch}' matches allowed pattern."
    allowed = "\n  ".join(patterns)
    return False, f"Branch '{branch}' does not match any allowed pattern.\n  Allowed:\n  {allowed}"

def validate_commit_message(message, policy):
    cfg     = policy.get("commit_message", {})
    min_len = cfg.get("min_length", 10)
    max_len = cfg.get("max_length", 100)
    pattern = cfg.get("pattern", "")
    hint    = cfg.get("pattern_hint", "")
    message = message.strip()
    if len(message) < min_len:
        return False, f"Commit message too short ({len(message)} chars). Minimum: {min_len}."
    if len(message) > max_len:
        return False, f"Commit message too long ({len(message)} chars). Maximum: {max_len}."
    if pattern and not re.match(pattern, message):
        return False, f"Invalid format.\n  Expected: {hint}\n  Got: \"{message}\""
    return True, "Commit message is valid."

def print_result(label, ok, detail):
    icon   = f"{GREEN}✅{RESET}" if ok else f"{RED}❌{RESET}"
    status = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
    print(f"\n{BOLD}{icon}  {label}: {status}{RESET}")
    color = GREEN if ok else YELLOW
    for line in detail.splitlines():
        print(f"  {color}{line}{RESET}")

def run_check(args, policy):
    all_passed = True
    print(f"\n{CYAN}{BOLD}━━━  Git Policy Enforcer  ━━━{RESET}")

    branch = args.branch or get_current_branch()
    print(f"\n{BOLD}Branch:{RESET}  {branch}")
    ok, detail = validate_branch(branch, policy)
    print_result("Branch Policy", ok, detail)
    if not ok:
        all_passed = False

    commit_msg = None
    if args.commit_msg:
        commit_msg = args.commit_msg
    elif args.commit_file:
        commit_msg = Path(args.commit_file).read_text().strip()

    if commit_msg is not None:
        print(f"\n{BOLD}Commit:{RESET}  {commit_msg}")
        ok, detail = validate_commit_message(commit_msg, policy)
        print_result("Commit Message Policy", ok, detail)
        if not ok:
            all_passed = False

    print(f"\n{CYAN}{'━'*34}{RESET}")
    if all_passed:
        print(f"{GREEN}{BOLD}  All checks passed. Good to go! 🚀{RESET}\n")
    else:
        print(f"{RED}{BOLD}  Policy violations found. Push blocked.{RESET}\n")
    return all_passed

def main():
    parser = argparse.ArgumentParser(description="Enforce git branch and commit message policies.")
    parser.add_argument("--branch",      help="Branch name to validate")
    parser.add_argument("--commit-msg",  help="Commit message to validate")
    parser.add_argument("--commit-file", help="Path to commit message file (used by git hook)")
    parser.add_argument("--policy",      default="policy.yaml", help="Path to policy YAML")
    args = parser.parse_args()
    policy = load_policy(args.policy)
    passed = run_check(args, policy)
    sys.exit(0 if passed else 1)

if __name__ == "__main__":
    main()