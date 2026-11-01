#!/usr/bin/env python3
"""Static validator for the GAME STUDIO skill/plugin.

Usage: python3 scripts/validate.py [path-to-game-studio-dir]

Checks: plugin manifest, root SKILL.md frontmatter, the 30 specialist agents
(numbering, frontmatter, unique names, tools, required sections, shared
protocol), that SKILL.md's roster matches the agent files, that every
reference/template SKILL.md mentions exists, and that no agent names a
non-existent reference. Exit code 0 = all checks passed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

EXPECTED_AGENTS = [
    "executive-producer", "project-manager", "game-director", "creative-director",
    "technical-director", "lead-game-designer", "systems-designer", "level-designer",
    "narrative-quest-designer", "economy-designer", "ux-designer", "ui-visual-designer",
    "ui-engineer", "art-director", "concept-artist", "character-artist",
    "environment-artist", "props-artist", "technical-artist", "animator",
    "vfx-lighting-artist", "gameplay-programmer", "ai-programmer",
    "physics-combat-programmer", "multiplayer-backend-engineer",
    "tools-build-devops-engineer", "sound-designer", "composer", "qa-engineer",
    "publishing-marketing-specialist",
]
EXPECTED_FILES = {
    1: "01-executive-producer.md", 2: "02-project-manager.md", 3: "03-game-director.md",
    4: "04-creative-director.md", 5: "05-technical-director.md", 6: "06-lead-game-designer.md",
    7: "07-systems-designer.md", 8: "08-level-designer.md", 9: "09-narrative-quest-designer.md",
    10: "10-economy-designer.md", 11: "11-ux-designer.md", 12: "12-ui-visual-designer.md",
    13: "13-ui-engineer.md", 14: "14-art-director.md", 15: "15-concept-artist.md",
    16: "16-character-artist.md", 17: "17-environment-artist.md", 18: "18-props-artist.md",
    19: "19-technical-artist.md", 20: "20-animator.md", 21: "21-vfx-lighting-artist.md",
    22: "22-gameplay-programmer.md", 23: "23-ai-programmer.md",
    24: "24-physics-combat-programmer.md", 25: "25-multiplayer-backend-engineer.md",
    26: "26-tools-build-devops-engineer.md", 27: "27-sound-designer.md", 28: "28-composer.md",
    29: "29-qa-engineer.md", 30: "30-publishing-marketing-specialist.md",
}
KNOWN_TOOLS = {
    "Read", "Write", "Edit", "Bash", "Glob", "Grep", "WebFetch", "WebSearch",
    "NotebookEdit", "TodoWrite", "Agent", "Task",
}
VALID_MODELS = {"inherit", "sonnet", "opus", "haiku", "fable"}
VALID_COLORS = {"red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"}
REQUIRED_AGENT_SECTIONS = [
    "## Responsibilities", "## Inputs", "## Outputs", "## Method",
    "## Quality checklist", "## Collaboration", "## Studio Protocol",
]
REQUIRED_REFERENCES = [
    "development-pipeline.md", "coding-standards.md", "art-pipeline.md",
    "qa-standards.md", "project-management.md", "engine-guidelines.md",
]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.passed = 0

    def ok(self, cond: bool, msg: str, warn: bool = False) -> bool:
        if cond:
            self.passed += 1
        elif warn:
            self.warnings.append(msg)
        else:
            self.errors.append(msg)
        return cond


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    """Minimal YAML frontmatter parser (flat `key: value` pairs, folded lines)."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    block, body = text[4:end], text[end + 5:]
    data: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m and not line.startswith(" "):
            key = m.group(1)
            data[key] = m.group(2).strip()
        elif key is not None:  # continuation / list item
            data[key] = (data[key] + " " + line.strip()).strip()
    for k, v in data.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            data[k] = v[1:-1]
    return data, body


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
    r = Report()
    print(f"Validating GAME STUDIO at: {root}")

    # --- plugin manifest
    manifest = root / ".claude-plugin" / "plugin.json"
    if r.ok(manifest.is_file(), ".claude-plugin/plugin.json missing"):
        try:
            pj = json.loads(manifest.read_text(encoding="utf-8"))
            r.ok(pj.get("name") == "game-studio", "plugin.json name must be 'game-studio'")
            r.ok(bool(pj.get("version")), "plugin.json version missing")
            r.ok("./" in (pj.get("skills") or []), "plugin.json skills must include './' (root SKILL.md)")
        except json.JSONDecodeError as e:
            r.ok(False, f"plugin.json invalid JSON: {e}")
    mp = root / ".claude-plugin" / "marketplace.json"
    if mp.is_file():
        try:
            json.loads(mp.read_text(encoding="utf-8"))
            r.ok(True, "")
        except json.JSONDecodeError as e:
            r.ok(False, f"marketplace.json invalid JSON: {e}")

    # --- SKILL.md
    skill = root / "SKILL.md"
    skill_text = ""
    if r.ok(skill.is_file(), "SKILL.md missing"):
        skill_text = skill.read_text(encoding="utf-8")
        fm = parse_frontmatter(skill_text)
        if r.ok(fm is not None, "SKILL.md frontmatter missing/invalid"):
            meta, body = fm
            r.ok(meta.get("name") == "game-studio", "SKILL.md name must be 'game-studio'")
            desc = meta.get("description", "")
            r.ok(80 <= len(desc) <= 1024, f"SKILL.md description length {len(desc)} not in 80..1024")
            r.ok(len(body.splitlines()) <= 500, "SKILL.md body > 500 lines (keep it lean)", warn=True)

    # --- agents
    agents_dir = root / "agents"
    names_seen: dict[str, str] = {}
    if r.ok(agents_dir.is_dir(), "agents/ directory missing"):
        files = sorted(p.name for p in agents_dir.glob("*.md"))
        r.ok(len(files) == 30, f"expected 30 agent files, found {len(files)}")
        for num, fname in EXPECTED_FILES.items():
            path = agents_dir / fname
            if not r.ok(path.is_file(), f"missing agent file agents/{fname}"):
                continue
            text = path.read_text(encoding="utf-8")
            fm = parse_frontmatter(text)
            if not r.ok(fm is not None, f"{fname}: frontmatter missing/invalid"):
                continue
            meta, body = fm
            name = meta.get("name", "")
            expected = EXPECTED_AGENTS[num - 1]
            r.ok(name == expected, f"{fname}: name '{name}' != expected '{expected}'")
            r.ok(bool(NAME_RE.match(name)), f"{fname}: name not kebab-case")
            r.ok(name not in names_seen, f"{fname}: duplicate name '{name}' (also {names_seen.get(name)})")
            names_seen[name] = fname
            desc = meta.get("description", "")
            r.ok(desc.startswith("GAME STUDIO"), f"{fname}: description should start with 'GAME STUDIO'")
            r.ok(60 <= len(desc) <= 600, f"{fname}: description length {len(desc)} not in 60..600")
            r.ok("Use " in desc or "use " in desc or "Mandatory" in desc,
                 f"{fname}: description should say when to use it")
            tools = [t.strip() for t in meta.get("tools", "").split(",") if t.strip()]
            r.ok(bool(tools), f"{fname}: tools list empty")
            unknown = [t for t in tools if t not in KNOWN_TOOLS]
            r.ok(not unknown, f"{fname}: unknown tools {unknown}")
            r.ok("Read" in tools, f"{fname}: every specialist needs Read")
            r.ok("Agent" not in tools and "Task" not in tools,
                 f"{fname}: specialists must not spawn agents (coordinator is the hub)")
            r.ok(meta.get("model", "inherit") in VALID_MODELS, f"{fname}: invalid model")
            r.ok(meta.get("color", "blue") in VALID_COLORS, f"{fname}: invalid color", warn=True)
            r.ok(body.lstrip().startswith(f"# {num:02d} "), f"{fname}: title should start with '# {num:02d} '")
            for sec in REQUIRED_AGENT_SECTIONS:
                r.ok(sec in body, f"{fname}: missing section '{sec}'")
            r.ok("STATUS: DONE | PARTIAL | BLOCKED" in body, f"{fname}: missing report format")
            for ref in re.findall(r"references/([\w-]+\.md)", body):
                r.ok((root / "references" / ref).is_file(), f"{fname}: references/{ref} does not exist")
            for tpl in re.findall(r"templates/([\w-]+\.md)", body):
                r.ok((root / "templates" / tpl).is_file(), f"{fname}: templates/{tpl} does not exist")
            # every implementer must be told to verify
            r.ok("VERIFICATION" in body and "NOT RUN" in body, f"{fname}: missing verification rule")

    # --- roster consistency SKILL.md <-> agents
    if skill_text:
        for name in EXPECTED_AGENTS:
            r.ok(f"`{name}`" in skill_text, f"SKILL.md roster does not mention `{name}`")
        roster = set(re.findall(r"^\|\s*\d{2}\s*\|\s*`([a-z0-9-]+)`", skill_text, re.M))
        r.ok(roster == set(EXPECTED_AGENTS),
             f"SKILL.md roster table mismatch: extra={sorted(roster - set(EXPECTED_AGENTS))} "
             f"missing={sorted(set(EXPECTED_AGENTS) - roster)}")
        for ref in sorted(set(re.findall(r"references/([\w-]+\.md)", skill_text))):
            r.ok((root / "references" / ref).is_file(), f"SKILL.md references missing file references/{ref}")
        for ref in REQUIRED_REFERENCES:
            r.ok((root / "references" / ref).is_file(), f"required reference references/{ref} missing")
            r.ok(f"references/{ref}" in skill_text, f"SKILL.md never tells when to read references/{ref}")
        for tpl in sorted(set(re.findall(r"templates/([\w-]+\.md)", skill_text))):
            r.ok((root / "templates" / tpl).is_file(), f"SKILL.md mentions missing templates/{tpl}")
        r.ok("game-studio:" in skill_text, "SKILL.md must explain the game-studio:<agent> subagent type")

    # --- README
    r.ok((root / "README.md").is_file(), "README.md missing")

    print(f"\nChecks passed: {r.passed}")
    for w in r.warnings:
        print(f"  WARN  {w}")
    for e in r.errors:
        print(f"  FAIL  {e}")
    if r.errors:
        print(f"\nRESULT: FAILED ({len(r.errors)} error(s), {len(r.warnings)} warning(s))")
        return 1
    print(f"\nRESULT: OK — 30/30 agents valid, skill + references consistent "
          f"({len(r.warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
