#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v rg >/dev/null 2>&1; then
  echo "error: ripgrep (rg) is required" >&2
  exit 2
fi

RG=(rg --no-config)

EXCLUDES=(
  -g '!**/.git/**'
  -g '!**/node_modules/**'
  -g '!**/dein/repos/**'
  -g '!**/google-chrome/**'
  -g '!script/scan-secrets.sh'
)

FOUND=0

print_matches() {
  local label="$1"
  local pattern="$2"
  local output

  output="$("${RG[@]}" --hidden --with-filename --line-number --column --only-matching "${EXCLUDES[@]}" -e "$pattern" . || true)"
  if [[ -n "$output" ]]; then
    FOUND=1
    echo
    echo "[$label]"
    awk -v label="$label" -F: 'NF >= 4 { print $1 ":" $2 ":" $3 " " label }' <<<"$output" | sort -u
  fi
}

echo "Scanning for secret patterns under $ROOT_DIR"

print_matches "private-key" '-----BEGIN (RSA |DSA |EC |OPENSSH |PGP )?PRIVATE KEY-----'
print_matches "aws-access-key" 'A(KIA|SIA)[0-9A-Z]{16}'
print_matches "github-token" '(github_pat_[A-Za-z0-9_]{20,255}|gh[pousr]_[A-Za-z0-9_]{20,255})'
print_matches "google-api-key" 'AIza[0-9A-Za-z_-]{35}'
print_matches "google-oauth-access-token" 'ya29\.[A-Za-z0-9._-]{20,}'
print_matches "google-refresh-token" '1//[A-Za-z0-9._-]{20,}'
print_matches "jwt" 'eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}'
print_matches "slack-token" 'xox[baprs]-[A-Za-z0-9-]{10,}'
print_matches "openai-key" 'sk-[A-Za-z0-9]{20,}'
print_matches "generic-assignment" '(?i)\b(api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|private[_-]?key|secret[_-]?key|password|passwd|pwd|credential)\b[A-Za-z0-9_ .-]{0,30}[:=][[:space:]]*["'\'']?[A-Za-z0-9_./+=:-]{16,}'

dangerous_files="$("${RG[@]}" --files --hidden "${EXCLUDES[@]}" | "${RG[@]}" '(^|/)(\.env($|\.)|.*credentials.*|.*secret.*|.*token.*|id_rsa|id_ed25519|known_hosts|.*\.pem$|.*\.key$|.*\.p12$|.*\.pfx$|.*netrc.*)' || true)"
if [[ -n "$dangerous_files" ]]; then
  FOUND=1
  echo
  echo "[sensitive-file-name]"
  printf '%s\n' "$dangerous_files" | sort -u
fi

if [[ "$FOUND" -eq 1 ]]; then
  echo
  echo "Potential secrets found."
  exit 1
fi

echo "No potential secrets found."
