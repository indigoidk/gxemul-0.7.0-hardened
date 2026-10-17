## 8. Questions -- verdict line first, then answer each by number; say plainly what you could not check

1. **The ruling.**  Does the renderer implement the ruled class exactly -- every explicit `d` outside ✓ ✕ ⏸ … in ONE
   residue class, text kept, a missing `d` still `…`, holds and records untouched -- and does the strip now sum to the
   entry total?  Is "legacy -- verdict unclassified" faithful to Astra's wording, and is anything in the legend or
   tooltip a claim the data does not support?
2. **The grandfathering key.**  Is the (row, phase, seat, date, d) multiset the right key?  Name an edit that adds a NEW
   off-domain answer and still passes Q2 (for example by reusing an existing tuple), and one that blocks a legitimate
   edit.  Is leaving the NOTE out of the key right?  Is the baseline writer's placement (artifacts dir, never run by the
   checker) a sufficient guard against re-baselining to launder an entry?
3. **The cutoff.**  Inclusive 2026-10-17.  Given that the baseline already refuses back-dated and undated additions, does
   the date test add anything real (C12 says it refuses a post-cutoff tuple that is somehow in the baseline), or is it a
   rule kept only because the ruling named it?  What does it do to an entry whose date is malformed (not ISO)?
4. **The controls (section 7).**  Are C1-C13, R1-R3 and W1-W2 each able to fail for the reason they name?  **What is the
   smallest edit to the staged checker, renderer or precommit block that passes all 19 controls and breaks a ruled
   property?**  (A sketch is fine; do not build anything.)
5. **Display.**  `?` for an explicit blank `d`, and HTML-escaping every `d` -- right?  Does the escape change any existing
   cell's rendering (an `&` or `<` in some `d`)?
6. **Which of my dispositions is wrong?**  Name the count you checked.
