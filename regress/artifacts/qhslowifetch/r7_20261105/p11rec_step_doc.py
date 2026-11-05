import io
import re
import sys

# Pass-11 records corrections R1 and R2 (adj_p11_20261105/ADJ_MYTHOS_local.md sections 2 and 3), docstring only.
p = sys.argv[1]
s = io.open(p, encoding="utf-8", newline="").read()
assert "\r" not in s
doc_end = s.index('"""', s.index('"""') + 3)


def rep_words(old, new):
    global s, doc_end
    pat = re.compile(r"\s+".join(re.escape(w) for w in old.split()))
    m = list(pat.finditer(s))
    assert len(m) == 1, (len(m), old[:80])
    assert m[0].end() < doc_end, "match outside the docstring"
    s = s[:m[0].start()] + new + s[m[0].end():]
    doc_end = s.index('"""', s.index('"""') + 3)


# R1: the ruler's section-2 text, with three changes made on checking it against the code (B123_NOTE.md, pass 11 records):
# the TESTS / does-not-test classification dropped from both enumerations (arm (b) masks pc's low two bits off, :4168), the pc
# rows narrowed to the cells carrying the marker, and the ME / pc catch tagged DERIVED like the RI escape.  Then the old sentence,
# quoted and marked false.
rep_words("A pair presents the failure block with the same pc, addr, MSR, running (0) and instruction slot, and differs only in "
          "translation_readahead, nonzero on the two-entry session's first visit.  So a toggle of pinned state under a condition on "
          "anything else the block reads fires on both of the two-entry session's visits exactly when it fires on the partner's one "
          "-- it cancels on one side and shows on the other -- and a condition on translation_readahead fires on one visit of the "
          "two-entry session and shows there.",
          "A pair presents the failure block with the same pc, addr, MSR, running (0) and instruction slot, and differs only in "
          "translation_readahead, nonzero on the two-entry session's first visit.  So a toggle of pinned state under a condition "
          "that the toggle itself leaves unchanged, on anything else the block reads, fires on both of the two-entry session's "
          "visits exactly when it fires on the partner's one; it cancels on one side and shows on the other.  A condition on "
          "translation_readahead fires on one visit of the two-entry session and shows there.  THE SCOPE: the pairing guarantees "
          "equal INPUTS at entry; it says nothing about state the toggle writes on the first visit and tests on the second.  A "
          "SELF-REFERENTIAL toggle, `if (translation_readahead || (msr & BIT)) msr ^= BIT`, sets its marker on the read-ahead "
          "visit and clears it on the real fetch, cancels on the two-entry side and never fires on the partner, which enters with "
          "the marker clear.  When the marker is MSR[ME] or one of pc's low two bits, the generating-set rows catch it: the "
          "ME-set cells' msr rows and the pc rows of the unaligned cells carrying it red because those bits are held both ways "
          "(DERIVED, not measured).  When the marker is MSR[RI] (codex pass 11, B1; cpu_ppc.h:175; DERIVED, not measured), "
          "MSR[PMM], MSR[LE], or an SRR0 bit clear in the sentinel, no row distinguishes it: this is a joint of "
          "translation_readahead x an untested bit x visit order, clause (e), NOT CLAIMED, and no row is owed for it "
          "(tools/CLAUDE.md, the generating-set and 'tests means masks or compares' clauses).  An entry with that bit set would see "
          "any one member and the next member moves the bit.  This text said \"a toggle of pinned state under a condition on "
          "anything else the block reads fires on both of the two-entry session's visits exactly when it fires on the partner's "
          "one\"; that was FALSE for conditions on state the toggle itself writes (codex pass 11, R1): the block reads MSR, B1's "
          "condition reads MSR, and the second visit's MSR is not the entry MSR.")

# R2: the ruler's section-3 correction; its closing "as the field-write disclosure says" dropped (that disclosure covers writes to
# fields the block neither reads nor writes, not conditions on unread state, and next_ic is written).  Then the old claim, marked.
rep_words("The bound: a condition on state the block neither reads nor writes -- the GPRs the subfic changes, next_ic -- is outside "
          "it, as the field-write disclosure says.",
          "The bound: a condition on state the block does not READ: the GPRs the subfic changes (neither read nor written here) and "
          "next_ic (written by arm (b)'s refresh, arm (c)'s park and the checkstop fallback, never read) is outside it.  This "
          "sentence called next_ic state the block \"neither reads nor writes\": FALSE (codex pass 11, R2).")

io.open(p, "w", encoding="utf-8", newline="").write(s)
print("DOC-P11 APPLIED")
