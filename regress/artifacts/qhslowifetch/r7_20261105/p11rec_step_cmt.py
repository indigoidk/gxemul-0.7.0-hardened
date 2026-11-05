import io
import sys
import textwrap

# Pass-11 R1's sibling in the partner loop's header comment (comment-only: no AST change).
p = sys.argv[1]
s = io.open(p, encoding="utf-8", newline="").read()
assert "\r" not in s
old = ("# translation_readahead differs, nonzero on the two-entry session's first visit.  So a toggle conditioned on any of those fires on\n"
       "# both visits exactly when it fires on the partner's one -- it cancels on the pair's two-entry side and shows on the partner -- and a\n"
       "# condition on translation_readahead fires on one visit only and shows on the two-entry side.\n")
assert s.count(old) == 1, s.count(old)
text = ("translation_readahead differs, nonzero on the two-entry session's first visit.  So a toggle conditioned on any of those that "
        "the toggle itself leaves unchanged fires on both visits exactly when it fires on the partner's one -- it cancels on the "
        "pair's two-entry side and shows on the partner -- and a condition on translation_readahead fires on one visit only and "
        "shows on the two-entry side.  A self-referential toggle is outside this: the docstring's SCOPE (codex pass 11, R1).")
lines = textwrap.wrap(text, width=132, break_on_hyphens=False, break_long_words=False)
new = "".join("# " + x + "\n" for x in lines)
assert max(len(x) for x in new.split("\n")) <= 134
assert "".join(new.replace("#", "").split()) == "".join(("# " + text).replace("#", "").split())
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8", newline="").write(s)
print("CMT-P11 APPLIED (%d lines -> %d)" % (3, len(lines)))
print(new, end="")
