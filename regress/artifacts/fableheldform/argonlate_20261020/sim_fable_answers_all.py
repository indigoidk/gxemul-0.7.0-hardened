"""READ-ONLY on the repo.  Copy of the HEAD ledger (argv[1]) -> argv[2] with a SIMULATED Fable answer
(dated 2026-10-21) appended to every phase where fable5 already has an entry, on the rows fableheldform
touched plus ip30abortkill -- a measurement input, never a ledger entry.  Run section H on argv[2] after."""
import io, json, sys
L = json.load(io.open(sys.argv[1], encoding="utf-8"))
ROWS = ("fableheldform", "ip30abortkill", "cxlaunchquotation", "dashokclass", "mapledmaaddr", "ppcgateimageskip",
        "sgirekills", "sgirandomcolour", "xscaleinten", "ppcrldimimask", "ppcrlwimiwidth", "wiringcliff")
for r in L["rows"]:
    if r["id"] in ROWS:
        for ph in ("design", "research", "review", "regress"):
            if any(e.get("phase") == ph and e.get("seat") == "fable5" for e in r["entries"]):
                r["entries"].append({"date": "2026-10-21", "phase": ph, "seat": "fable5", "d": "✓",
                                     "note": "SIMULATED Fable answer (a measurement input, not a ledger entry)"})
io.open(sys.argv[2], "w", encoding="utf-8").write(json.dumps(L, ensure_ascii=False, indent=1))
