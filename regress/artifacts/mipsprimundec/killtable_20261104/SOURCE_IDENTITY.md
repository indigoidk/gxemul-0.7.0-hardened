# mipsprimundec -- source identity of the shipped detector (P19 of cloud Fable's pass-2 adjudication)

Made AFTER the P12, P14 and P15 edits, the landing's `#NNN` -> `#580` fill and the landing's rewording of the DETECTOR paragraph's ExcCode/CE pairs into words (check_score_claims reads `10/0` as a score) -- P19's sequencing.  md5 of the bytes; `ast` = sha256 (first 16) of `ast.dump` of the module with its docstring removed (comments are not in the tree).

| file | md5 | ast (docstring stripped) |
|---|---|---|
| `regress/mips_primundec_probe.py` (shipped) | `dae62682d83898939fdcbe2b83d24893` | `1ee971e33d8c72eb` |
| `d31_20261104/probe122_frozen.py` (the 122-row copy the D31 table ran) | `5d3c67f078673743bf9072419bc4d8db` | `1ee971e33d8c72eb` |
| `probe_frozen.py` (the 121-row copy tables 1 and 2 ran) | `b4d04d57cf1ef9a99050b45e57e914f2` | `0473f4d0b4db1d33` |

**The shipped probe's syntax tree equals the 122-row frozen copy's** (yes); everything after the docstring is byte-identical (yes), so the two differ only in docstring text.
**The 122-row tree minus the D31 block equals the 121-row tree**: yes.  The block is four statements -- the `r59 mdmx` session, `ri`, `g59` and the `r59 mdmx notRI` row -- so every table-1 and table-2 score carries over to the shipped instrument for its 121 rows; the new row was measured on its own (`d31_20261104/`).
