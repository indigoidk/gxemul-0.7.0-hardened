Read-only review of a shell tool's argument checks. Do not edit anything.

Files (frozen copies; read these, not any other copy under the project root):
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c5_frozen\derive_hygiene_pins.sh  (md5 e1ce9c59, the tool)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c5_frozen\gate_hygiene.sh         (md5 9d88b3f6, the script it edits)
  C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c5_frozen\census_tokens.py        (md5 98788b1b)
  The previous versions: C:\DocumentNoSnc\cc\GXEMUL\_scratchpad\census0923\c4_frozen\ (same names).

Background: derive_hygiene_pins.sh reads counts from gate_hygiene.sh's own code and rewrites number and list assignments
in gate_hygiene.sh.  It takes three kinds of input that end up in that file: a "--ruling YYYY-MM-DD: reason" text
(written as a comment line), probe file names given to --grandfather/--release (written into a double-quoted list),
and file names found in the tree (written into WHOLE_FULL_FILES="..." as name:count).  The new version counts every
disallowed byte with wc -c, parses the date in UTC, refuses an empty ruling, runs the gate's python3 lines with a
working interpreter and checks the classifier runs on a known input first, and finds the list assignment by an anchored
search.

Answer VERDICT first (one line), then:

TASK 1.  For each of the three inputs, list values the checks accept that the tool's header says are refused, and
legitimate values they refuse.  Say what ends up in gate_hygiene.sh for each accepted odd value.

TASK 2.  Is there any other input that reaches gate_hygiene.sh through this tool that is not checked?

TASK 3.  The interpreter check: can the classifier run, pass the known-input check, and still produce a wrong or empty
result that the tool then writes as if it were right?

TASK 4.  Quote any sentence in the tool's header or the changed comments that is false about the code as it is now.

End with: files read, and anything you ran.
