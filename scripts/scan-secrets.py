#!/usr/bin/env python3

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]

SECRET_PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN (RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("aws-access-key", re.compile(r"A(KIA|SIA)[0-9A-Z]{16}")),
    ("github-token", re.compile(r"(github_pat_[A-Za-z0-9_]{20,255}|gh[pousr]_[A-Za-z0-9_]{20,255})")),
    ("google-api-key", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("google-oauth-access-token", re.compile(r"ya29\.[A-Za-z0-9._-]{20,}")),
    ("google-refresh-token", re.compile(r"1//[A-Za-z0-9._-]{20,}")),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")),
    ("slack-token", re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("openai-key", re.compile(r"sk-[A-Za-z0-9]{20,}")),
    (
        "generic-assignment",
        re.compile(
            r"\b(api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|"
            r"private[_-]?key|secret[_-]?key|password|passwd|pwd|credential)\b"
            r"[A-Za-z0-9_ .-]{0,30}[:=][ \t]*[\"']?[A-Za-z0-9_./+=:-]{16,}",
            re.IGNORECASE,
        ),
    ),
]

SENSITIVE_NAME_PATTERN = re.compile(
    r"(^|/)(\.env($|\.)|.*credentials.*|.*secret.*|.*token.*|id_rsa|id_ed25519|"
    r"known_hosts|.*\.pem$|.*\.key$|.*\.p12$|.*\.pfx$|.*netrc.*)",
    re.IGNORECASE,
)

SKIPPED_DIRS = {".git", "node_modules"}
SKIPPED_PATH_PARTS = {("dein", "repos")}
ALLOWED_SENSITIVE_PATHS = {
    "script/scan-secrets.sh",
    "scripts/scan-secrets.py",
    "scripts/scan-secrets.sh",
}


@dataclass(frozen=True)
class Match:
    path: str
    line: int
    column: int
    label: str


def run_git(args: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT_DIR,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def tracked_existing_files() -> list[Path]:
    completed = run_git(["ls-files", "-z"])
    if completed.returncode != 0:
        print(completed.stderr.strip(), file=sys.stderr)
        raise SystemExit(completed.returncode)

    files: list[Path] = []
    for raw_path in completed.stdout.split("\0"):
        if not raw_path:
            continue
        path = ROOT_DIR / raw_path
        if path.is_file():
            files.append(path)
    return files


def should_skip_path(path: Path) -> bool:
    rel_parts = path.relative_to(ROOT_DIR).parts
    if any(part in SKIPPED_DIRS for part in rel_parts):
        return True

    return any(
        len(rel_parts) >= len(skipped)
        and any(tuple(rel_parts[index : index + len(skipped)]) == skipped for index in range(len(rel_parts) - len(skipped) + 1))
        for skipped in SKIPPED_PATH_PARTS
    )


def iter_local_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT_DIR.rglob("*"):
        if not path.is_file():
            continue
        if should_skip_path(path):
            continue
        files.append(path)
    return files


def relative(path: Path) -> str:
    return path.relative_to(ROOT_DIR).as_posix()


def read_text_lossy(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def scan_file(path: Path, label: str, pattern: re.Pattern[str]) -> list[Match]:
    matches: list[Match] = []
    try:
        text = read_text_lossy(path)
    except OSError as exc:
        print(f"warning: cannot read {relative(path)}: {exc}", file=sys.stderr)
        return matches

    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in pattern.finditer(line):
            matches.append(Match(relative(path), line_number, match.start() + 1, label))
    return matches


def print_matches(label: str, matches: list[Match]) -> None:
    if not matches:
        return

    print()
    print(f"[{label}]")
    for match in sorted(set(matches), key=lambda item: (item.path, item.line, item.column, item.label)):
        print(f"{match.path}:{match.line}:{match.column} {match.label}")


def is_ignored(path: str) -> bool:
    completed = run_git(["check-ignore", "--quiet", "--", path])
    return completed.returncode == 0


def unignored_sensitive_files() -> list[str]:
    files: list[str] = []
    for path in iter_local_files():
        rel_path = relative(path)
        if rel_path in ALLOWED_SENSITIVE_PATHS:
            continue
        if not SENSITIVE_NAME_PATTERN.search(rel_path):
            continue
        if is_ignored(rel_path):
            continue
        files.append(rel_path)
    return sorted(set(files))


def main() -> int:
    found = False
    print(f"Scanning tracked files for secret patterns under {ROOT_DIR}")

    tracked_files = tracked_existing_files()
    for label, pattern in SECRET_PATTERNS:
        label_matches: list[Match] = []
        for path in tracked_files:
            label_matches.extend(scan_file(path, label, pattern))
        if label_matches:
            found = True
            print_matches(label, label_matches)

    unignored_files = unignored_sensitive_files()
    if unignored_files:
        found = True
        print()
        print("[unignored-sensitive-file-name]")
        for file in unignored_files:
            print(file)

    if found:
        print()
        print("Potential secrets found.")
        return 1

    print("No potential secrets found, and sensitive local file names are ignored.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
