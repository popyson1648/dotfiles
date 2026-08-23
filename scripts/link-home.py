#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import platform as platform_module
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence


CONFIG_ENTRIES = (
    "agents", "bat", "claude", "coc", "create-next-app-nodejs", "dlv",
    "emacs", "fish", "fontconfig", "git", "github", "karabiner",
    "mimeapps.list", "mise", "nextjs-nodejs", "nix", "nvim", "starship",
    "tmux", "vim", "wezterm", "zed", "zellij", "zsh",
)

HOME_LINKS = {
    ".agents": "agents",
    ".tmux.conf": "tmux/.tmux.conf",
    ".vim": "vim/.vim",
    ".vimrc": "vim/.vimrc",
    ".zshenv": "zsh/.zshenv",
    ".zshrc": "zsh/.zshrc",
}


@dataclass(frozen=True)
class LinkSpec:
    destination: Path
    source: Path
    required: bool = True
    label: str = "common"


@dataclass
class Summary:
    ok: int = 0
    absent: int = 0
    created: int = 0
    skipped: int = 0
    missing_targets: int = 0
    conflicts: int = 0
    rolled_back: int = 0

    @property
    def has_errors(self) -> bool:
        return bool(self.missing_targets or self.conflicts)


def repository_root() -> Path:
    return Path(__file__).resolve().parent.parent


def detect_platform(
    *,
    system: str | None = None,
    osrelease: str | None = None,
    environ: Mapping[str, str] | None = None,
) -> str:
    system_name = system or platform_module.system()
    environment = os.environ if environ is None else environ

    if system_name == "Darwin":
        return "macos"
    if system_name != "Linux":
        raise RuntimeError(f"unsupported operating system: {system_name}")

    release = osrelease
    if release is None:
        try:
            release = Path("/proc/sys/kernel/osrelease").read_text(encoding="utf-8")
        except OSError:
            release = platform_module.release()

    if "microsoft" in release.casefold() or "WSL_INTEROP" in environment:
        return "wsl"
    return "linux"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Link this repository's dotfiles into the current home directory."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check", action="store_const", dest="mode", const="check",
        help="verify that all applicable links are installed",
    )
    mode.add_argument(
        "--dry-run", action="store_const", dest="mode", const="dry-run",
        help="show changes without creating links",
    )
    parser.add_argument(
        "--windows-home", type=Path,
        help="Windows home to link under WSL (also read from DOTFILES_WINDOWS_HOME)",
    )
    parser.set_defaults(mode="apply")
    return parser.parse_args()


def _absolute_link_target(link: Path, target: str | os.PathLike[str]) -> Path:
    target_path = Path(target)
    if not target_path.is_absolute():
        target_path = link.parent / target_path
    return Path(os.path.abspath(target_path))


def link_matches(destination: Path, source: Path) -> bool:
    if not destination.is_symlink():
        return False
    return _absolute_link_target(destination, os.readlink(destination)) == Path(
        os.path.abspath(source)
    )


def discover_windows_home(
    home: Path,
    explicit: Path | None,
    environ: Mapping[str, str] | None = None,
) -> Path | None:
    environment = os.environ if environ is None else environ
    configured = explicit or (
        Path(environment["DOTFILES_WINDOWS_HOME"])
        if environment.get("DOTFILES_WINDOWS_HOME")
        else None
    )
    if configured is not None:
        return configured

    same_name = Path("/mnt/c/Users") / home.name
    if same_name.is_dir():
        return same_name
    return None


def build_link_specs(
    repo: Path,
    home: Path,
    platform_name: str,
    *,
    windows_home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> list[LinkSpec]:
    repo = Path(os.path.abspath(repo))
    home = Path(os.path.abspath(home))
    config_source = repo / ".config"
    config_destination = home / ".config"

    specs: list[LinkSpec] = []
    if link_matches(config_destination, config_source):
        specs.append(LinkSpec(config_destination, config_source, label="legacy-config"))
    else:
        for name in CONFIG_ENTRIES:
            source = config_source / name
            if source.exists() or source.is_symlink():
                specs.append(LinkSpec(config_destination / name, source))

    for destination_name, source_name in HOME_LINKS.items():
        specs.append(LinkSpec(home / destination_name, config_source / source_name))

    if platform_name == "wsl":
        target = discover_windows_home(home, windows_home, environ)
        if target is not None:
            specs.append(
                LinkSpec(
                    home / f"win_{target.name}",
                    Path(os.path.abspath(target)),
                    required=False,
                    label="wsl",
                )
            )

    return specs


def inspect_links(specs: Sequence[LinkSpec], summary: Summary) -> list[LinkSpec]:
    pending: list[LinkSpec] = []
    for spec in specs:
        if not spec.source.exists():
            if spec.required:
                print(
                    f"missing:  required target does not exist: {spec.source}",
                    file=sys.stderr,
                )
                summary.missing_targets += 1
            else:
                print(f"skipped:  optional target does not exist: {spec.source}")
                summary.skipped += 1
            continue

        if spec.destination.is_symlink():
            if link_matches(spec.destination, spec.source):
                print(f"ok:       {spec.destination} -> {os.readlink(spec.destination)}")
                summary.ok += 1
            else:
                print(
                    f"conflict: {spec.destination} is linked to "
                    f"{os.readlink(spec.destination)} (expected {spec.source})",
                    file=sys.stderr,
                )
                summary.conflicts += 1
            continue

        if spec.destination.exists():
            print(
                f"conflict: {spec.destination} exists and is not a symlink",
                file=sys.stderr,
            )
            summary.conflicts += 1
            continue

        pending.append(spec)
    return pending


def apply_links(specs: Sequence[LinkSpec], summary: Summary) -> bool:
    created_links: list[Path] = []
    created_directories: list[Path] = []
    try:
        for spec in specs:
            parent = spec.destination.parent
            if not parent.exists():
                parent.mkdir(parents=True)
                created_directories.append(parent)
            spec.destination.symlink_to(
                spec.source, target_is_directory=spec.source.is_dir()
            )
            created_links.append(spec.destination)
            summary.created += 1
            print(f"created:  {spec.destination} -> {spec.source}")
    except OSError as exc:
        print(f"failed:   could not create links: {exc}", file=sys.stderr)
        summary.conflicts += 1
        for link in reversed(created_links):
            try:
                link.unlink()
                summary.rolled_back += 1
            except OSError as rollback_error:
                print(
                    f"failed:   could not roll back {link}: {rollback_error}",
                    file=sys.stderr,
                )
        for directory in reversed(created_directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        return False
    return True


def print_summary(summary: Summary, mode: str, platform_name: str) -> None:
    print(
        "\nSummary: "
        f"ok={summary.ok} absent={summary.absent} created={summary.created} "
        f"skipped={summary.skipped} missing_targets={summary.missing_targets} "
        f"conflicts={summary.conflicts} rolled_back={summary.rolled_back} "
        f"mode={mode} platform={platform_name}"
    )


def run(
    *,
    repo: Path,
    home: Path,
    platform_name: str,
    mode: str,
    windows_home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> int:
    summary = Summary()
    specs = build_link_specs(
        repo, home, platform_name, windows_home=windows_home, environ=environ
    )
    pending = inspect_links(specs, summary)

    if summary.has_errors:
        print_summary(summary, mode, platform_name)
        return 1

    if mode == "check":
        for spec in pending:
            print(f"absent:   {spec.destination} -> {spec.source}", file=sys.stderr)
        summary.absent = len(pending)
        print_summary(summary, mode, platform_name)
        return 1 if pending else 0

    if mode == "dry-run":
        for spec in pending:
            print(f"would-create: {spec.destination} -> {spec.source}")
        summary.absent = len(pending)
        print_summary(summary, mode, platform_name)
        return 0

    if mode != "apply":
        raise ValueError(f"unknown mode: {mode}")

    apply_links(pending, summary)
    print_summary(summary, mode, platform_name)
    return 1 if summary.has_errors else 0


def main() -> int:
    args = parse_args()
    try:
        platform_name = detect_platform()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    return run(
        repo=repository_root(),
        home=Path.home(),
        platform_name=platform_name,
        mode=args.mode,
        windows_home=args.windows_home,
    )


if __name__ == "__main__":
    raise SystemExit(main())
