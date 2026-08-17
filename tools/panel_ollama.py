#!/usr/bin/env python3
"""One Ollama-cloud panel seat. Run from Windows git-bash (NOT WSL -- WSL
cannot reach the Windows host's localhost:11434). Writes a utf-8 file; never
print()s the response (git-bash stdout is cp1252 and crashes on it).

    python panel_ollama.py <model> <out_file> <brief_file>
"""
import json
import sys
import urllib.request

model, out, brief_path = sys.argv[1], sys.argv[2], sys.argv[3]
brief = open(brief_path, encoding="utf-8").read()
try:
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps({"model": model, "prompt": brief,
                         "stream": False}).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    resp = json.load(urllib.request.urlopen(req, timeout=1500))
    body = resp.get("response") or json.dumps(resp)
except Exception as e:      # a retired model returns an HTTP 500 with a reason
    body = "OLLAMA_SEAT_ERROR: %r" % e
open(out, "w", encoding="utf-8").write(body)
