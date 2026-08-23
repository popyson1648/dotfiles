#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).with_name("link-home.py")
SPEC = importlib.util.spec_from_file_location("link_home", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
link_home = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = link_home
SPEC.loader.exec_module(link_home)


class LinkHomeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.repo = self.root / "repo with spaces"
        self.home = self.root / "home with spaces"
        self.home.mkdir(parents=True)
        self._create_repository()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _create_repository(self) -> None:
        config = self.repo / ".config"
        for directory in ("agents", "nvim", "tmux", "vim", "zsh"):
            (config / directory).mkdir(parents=True, exist_ok=True)
        for relative_path in link_home.HOME_LINKS.values():
            target = config / relative_path
            if target.suffix or target.name.startswith("."):
                target.touch()

    def run_linker(
        self,
        mode: str = "apply",
        platform_name: str = "linux",
        windows_home: Path | None = None,
    ) -> int:
        return link_home.run(
            repo=self.repo,
            home=self.home,
            platform_name=platform_name,
            mode=mode,
            windows_home=windows_home,
            environ={},
        )

    def test_detects_linux_macos_and_wsl(self) -> None:
        self.assertEqual(
            link_home.detect_platform(system="Linux", osrelease="6.8-generic", environ={}),
            "linux",
        )
        self.assertEqual(
            link_home.detect_platform(system="Darwin", osrelease="", environ={}),
            "macos",
        )
        self.assertEqual(
            link_home.detect_platform(
                system="Linux", osrelease="5.15.0-microsoft-standard-WSL2", environ={}
            ),
            "wsl",
        )
        self.assertEqual(
            link_home.detect_platform(
                system="Linux", osrelease="6.8-generic", environ={"WSL_INTEROP": "x"}
            ),
            "wsl",
        )

    def test_rejects_unsupported_platform(self) -> None:
        with self.assertRaises(RuntimeError):
            link_home.detect_platform(system="Windows", osrelease="", environ={})

    def test_apply_is_idempotent_and_check_passes(self) -> None:
        self.assertEqual(self.run_linker(), 0)
        self.assertTrue((self.home / ".config" / "nvim").is_symlink())
        self.assertEqual(
            (self.home / ".config" / "nvim").readlink(),
            self.repo / ".config" / "nvim",
        )
        self.assertEqual(self.run_linker(), 0)
        self.assertEqual(self.run_linker(mode="check"), 0)

    def test_dry_run_does_not_modify_home(self) -> None:
        self.assertEqual(self.run_linker(mode="dry-run"), 0)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_check_fails_when_links_are_absent(self) -> None:
        self.assertEqual(self.run_linker(mode="check"), 1)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_conflict_prevents_all_changes(self) -> None:
        (self.home / ".zshenv").write_text("existing\n", encoding="utf-8")
        self.assertEqual(self.run_linker(), 1)
        self.assertFalse((self.home / ".config").exists())
        self.assertEqual(
            (self.home / ".zshenv").read_text(encoding="utf-8"), "existing\n"
        )

    def test_missing_required_target_prevents_all_changes(self) -> None:
        (self.repo / ".config" / "zsh" / ".zshenv").unlink()
        self.assertEqual(self.run_linker(), 1)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_wsl_adds_existing_windows_home_link(self) -> None:
        windows_home = self.root / "Windows User"
        windows_home.mkdir()
        self.assertEqual(
            self.run_linker(platform_name="wsl", windows_home=windows_home), 0
        )
        destination = self.home / "win_Windows User"
        self.assertTrue(destination.is_symlink())
        self.assertEqual(destination.readlink(), windows_home)

    def test_non_wsl_does_not_add_windows_home_link(self) -> None:
        windows_home = self.root / "Windows User"
        windows_home.mkdir()
        specs = link_home.build_link_specs(
            self.repo,
            self.home,
            "macos",
            windows_home=windows_home,
            environ={},
        )
        self.assertFalse(any(spec.label == "wsl" for spec in specs))

    def test_missing_optional_wsl_target_is_skipped(self) -> None:
        windows_home = self.root / "missing-windows-home"
        self.assertEqual(
            self.run_linker(platform_name="wsl", windows_home=windows_home), 0
        )
        self.assertFalse((self.home / "win_missing-windows-home").exists())

    def test_existing_legacy_config_link_is_accepted(self) -> None:
        (self.home / ".config").symlink_to(
            self.repo / ".config", target_is_directory=True
        )
        self.assertEqual(self.run_linker(), 0)
        self.assertEqual(self.run_linker(mode="check"), 0)

    def test_creation_failure_rolls_back_created_links(self) -> None:
        original = Path.symlink_to
        calls = 0

        def fail_second_call(path: Path, *args: object, **kwargs: object) -> None:
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("simulated failure")
            original(path, *args, **kwargs)

        with mock.patch.object(Path, "symlink_to", autospec=True, side_effect=fail_second_call):
            self.assertEqual(self.run_linker(), 1)

        self.assertFalse(any(path.is_symlink() for path in self.home.rglob("*")))


if __name__ == "__main__":
    unittest.main()
