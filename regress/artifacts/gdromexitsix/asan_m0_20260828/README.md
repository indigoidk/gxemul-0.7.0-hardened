# `#489`'s headline claim, MEASURED — a guest-controlled heap-buffer-overflow WRITE

`#489` de-fatalised the `case 0x14` Read-TOC length guard. Its strongest single result was the
BARE-DELETION mutant (`M0`): with the guard removed, the host **survived** while writing 408
bytes past an allocation sized by a guest-supplied count.

**The measuring seat stated its own limit, and that limit was the point:**

> it confirms the write does not FAULT, not that the write is absent. **One ASan run would
> convert the claim from derived to measured** — and `build-asan/` currently has no binary.

`build-asan/` was fixed the same day (`asanunbuildable`). This is that run.

## THE MEASUREMENT

`M0` — the `cnt != 408` guard deleted outright, one edit over the shipped tree, built in a
scratch clone of `build-asan/` with its own `.MUTANT` sentinel — run against the shipped
19-row detector under `ASAN_OPTIONS=log_path=/tmp/asanrep:detect_leaks=0:abort_on_error=0`.

```
TOCLEN_RESULT=8/19
7 × ERROR: AddressSanitizer: heap-buffer-overflow
```

| overflow shape | count | what produced it |
|---|---|---|
| `0 bytes after 407-byte region` | 5 | `cnt=407` — the hardcoded 408th byte lands one past |
| `0 bytes after 1-byte region` | 2 | the `cnt=0` end of the same guard |

**Every one is a `WRITE of size 1`** — the byte-at-a-time TOC writer walking off the end of a
buffer whose size the guest chose.

## THE STACK IS THE PART THAT MATTERS

```
    #0 handle_command              dev_dreamcast_gdrom.c:567
    #1 dev_dreamcast_gdrom_access                       :842
    #2 sh_memory_rw_one_page       memory_rw.c:587
    #3 sh_instr_mov_w_store_rm_rn  cpu_sh_instr.c:1399
    #4 sh_instr_to_be_translated   cpu_dyntrans.c:1978
    #5 sh_run_instr                cpu_dyntrans.c:325
    #6 machine_run                 machine.c:710
    #7 emul_run                    emul.c:1048
    #8 main                        main.c:807

  allocated by:  alloc_data  dev_dreamcast_gdrom.c:443   <- malloc(guest-supplied cnt)
                 handle_command                    :532
```

**A guest `mov.w` store, through real address decode, through `memory_rw`, into the device
handler, onto a heap buffer the guest sized.** No harness, no direct call, no stub — the whole
path from `_start` down. That is why the claim is now *measured* rather than *inferred from
survival*: survival tells you the process did not die, and says nothing about whether memory
outside the allocation was written. ASan answers exactly that question, and the answer is yes,
seven times, in two distinct shapes.

## WHAT THIS DOES AND DOES NOT ESTABLISH

* **DOES:** the guard `#489` shipped is the only thing between a guest and a heap overflow
  write on this path. Removing it is not a cosmetic regression.
* **DOES:** the earlier "host survives" observation was correct AND incomplete — both facts
  hold, and the round was right to record its limit rather than round it up.
* **DOES NOT:** say anything about the SHIPPED code, which declines and never reaches
  `alloc_data` with a bad count. This measures the mutant, i.e. what the fix prevents.
* **DOES NOT:** establish exploitability. It establishes an out-of-bounds write with
  guest-chosen extent, which is where a hardening fork's interest properly stops.

## AN APPARATUS FAILURE WORTH CARRYING — THE FIRST RUN WAS NOISE, NOT A NEGATIVE

The first attempt reported **`6/19` and ZERO ASan reports**, which reads as a clean negative
result. It was not a result at all.

The tell was a row that could not have been affected by the mutant: **`ok surv` read `exit1`
on the LEGAL 408-byte length**, which the deleted guard does not touch. A number that cannot be
explained by the thing under test is not evidence about the thing under test.

**Cause: LeakSanitizer.** It is on by default with ASan, fires at exit on every session, and
ASan's default exit code is 1 — so every survival row read as a host death, and the genuine
overflow reports went to a pty that the probe's log does not retain. `detect_leaks=0` plus
`log_path=` fixed both halves at once.

> **AN ASAN RUN THROUGH A PTY NEEDS `log_path=` AND `detect_leaks=0`.** Without the first the
> reports can vanish; without the second every row reads as a death. Either alone yields a
> confident, wrong answer — and the first run produced exactly that.

*Also recorded because the failure was the GOOD kind: the mutant applier REFUSED with
`count=0` on an earlier attempt rather than mutating nothing and producing a table of
meaningless scores. Its anchor had been eaten by a nested-heredoc backslash chain — the
documented trap — and `apply_m0.py` (preserved here) is the remedy: a real file, `chr(92)`, and
an assertion that the guard is actually gone afterwards.*
