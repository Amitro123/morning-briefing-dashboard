#!/usr/bin/env python3
"""Build morning-briefing.skill and plugin/ from the canonical skill directory."""

from __future__ import annotations

import pathlib
import shutil
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / "morning-briefing"
AGENT_SOURCE = ROOT / ".claude" / "agents" / "morning-briefing.md"
OUTPUT = ROOT / "morning-briefing.skill"
PLUGIN_ROOT = ROOT / "plugin"
INCLUDE = (
    "SKILL.md",
    "scripts/render_board.py",
)


def build_skill_zip() -> None:
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in INCLUDE:
            path = SOURCE / relative
            data = path.read_bytes().replace(b"\r\n", b"\n")
            archive.writestr(f"morning-briefing/{relative.replace(chr(92), '/')}", data)
    print(OUTPUT)


def build_plugin_dir() -> None:
    plugin_skill_dir = PLUGIN_ROOT / "skills" / "morning-briefing"
    plugin_agent_dir = PLUGIN_ROOT / "agents"
    if plugin_skill_dir.exists():
        shutil.rmtree(plugin_skill_dir)
    plugin_agent_dir.mkdir(parents=True, exist_ok=True)

    for relative in INCLUDE:
        dest = plugin_skill_dir / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((SOURCE / relative).read_bytes())

    shutil.copyfile(AGENT_SOURCE, plugin_agent_dir / "morning-briefing.md")
    print(plugin_skill_dir)
    print(plugin_agent_dir / "morning-briefing.md")


def main() -> None:
    build_skill_zip()
    build_plugin_dir()


if __name__ == "__main__":
    main()
