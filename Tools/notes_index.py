#!/usr/bin/env python3
"""
notes_index.py - read the notes without reading the notes. Free tool (Tools\\TOOLS.md).

The matching notes have grown too large to load in every session (usage). This tool makes a short index and
prints single entries, so a session reads the index (a few KB) and then only the entries it needs.

Usage (Claude's side, on a staged copy; or `py Tools\\notes_index.py ...` on the PC):
  python3 -I Tools/notes_index.py Notes/MATCHING_NOTES.md                 write Notes/NOTES_INDEX.md and print it
  python3 -I Tools/notes_index.py Notes/MATCHING_NOTES.md --show 66 71    print entries 66 and 71
  python3 -I Tools/notes_index.py Notes/MATCHING_NOTES.md --show "STLport"  print the section(s) whose heading matches
  python3 -I Tools/notes_index.py Notes/MATCHING_NOTES.md --find inline budget   entries containing all the words

An entry is a numbered note ("66. ...") or a "## heading" section. The index gives: id, line range, size and the
entry's first sentence. Other .md notes work too (COMPILER_LIMITED.md, OPEN_WALLS.md).
Inputs: one Markdown file. Output: the index file next to it (NOTES_INDEX.md, only for MATCHING_NOTES.md) and stdout.
"""
import os, re, sys


def entries(lines):
    """-> list of dict(id, title, start, end) ; numbered notes win over the heading that contains them"""
    marks = []
    for i, l in enumerate(lines):
        m = re.match(r"^(\d+)\.\s+(.*)", l)
        h = re.match(r"^(#{2,4})\s+(.*)", l)
        if m:
            marks.append((i, m.group(1), m.group(2)))
        elif h:
            marks.append((i, "#", h.group(2)))
    out = []
    for k, (i, ident, first) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(lines)
        text = " ".join(x.strip() for x in lines[i:min(end, i + 4)])
        text = re.sub(r"^(\d+\.|#+)\s+", "", text)
        bold = re.match(r"\*\*(.+?)\*\*", text)
        title = bold.group(1) if bold else re.split(r"(?<=[.:;])\s", text, maxsplit=1)[0]
        out.append(dict(id=ident, title=title.strip(" .*")[:118], start=i + 1, end=end,
                        size=sum(len(x) + 1 for x in lines[i:end]), head=first))
    return out


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path, args = sys.argv[1], sys.argv[2:]
    lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    ents = entries(lines)
    if args and args[0] == "--show":
        for want in args[1:]:
            hits = [e for e in ents if e["id"] == want] if want.isdigit() else \
                   [e for e in ents if e["id"] == "#" and want.lower() in e["head"].lower()]
            if not hits:
                print(f"(no entry '{want}')")
            for e in hits:
                # a heading section is printed up to the next heading, including its numbered notes
                end = e["end"]
                if e["id"] == "#":
                    later = [x["start"] - 1 for x in ents if x["id"] == "#" and x["start"] > e["start"]]
                    end = later[0] if later else len(lines)
                print(f"--- {os.path.basename(path)} lines {e['start']}-{end}")
                print("\n".join(lines[e["start"] - 1:end]))
        return
    if args and args[0] == "--find":
        words = [w.lower() for w in args[1:]]
        for e in ents:
            body = " ".join(lines[e["start"] - 1:e["end"]]).lower()
            if all(w in body for w in words):
                print(f"{e['id']:>3}  L{e['start']}-{e['end']}  {e['title']}")
        return
    total = sum(len(x) + 1 for x in lines)
    L = [f"# Index of {os.path.basename(path)} ({total // 1024} KB, {len(ents)} entries)", "",
         "Made by Tools/notes_index.py - do not edit; re-run it after adding notes. Read an entry with",
         f"`python3 -I Tools/notes_index.py Notes/{os.path.basename(path)} --show <id or heading words>`.", "",
         "| Entry | Lines | Size | First sentence |", "|---|---|---:|---|"]
    for e in ents:
        ident = e["id"] if e["id"] != "#" else "section"
        L.append(f"| {ident} | {e['start']}-{e['end']} | {e['size'] / 1024:.1f} KB | {e['title'].replace('|', '/')} |")
    text = "\n".join(L) + "\n"
    if os.path.basename(path).upper() == "MATCHING_NOTES.MD":
        open(os.path.join(os.path.dirname(path) or ".", "NOTES_INDEX.md"), "w", encoding="utf-8", newline="\n").write(text)
    print(text)


if __name__ == "__main__":
    main()
