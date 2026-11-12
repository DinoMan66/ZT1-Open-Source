#!/usr/bin/env python3
"""
watch_ai.py - a local model that does the reading. Free tool (Tools\\TOOLS.md).

Run it on the PC (not in the VM) and leave the window open. Easiest: double-click Tools\\localai\\start_local_ai.bat,
which starts llama-server with the model and then this watcher. By hand:
    py Tools\\localai\\watch_ai.py                  finds the local server by itself: llama-server (port 8080)
                                                  or Ollama (port 11434); waits while the model is still loading
    py Tools\\localai\\watch_ai.py --once           answer what is waiting, then exit
    --url http://127.0.0.1:8080   --model qwen3.5:9b (Ollama only)   --ctx N (default: what the server reports)

It waits for questions Claude drops in Tools\\queue\\ask_<id>.json, reads the named project files HERE (so their
text never enters Claude's context), asks the local model, and writes the answer to Tools\\localai\\out\\<id>.md.
Claude then reads only the short answer. It also runs Tools\\queue\\preread_<id>.txt requests (preread.py
options on one line), so a session can ask for digests or naming evidence of the functions it is working on. Nothing leaves this PC: the model runs locally (127.0.0.1 only).

A question file:
    {"id": "r312-notes", "question": "Which notes explain why a small inline helper is called instead of inlined?",
     "files": ["Notes/MATCHING_NOTES.md", "Notes/OPEN_WALLS.md:1-40"], "grep": "inline", "around": 12, "max_words": 250}
  files   paths inside the project, optionally with a line range (path:first-last). Text files only.
  grep    optional regular expression: only the lines within `around` lines of a match are read (for huge files
          such as decompiled\\zoo.exe.c).
  The answer quotes line numbers, so Claude can open exactly those lines if it needs the original wording.

Long input is read in pieces that fit the server's context (llama-server -c 32768: about 30,000 tokens a piece;
Ollama: 8,192 by default) and the partial answers are merged - slower and less exact than one pass. The answer is a HINT from a small model: it can be
wrong or miss things. It is never evidence for a name, a rule or a match (CLAUDE.md "Local model").
Needs: llama.cpp's llama-server or Ollama on this PC. Python standard library only.
"""
import argparse, glob, json, os, re, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
QUEUE = os.path.join(ROOT, "Tools", "queue")
OUT = os.path.join(HERE, "out")
TEXT_EXT = (".md", ".txt", ".csv", ".c", ".cc", ".cpp", ".h", ".hpp", ".inl", ".py", ".bat", ".map", ".json", ".log", ".cdb")
MAX_FILE = 64 * 1024 * 1024


def read_lines(spec, pattern, around):
    """-> [(line number, text)] of one 'path[:first-last]' entry, restricted to the project folder"""
    m = re.match(r"^(.*?)(?::(\d+)-(\d+))?$", spec.strip())
    rel, a, b = m.group(1), m.group(2), m.group(3)
    path = os.path.normpath(os.path.join(ROOT, rel))
    if os.path.commonpath([os.path.abspath(path), ROOT]) != ROOT:
        raise ValueError(f"{rel}: outside the project folder")
    if not path.lower().endswith(TEXT_EXT):
        raise ValueError(f"{rel}: not a text file type")
    if not os.path.isfile(path):
        raise ValueError(f"{rel}: no such file")
    if os.path.getsize(path) > MAX_FILE:
        raise ValueError(f"{rel}: larger than {MAX_FILE >> 20} MB")
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    lo, hi = (int(a), int(b)) if a else (1, len(lines))
    picked = list(range(max(1, lo), min(len(lines), hi) + 1))
    if pattern:
        rx = re.compile(pattern, re.I)
        keep = set()
        for n in picked:
            if rx.search(lines[n - 1]):
                keep.update(range(n - around, n + around + 1))
        picked = [n for n in picked if n in keep]
    return rel, [(n, lines[n - 1]) for n in picked]


def chunks(parts, budget_chars):
    """group (file, [(n, text)]) into pieces of at most budget_chars, never splitting a line"""
    cur, size = [], 0
    for rel, rows in parts:
        head = f"\n=== FILE {rel} (cite it as {os.path.basename(rel)}) ===\n"
        cur.append(head); size += len(head)
        last = None
        for n, text in rows:
            line = (("...\n" if last is not None and n != last + 1 else "") + f"{n}: {text[:400]}\n")
            if size + len(line) > budget_chars and len(cur) > 1:
                yield "".join(cur)
                cur, size = [head], len(head)
            cur.append(line); size += len(line); last = n
    if size:
        yield "".join(cur)


def http_json(url, body=None, timeout=10):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="replace"))


def find_server(a, wait=600):
    """-> ("llama"|"ollama", url, context tokens). Waits up to `wait` s while a server is starting / loading."""
    urls = [a.url] if a.url != "auto" else ["http://127.0.0.1:8080", "http://127.0.0.1:11434"]
    t0, said = time.time(), False
    while True:
        for u in urls:
            u = u.rstrip("/")
            try:                                                   # llama-server: /health is 200 once loaded
                if http_json(u + "/health").get("status") == "ok":
                    ctx = a.ctx
                    if not ctx:
                        try:
                            pr = http_json(u + "/props")
                            ctx = int(pr.get("default_generation_settings", {}).get("n_ctx") or pr.get("n_ctx") or 0)
                        except Exception:
                            ctx = 0
                    return "llama", u, ctx or 8192
            except Exception:
                pass
            try:                                                   # Ollama
                http_json(u + "/api/tags")
                return "ollama", u, a.ctx or 8192
            except Exception:
                pass
        if time.time() - t0 > wait:
            sys.exit("no local model server answered on " + " / ".join(urls) +
                     " - start llama-server (or Ollama) first, or use Tools\\localai\\start_local_ai.bat")
        if not said:
            print("  waiting for the local model server (still starting or loading the model) ...", flush=True); said = True
        time.sleep(5)


def ask_model(url, model, ctx, prompt, max_tokens, kind="ollama"):
    if kind == "llama":                                            # llama-server, OpenAI-style chat endpoint
        r = http_json(url.rstrip("/") + "/v1/chat/completions",
                      {"messages": [{"role": "user", "content": prompt}], "temperature": 0.1, "max_tokens": max_tokens,
                       "stream": False, "chat_template_kwargs": {"enable_thinking": False}}, timeout=1800)
        ans = (r.get("choices") or [{}])[0].get("message", {}).get("content") or ""
        return re.sub(r"<think>.*?</think>", "", ans, flags=re.S).strip()
    body = json.dumps({"model": model, "prompt": prompt, "stream": False, "think": False,
                       "options": {"num_ctx": ctx, "temperature": 0.1, "num_predict": max_tokens}}).encode()
    req = urllib.request.Request(url.rstrip("/") + "/api/generate", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1800) as r:
        ans = json.loads(r.read().decode("utf-8", errors="replace")).get("response", "")
    return re.sub(r"<think>.*?</think>", "", ans, flags=re.S).strip()


RULES = ("You are reading project files for a colleague who cannot see them. Answer ONLY from the text given. "
         "Be brief and factual. After each point give the file and line numbers it comes from: the file named in "
         "the === FILE ... === header above those lines, never any other name, e.g. (name.ext 304-320). "
         "If the text does not answer the question, say 'not found in this part'. "
         "Do not guess, do not add advice.")


def answer(job, a):
    q = str(job.get("question", "")).strip()
    if not q:
        raise ValueError("no question")
    max_words = int(job.get("max_words", 250))
    parts = [read_lines(s, job.get("grep"), int(job.get("around", 10))) for s in job.get("files", [])]
    if not parts:
        raise ValueError("no files")
    nlines = sum(len(r) for _, r in parts)
    nchars = sum(len(t) for _, r in parts for _, t in r)
    budget = max(4000, int((a.ctx - 900 - max_words * 2) * 2.6))       # ~2.6 characters per token (hex and code), room for the answer
    pieces = list(chunks(parts, budget))
    partial = []
    for i, piece in enumerate(pieces):
        print(f"    piece {i + 1}/{len(pieces)} ({len(piece) // 1024} KB) ...", flush=True)
        p = f"{RULES}\n\nQUESTION: {q}\n\nTEXT (each line starts with its line number):\n{piece}\n\nANSWER (at most {max_words} words):"
        partial.append(ask_model(a.url, a.model, a.ctx, p, max_words * 3, a.kind))
    if len(partial) > 1:
        useful = [x for x in partial if "not found in this part" not in x.lower() or len(x) > 80]
        merged = "\n\n".join(f"[part {i + 1}] {x}" for i, x in enumerate(useful or partial))[:budget]
        p = (f"{RULES}\n\nQUESTION: {q}\n\nBelow are partial answers from different parts of the files. Merge them into "
             f"one answer, keep every file/line reference, drop repeats.\n\n{merged}\n\nANSWER (at most {max_words} words):")
        final = ask_model(a.url, a.model, a.ctx, p, max_words * 3, a.kind)
    else:
        final = partial[0]
    head = (f"<!-- local model {a.model if a.kind == 'ollama' else 'llama-server'}, {len(pieces)} piece(s), read {nlines} lines / {nchars // 1024} KB. "
            f"A hint, not evidence: check anything you act on. -->\n")
    return head + final + "\n"


PREREAD_OPTS = {"--top", "--folder", "--max-size", "--min-size", "--va", "--evidence", "--force"}


def run_preread_request(p):
    """Tools\\queue\\preread_<id>.txt from a Claude session: preread.py options on one line (e.g. `--folder ui --top 20`,
    `--va 0x4e9989 0x4e9a10`, `--evidence 0x61f8c0`). The questions it queues are answered by this watcher next."""
    name = os.path.basename(p)
    try:
        time.sleep(1.0)
        args = open(p, encoding="utf-8").read().split()
        bad = [x for x in args if x.startswith("--") and x not in PREREAD_OPTS]
        if bad:
            raise ValueError("not a preread.py option: " + " ".join(bad))
        import subprocess
        r = subprocess.run([sys.executable, os.path.join(HERE, "preread.py")] + args, capture_output=True, text=True,
                           errors="replace", timeout=600)
        text = r.stdout[-3000:] + r.stderr[-2000:]
        print(f"  {name}: preread.py {' '.join(args)} -> {text.strip().splitlines()[-1] if text.strip() else 'done'}", flush=True)
    except Exception as ex:
        text = f"ERROR: {type(ex).__name__}: {ex}\n"; print(f"  {name}: failed: {ex}")
    with open(os.path.join(OUT, name[:-4] + ".log"), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    try: os.remove(p)
    except OSError: pass


def server_down(ex):
    """True when the model server itself is gone (crashed, window closed, still loading), not when it refused a request"""
    import http.client, urllib.error
    if isinstance(ex, urllib.error.HTTPError):
        return ex.code == 503                                # llama-server answers 503 while (re)loading the model
    if isinstance(ex, urllib.error.URLError):
        ex = ex.reason if isinstance(ex.reason, BaseException) else ex
    return isinstance(ex, (ConnectionError, http.client.RemoteDisconnected, TimeoutError)) or \
        getattr(ex, "winerror", None) in (10053, 10054, 10061) or isinstance(ex, OSError) and "refused" in str(ex).lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="qwen3.5:9b")
    ap.add_argument("--ctx", type=int, default=0, help="context tokens per request (default: what the server reports)")
    ap.add_argument("--url", default="auto", help="server address, local only (default: find llama-server or Ollama)")
    ap.add_argument("--once", action="store_true", help="answer what is waiting, then exit")
    a = ap.parse_args()
    if a.url != "auto" and not re.match(r"^https?://(127\.0\.0\.1|localhost)(:\d+)?/?$", a.url):
        sys.exit("--url must be on this PC (127.0.0.1 / localhost): project text is never sent anywhere else")
    os.makedirs(OUT, exist_ok=True); os.makedirs(QUEUE, exist_ok=True)
    a.kind, a.url, a.ctx = find_server(a)
    print(f"local reader: {'llama-server' if a.kind == 'llama' else 'Ollama model ' + a.model} at {a.url}, context {a.ctx}, watching {QUEUE}\\ask_*.json  (Ctrl+C stops)")
    crashes = {}                                          # ask file -> times the server died while answering it
    while True:
        for p in sorted(glob.glob(os.path.join(QUEUE, "preread_*.txt"))):
            run_preread_request(p)
        for p in sorted(glob.glob(os.path.join(QUEUE, "ask_*.json"))):
            name = os.path.basename(p)
            try:
                time.sleep(1.0)                                   # let the shared folder finish writing
                job = json.load(open(p, encoding="utf-8"))
                ident = re.sub(r"[^\w.-]", "_", str(job.get("id") or name[4:-5]))[:60]
                print(f"  {name}: {str(job.get('question', ''))[:90]}", flush=True)
                t0 = time.time()
                text = answer(job, a)
                print(f"    answered in {time.time() - t0:.0f} s")
            except Exception as ex:                               # a bad request must not stop the watcher
                if server_down(ex):
                    crashes[p] = crashes.get(p, 0) + 1
                    if crashes[p] < 3:
                        # the question stays queued; answer it once the server is back
                        print(f"    the model server stopped answering ({ex}). It has crashed or its window was closed -"
                              f" look at the llama-server window for the reason. Waiting for it to come back ...", flush=True)
                        a.kind, a.url, a.ctx = find_server(a, wait=3600)
                        print("    the server is back; continuing", flush=True)
                        break
                    ex = RuntimeError(f"the server stopped every time it read this request ({ex}) - it is probably "
                                      "too large for the server's memory; ask with fewer or shorter files")
                ident = re.sub(r"[^\w.-]", "_", str((locals().get("job") or {}).get("id") or name[4:-5]))[:60]
                with open(os.path.join(OUT, ident + ".failed.txt"), "w", encoding="utf-8", newline="\n") as f:
                    f.write(f"local model: request failed\nERROR: {type(ex).__name__}: {ex}\n")
                print(f"    failed: {ex}  -> Tools\\localai\\out\\{ident}.failed.txt")
                try: os.remove(p)
                except OSError: pass
                continue
            with open(os.path.join(OUT, ident + ".md"), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            try: os.remove(os.path.join(OUT, ident + ".failed.txt"))
            except OSError: pass
            if ident.startswith("pre_") and os.path.exists(os.path.join(HERE, "preread.py")):
                try:                                              # keep Tools\localai\out\PREREAD.md current
                    import subprocess
                    subprocess.run([sys.executable, os.path.join(HERE, "preread.py"), "--collect"], capture_output=True, timeout=120)
                except Exception:
                    pass
            try:
                os.remove(p)
            except OSError:
                pass
        if a.once:
            return
        time.sleep(3)


if __name__ == "__main__":
    main()
