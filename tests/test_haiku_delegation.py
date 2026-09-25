"""Regression guards for the "delegate to Haiku" mechanism.

These are documentation/packaging consistency checks, not a functional test of
the Agent tool itself (that can't be exercised from a unit test — there's no
Agent tool inside a pytest run). What they *do* guard against:

- the fallback section (for hosts with a generic Agent/Task tool but no
  .claude/agents/*.md subagent, e.g. Cowork) silently getting removed or
  edited into something that no longer names the required pieces
  (general-purpose, model: "haiku", self-contained prompt)
- the Claude Code path (.claude/agents/morning-briefing.md, still pinned to
  Haiku, still pointed at from CLAUDE.md) being broken by that same edit
- the packaged plugin/ and .skill copies drifting from the canonical source
  after someone edits SKILL.md and forgets to re-run tools/package_skill.py

The actual "does a Haiku subagent successfully pull mail and render a board"
claim was verified manually against a live Microsoft 365 connector (see the
README changelog entry for 1.3.8) — that's not something a CI-safe unit test
can reproduce without live credentials and a real mailbox.
"""

import pathlib
import re
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / "morning-briefing" / "SKILL.md"
CLAUDE_MD = ROOT / "CLAUDE.md"
AGENT_SOURCE = ROOT / ".claude" / "agents" / "morning-briefing.md"
PLUGIN_SKILL = ROOT / "plugin" / "skills" / "morning-briefing" / "SKILL.md"
PLUGIN_AGENT = ROOT / "plugin" / "agents" / "morning-briefing.md"
PACKAGE = ROOT / "morning-briefing.skill"
README = ROOT / "README.md"


class HaikuDelegationTests(unittest.TestCase):
    def test_skill_documents_the_generic_agent_fallback(self):
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("Delegate to a cheaper model when possible", skill)
        for phrase in [
            "general-purpose",
            'model: "haiku"',
            "no memory of the parent session",
            "fully self-contained",
            ".claude/agents/morning-briefing.md",
        ]:
            self.assertIn(phrase, skill, f"missing {phrase!r} from the delegation section")

    def test_claude_md_points_at_both_delegation_paths(self):
        claude_md = CLAUDE_MD.read_text(encoding="utf-8")
        self.assertIn(".claude/agents/morning-briefing.md", claude_md)
        self.assertIn("Delegate to a cheaper model when possible", claude_md)

    def test_claude_code_subagent_still_pinned_to_haiku(self):
        # Regression guard: the fallback section is additive and must not
        # have touched the actual Claude Code subagent definition.
        agent = AGENT_SOURCE.read_text(encoding="utf-8")
        self.assertRegex(agent, r"(?m)^model:\s*haiku\s*$")
        self.assertIn("morning-briefing/SKILL.md", agent)

    def test_plugin_copies_match_canonical_source(self):
        self.assertTrue(PLUGIN_SKILL.exists(), "run tools/package_skill.py")
        self.assertTrue(PLUGIN_AGENT.exists(), "run tools/package_skill.py")
        self.assertEqual(PLUGIN_SKILL.read_bytes(), SKILL.read_bytes())
        self.assertEqual(PLUGIN_AGENT.read_bytes(), AGENT_SOURCE.read_bytes())

    def test_packaged_zip_contains_the_new_section(self):
        with zipfile.ZipFile(PACKAGE) as archive:
            packaged = archive.read("morning-briefing/SKILL.md").decode("utf-8")
        self.assertIn("Delegate to a cheaper model when possible", packaged)

    def test_version_bumped_and_matches_readme_badge(self):
        skill = SKILL.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        skill_version = re.search(r'(?m)^version:\s*([\d.]+)\s*$', skill).group(1)
        badge_version = re.search(
            r"badge/version-([\d.]+)-blue", readme
        ).group(1)
        changelog_top_version = re.search(
            r"\|\s*\*\*([\d.]+)\*\*\s*\|", readme
        ).group(1)
        self.assertEqual(skill_version, badge_version)
        self.assertEqual(skill_version, changelog_top_version)
        # This specific change landed in 1.3.8 — guard against a stale bump.
        parts = tuple(int(p) for p in skill_version.split("."))
        self.assertGreaterEqual(parts, (1, 3, 8))


if __name__ == "__main__":
    unittest.main()
