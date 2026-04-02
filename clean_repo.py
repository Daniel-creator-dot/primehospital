from pathlib import Path
import subprocess
import sys

repo = Path(__file__).resolve().parent
print(f"Repo: {repo}")

patterns = [
    "*.md",
    "*.txt",
    "*.log",
    "*.bak",
    "*.backup",
    "*.sql",
    "*.sqlite3",
    "*.sqlite3-journal",
    "*.db",
    "*.zip",
    "*.dump",
]
dirs = [
    "backups",
    "media",
    "static",
    "staticfiles",
    "logs",
    "venv",
    "env",
    "ENV",
    ".venv",
    ".idea",
    ".vscode",
]


def run(cmd):
    print("$", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=repo, capture_output=True, text=True)
    print(proc.stdout.strip())
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)
    return proc

run(["git", "status", "--short", "--branch"])
for p in patterns:
    run(["git", "rm", "-r", "--cached", "-f", "--ignore-unmatch", p])
for d in dirs:
    run(["git", "rm", "-r", "--cached", "-f", "--ignore-unmatch", d])
run(["git", "add", ".gitignore"])
run(["git", "status", "--short", "--branch"])
run(["git", "commit", "-m", "Clean repo: remove docs and local backups before push"])
run(["git", "push", "origin", "main"])
