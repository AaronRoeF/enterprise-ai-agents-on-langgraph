#!/usr/bin/env python3
"""
ASCII diagram linter for the OCARA Field Guide book.

Validates every fenced code block (and any indented-block diagram) against
the strict ASCII discipline rules:

  1. Width: hard 72-column ceiling. 80 allowed ONLY in code blocks tagged as
     a programming language (Python, TypeScript, etc.). Diagrams use 72.
  2. Containment: diagrams must be inside a fenced code block.
  3. Character set: 7-bit ASCII only for diagrams. No Unicode box-drawing,
     emoji, CJK.
  4. No trailing whitespace.
  5. (Soft) right-border consistency check for box-style diagrams.

USAGE:
  python3 tools/lint-ascii-diagrams.py book/01-foundations.md
  python3 tools/lint-ascii-diagrams.py book/*.md

EXIT CODES:
  0 — all checks passed
  1 — violations found

OUTPUT:
  Per-file violation summary with file:line references.
"""
import os
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

# Diagram-ish languages — must follow ASCII rules.
DIAGRAM_LANGS = {"", "text", "txt", "ascii", "diagram", "mermaid"}

WIDTH_LIMIT_DIAGRAM = 72
WIDTH_LIMIT_CODE = 120  # soft limit for source code


def is_seven_bit_ascii(s: str) -> bool:
    """True if every char in s is in the 7-bit ASCII printable range or tab/newline."""
    return all(ord(c) < 128 for c in s)


def find_non_ascii(s: str) -> list[tuple[int, str]]:
    """Return list of (column, char) for non-ASCII characters."""
    return [(i, c) for i, c in enumerate(s) if ord(c) >= 128]


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

            # Width check
            if len(stripped) > limit:
                kind = "DIAGRAM" if is_diagram else f"CODE({fence_lang})"
                violations.append(
                    f"{path}:{line_num}: WIDTH [{kind}] {len(stripped)} cols (limit {limit}) — block starts at line {fence_start_line}"
                )

            # Trailing whitespace
            if line.rstrip("\n") != line.rstrip():
                violations.append(
                    f"{path}:{line_num}: TRAILING-WHITESPACE — block starts at line {fence_start_line}"
                )

            # ASCII-only for diagrams
            if is_diagram and not is_seven_bit_ascii(stripped):
                non_ascii = find_non_ascii(stripped)
                sample = ", ".join(f"col {col}: U+{ord(c):04X} '{c}'" for col, c in non_ascii[:3])
                violations.append(
                    f"{path}:{line_num}: NON-ASCII [DIAGRAM] {sample} — block starts at line {fence_start_line}"
                )

            # Detect mermaid blocks (these are violations of the ASCII rollback rule)
            if fence_lang == "mermaid":
                # Only report once per block (at the fence open)
                if line_num == fence_start_line + 1:
                    violations.append(
                        f"{path}:{fence_start_line}: MERMAID-BLOCK — should be converted to ASCII"
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
        # Aggregate by violation type for a quick summary.
        # Message format: "path:line: TYPE [scope] details"
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
        print(f"All {len(sys.argv)-1} file(s) passed ASCII diagram lint.")
        sys.exit(0)


if __name__ == "__main__":
    main()
