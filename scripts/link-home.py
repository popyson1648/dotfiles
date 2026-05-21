#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LinkSpec:
    name: str
    target: str


LINKS = [
    LinkSpec(".zshenv", "/home/popyson/doc/dotfiles/.config/zsh/.zshenv"),
    LinkSpec(".agents", "/home/popyson/.config/agents"),
    LinkSpec(".leetcode", "/home/popyson/Document/LeetCode"),
    LinkSpec(".vimrc", "/home/popyson/.config/vim/.vimrc"),
    LinkSpec("dev", "Document/Development"),
    LinkSpec(".zshrc", "/home/popyson/doc/dotfiles/.config/zsh/.zshrc"),
    LinkSpec("win_popyson", "/mnt/c/Users/popyson"),
    LinkSpec(".tmux.conf", "/home/popyson/.config/tmux/.tmux.conf"),
    LinkSpec(".config", "/home/popyson/doc/dotfiles/.config"),
    LinkSpec("doc", "/home/popyson/Document"),
    LinkSpec(".vim", "/home/popyson/doc/dotfiles/.config/vim/.vim"),
]


@dataclass
class Summary:
    ok: int = 0
    absent: int = 0
    created: int = 0
    missing_targets: int = 0
    conflicts: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the configured symlinks under $HOME."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_const",
        dest="mode",
        const="check",
        help="only report link status; do not create links",
    )
    mode.add_argument(
        "--dry-run",
        action="store_const",
        dest="mode",
        const="dry-run",
        help="print what would be created; do not create links",
    )
    parser.set_defaults(mode="apply")
    return parser.parse_args()


def target_path(link_path: Path, target: str) -> Path:
    path = Path(target)
    if path.is_absolute():
        return path
    return link_path.parent / path


def same_target(link_path: Path, expected_target: str) -> bool:
    current_target = os.readlink(link_path)
    if current_target == expected_target:
        return True

    current_path = target_path(link_path, current_target)
    expected_path = target_path(link_path, expected_target)

    if not current_path.exists() or not expected_path.exists():
        return False

    return current_path.resolve() == expected_path.resolve()


def print_summary(summary: Summary, mode: str) -> None:
    print(
        "\nSummary: "
        f"ok={summary.ok} "
        f"absent={summary.absent} "
        f"created={summary.created} "
        f"missing_targets={summary.missing_targets} "
        f"conflicts={summary.conflicts} "
        f"mode={mode}"
    )


def process_link(home: Path, spec: LinkSpec, mode: str, summary: Summary) -> None:
    link_path = home / spec.name

    if link_path.is_symlink():
        current_target = os.readlink(link_path)
        if same_target(link_path, spec.target):
            print(f"ok:      {link_path} -> {current_target}")
            summary.ok += 1
        else:
            print(
                f"conflict:{link_path} -> {current_target} "
                f"(expected {spec.target})",
                file=sys.stderr,
            )
            summary.conflicts += 1
        return

    if link_path.exists():
        print(f"conflict:{link_path} exists and is not a symlink", file=sys.stderr)
        summary.conflicts += 1
        return

    if not target_path(link_path, spec.target).exists():
        print(
            f"missing: {link_path} target does not exist: {spec.target}",
            file=sys.stderr,
        )
        summary.missing_targets += 1

    if mode == "apply":
        try:
            link_path.symlink_to(spec.target)
        except OSError as exc:
            print(
                f"failed:  could not create {link_path} -> {spec.target}: {exc}",
                file=sys.stderr,
            )
            summary.conflicts += 1
            return
        print(f"created: {link_path} -> {spec.target}")
        summary.created += 1
    elif mode == "check":
        print(f"absent:  {link_path} -> {spec.target}")
        summary.absent += 1
    elif mode == "dry-run":
        print(f"would-create: {link_path} -> {spec.target}")
        summary.absent += 1
    else:
        raise ValueError(f"unknown mode: {mode}")


def main() -> int:
    args = parse_args()
    home = Path.home()
    summary = Summary()

    for spec in LINKS:
        process_link(home, spec, args.mode, summary)

    print_summary(summary, args.mode)

    if summary.conflicts:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
