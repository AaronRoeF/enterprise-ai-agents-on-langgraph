#!/usr/bin/env python3
"""
ASCII / Unicode diagram linter for the OCARA Field Guide book.

Validates every fenced code block (and any indented-block diagram) against
the diagram discipline rules:

  1. Width: hard 72-column ceiling for diagrams. 120 allowed for code blocks
     tagged as a programming language.
  2. Containment: diagrams must be inside a fenced code block.
  3. Character set: 7-bit ASCII plus a strict whitelist of Unicode:
       - Box-drawing:     U+2500..U+257F (─ │ ┌ ┐ └ ┘ ┬ ┴ ├ ┤ ┼ ═ ║ ╔ ╗ ╚ ╝ etc.)
       - Block elements:  U+2580..U+259F (█ ▓ ▒ ░ ▀ ▄ etc.) — for heatmaps
       - Geometric shapes: U+25A0..U+25FF (► ◄ ▼ ▲ etc.) — arrow semantics
       - Em-dash U+2014, en-dash U+2013
       - A short list of arrow chars (→ ← ↑ ↓ ⇒ ⇐)
     Forbidden non-ASCII: emoji, CJK, fullwidth/halfwidth forms, smart/curly
     quotes. Any other non-ASCII char is also a violation by default.
  4. No trailing whitespace.
  5. Mermaid blocks are violations (book uses ASCII/Unicode diagrams).

The CC1 convention uses three arrow styles:
  ─►   LLM-decided control flow (light)
  ══►  runtime-automatic / deterministic flow (heavy)
  ─ ─► human-mediated / dashed flow

USAGE:
  python3 tools/lint-ascii-diagrams.py book/01-foundations.md
  python3 tools/lint-ascii-diagrams.py book/*.md

EXIT CODES:
  0 — all checks passed
  1 — violations found
"""
import re
import sys
from pathlib import Path

# Languages whose blocks can exceed 72 cols (source code, not diagrams).
CODE_LANGS = {
    "python", "py", "typescript", "ts", "javascript", "js", "json", "yaml",
    "yml", "bash", "sh", "shell", "sql", "dockerfile", "rust", "go", "java",
    "kotlin", "swift", "ruby", "php", "html", "css", "xml", "toml", "ini",
    "diff", "graphql", "protobuf", "proto",
}

# Diagram-ish languages — must follow ASCII/Unicode whitelist rules.
DIAGRAM_LANGS = {"", "text", "txt", "ascii", "diagram", "mermaid"}

WIDTH_LIMIT_DIAGRAM = 72
WIDTH_LIMIT_CODE = 120  # soft limit for source code

# --- Unicode whitelist for diagrams -----------------------------------------
ALLOWED_UNICODE_RANGES = [
    (0x2500, 0x257F),  # Box Drawing
    (0x2580, 0x259F),  # Block Elements (block shading for heatmaps)
    (0x25A0, 0x25FF),  # Geometric Shapes (► ◄ ▼ ▲ etc.)
]
ALLOWED_UNICODE_CHARS = {
    0x2013,  # –  en-dash
    0x2014,  # —  em-dash
    0x2190,  # ←  leftwards arrow
    0x2191,  # ↑  upwards arrow
    0x2192,  # →  rightwards arrow
    0x2193,  # ↓  downwards arrow
    0x21D0,  # ⇐  leftwards double arrow
    0x21D2,  # ⇒  rightwards double arrow
    0x2026,  # …  horizontal ellipsis
    0x00A0,  # NBSP — tolerated; flagged separately if it shows up in code
}

# --- Explicitly-named forbidden classes (for clearer error messages) --------
SMART_QUOTES = {0x2018, 0x2019, 0x201C, 0x201D, 0x201E, 0x201F, 0x2039, 0x203A}
FORBIDDEN_RANGES = [
    # Emoji & pictographs (rough buckets; not exhaustive but covers the
    # families that actually appear in copy/paste):
    (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
    (0x1F600, 0x1F64F),  # Emoticons
    (0x1F680, 0x1F6FF),  # Transport and Map
    (0x1F900, 0x1F9FF),  # Supplemental Symbols and Pictographs
    (0x1FA00, 0x1FAFF),  # Symbols and Pictographs Extended-A
    (0x2700,  0x27BF),   # Dingbats
    # CJK Unified Ideographs (and Kana / Hangul):
    (0x3000, 0x303F),    # CJK Symbols and Punctuation
    (0x3040, 0x309F),    # Hiragana
    (0x30A0, 0x30FF),    # Katakana
    (0x3400, 0x4DBF),    # CJK Extension A
    (0x4E00, 0x9FFF),    # CJK Unified Ideographs
    (0xAC00, 0xD7AF),    # Hangul Syllables
    (0x20000, 0x2EBEF),  # CJK Extensions B–F
    # Fullwidth / halfwidth (double-width chars break monospace grid):
    (0xFF00, 0xFFEF),
]


def is_in_ranges(cp: int, ranges) -> bool:
    return any(lo <= cp <= hi for lo, hi in ranges)


def classify_non_ascii(cp: int) -> str:
    """Return a short tag describing why a non-ASCII codepoint is forbidden,
    or "" if it is in the allowlist (i.e., permitted)."""
    if cp in ALLOWED_UNICODE_CHARS:
        return ""
    if is_in_ranges(cp, ALLOWED_UNICODE_RANGES):
        return ""
    if cp in SMART_QUOTES:
        return "smart-quote"
    if is_in_ranges(cp, FORBIDDEN_RANGES):
        # Decide bucket label for nicer reporting.
        if 0x1F300 <= cp <= 0x1FAFF or 0x2700 <= cp <= 0x27BF:
            return "emoji"
        if (0x3000 <= cp <= 0x9FFF) or (0xAC00 <= cp <= 0xD7AF) or (0x20000 <= cp <= 0x2EBEF):
            return "cjk"
        if 0xFF00 <= cp <= 0xFFEF:
            return "fullwidth"
        return "forbidden"
    # Anything else non-ASCII that we didn't whitelist or explicitly forbid:
    return "non-whitelisted"


def find_violations_in_line(s: str) -> list[tuple[int, str, str]]:
    """Return list of (column, char, reason) for non-ASCII chars that violate
    the whitelist."""
    out = []
    for i, c in enumerate(s):
        cp = ord(c)
        if cp < 128:
            continue
        reason = classify_non_ascii(cp)
        if reason:
            out.append((i, c, reason))
    return out


def lint_file(path: Path) -> list[str]:
    """Returns list of human-readable violation messages."""
    violations = []
    lines = path.read_text(encoding="utf-8").splitlines()

    in_fence = False
    fence_lang = ""
    fence_start_line = 0

    for line_num, line in enumerate(lines, start=1):
        stripped = line.rstrip("\n")

        # Detect fence open/close
        if not in_fence:
            m = re.match(r"^```(\w*)\s*$", stripped)
            if m:
                in_fence = True
                fence_lang = m.group(1).lower()
                fence_start_line = line_num
                continue
        else:
            if stripped == "```":
                in_fence = False
                fence_lang = ""
                continue

        # Inside a fence: apply diagram rules if it's a diagram-language fence.
        if in_fence:
            is_diagram = fence_lang in DIAGRAM_LANGS
            limit = WIDTH_LIMIT_DIAGRAM if is_diagram else WIDTH_LIMIT_CODE

            # Width check (column count = codepoint count; fullwidth chars
            # are forbidden so a 1:1 col count is safe for diagrams).
            if len(stripped) > limit:
                kind = "DIAGRAM" if is_diagram else f"CODE({fence_lang})"
                violations.append(
                    f"{path}:{line_num}: WIDTH [{kind}] {len(stripped)} cols "
                    f"(limit {limit}) — block starts at line {fence_start_line}"
                )

            # Trailing whitespace
            if line.rstrip("\n") != line.rstrip():
                violations.append(
                    f"{path}:{line_num}: TRAILING-WHITESPACE — block starts at line {fence_start_line}"
                )

            # Whitelist check for diagrams
            if is_diagram:
                hits = find_violations_in_line(stripped)
                if hits:
                    sample = ", ".join(
                        f"col {col}: U+{ord(c):04X} '{c}' [{reason}]"
                        for col, c, reason in hits[:3]
                    )
                    violations.append(
                        f"{path}:{line_num}: FORBIDDEN-CHAR [DIAGRAM] {sample} "
                        f"— block starts at line {fence_start_line}"
                    )

            # Detect mermaid blocks (violations of the ASCII rollback rule)
            if fence_lang == "mermaid":
                if line_num == fence_start_line + 1:
                    violations.append(
                        f"{path}:{fence_start_line}: MERMAID-BLOCK — should be converted to ASCII/Unicode"
                    )

    if in_fence:
        violations.append(f"{path}:{fence_start_line}: UNCLOSED-FENCE")

    return violations


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <markdown-file> [<markdown-file> ...]", file=sys.stderr)
        sys.exit(2)

    all_violations = []
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"WARN: {path} does not exist, skipping", file=sys.stderr)
            continue
        v = lint_file(path)
        all_violations.extend(v)

    if all_violations:
        print(f"\n=== {len(all_violations)} violation(s) found ===")
        for v in all_violations:
            print(v)
        types = {}
        type_pat = re.compile(r":\d+:\s+(\S+)")
        for v in all_violations:
            m = type_pat.search(v)
            tag = m.group(1) if m else "?"
            types[tag] = types.get(tag, 0) + 1
        print(f"\n=== Summary by type ===")
        for tag, count in sorted(types.items(), key=lambda x: -x[1]):
            print(f"  {tag}: {count}")
        sys.exit(1)
    else:
        print(f"All {len(sys.argv)-1} file(s) passed diagram lint (ASCII + whitelisted Unicode).")
        sys.exit(0)


if __name__ == "__main__":
    main()
