"""READ-ONLY on the repo: builds MUTATED COPIES of the HEAD ledger copy inside this work dir only."""
import io, json, sys, copy
src, outdir = sys.argv[1], sys.argv[2]
sys.path.insert(0, outdir + "/st")
import stage_tokens as st
L = json.load(io.open(src, encoding="utf-8"))
def row(L, rid):
    return [r for r in L["rows"] if r["id"] == rid][0]
rep = io.open(outdir + "/sim_sgirekills.txt", "w", encoding="utf-8")
r = row(L, "sgirekills")
ass = [e for e in r["entries"] if e.get("phase") == "assess"]
rep.write("HEAD: live_holds(sgirekills/assess) = %s\n" % st.live_holds(ass))
rep.write("HEAD: held_seats([2]) = %s\n" % st.held_seats(r["entries"][2]))
for i in (70, 71):
    e = r["entries"][i]
    rep.write("HEAD: [%d] seat=%s is_answer=%s note[:120]=%r\n" % (i, e["seat"], st.is_answer(e), e["note"][:120]))
def variant(tok, close):
    M = copy.deepcopy(L)
    rr = row(M, "sgirekills")
    if tok:
        for i in (70, 71):
            rr["entries"][i]["note"] = st.NOTSEAT + " " + rr["entries"][i]["note"]
    if close:
        rr["state"] = "closed"
        for ph in ("research", "review", "regress"):
            rr["entries"].append({"date": "2026-10-21", "phase": ph, "seat": "fable5", "d": "✓",
                                  "note": "SIMULATED Fable answer (not a ledger entry; a measurement input)"})
    return M
for name, tok, close in (("A_head_reclosed", False, True), ("B_tokened_reclosed", True, True), ("C_tokened_held", True, False)):
    M = variant(tok, close)
    p = outdir + "/ledger_sim_%s.json" % name
    io.open(p, "w", encoding="utf-8").write(json.dumps(M, ensure_ascii=False, indent=1))
    ass = [e for e in row(M, "sgirekills")["entries"] if e.get("phase") == "assess"]
    rep.write("%s: live_holds(sgirekills/assess) = %s ; state=%s ; ledger=%s\n" % (name, st.live_holds(ass), row(M, "sgirekills")["state"], p))
rep.close()
