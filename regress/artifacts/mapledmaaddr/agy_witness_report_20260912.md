I have launched the initial environment check script in WSL Gentoo and will wait for it to complete.
I will wait for the environment check to complete.
I am waiting for the check to complete.
Waiting for the git diff check to complete.
Waiting for the task to finish.
Waiting for background tasks.
Waiting for the background process to complete.
I am awaiting the completion of the background check.
Waiting for background task notification.
The environment check is running; I will wait for notification upon its completion.
Clones `/tmp/gxagy_maple_c` and `/tmp/gxagy_maple_f` have been prepared, and both builds have been launched in WSL Gentoo. I will wait for the build process to finish.
Waiting for test session to complete.
Waiting for test on committed build to finish.
Waiting for task-122.
Waiting for the test on the fixed build to complete.
Waiting for background completion.
Waiting for background notification.
Running the witness against the committed build; I will wait for it to complete.
Waiting for background notification.
Waiting for witness run to complete.
Waiting for background task-145 to finish.
Waiting for background task-145 to finish.
Running the witness against the fix build; I will wait for it to complete.
Waiting for task-167 to complete.
Waiting for witness run to complete.
Waiting for task-186 to finish.
Running the witness script against both clones to generate `witness_committed.out` and `witness_fix.out`. I will wait for both runs to finish.
Waiting for task-204 to complete.
AGY_MAPLE_20260912
VERDICT: Rung-3 cold-debugger witness for `mapledmaaddr` successfully built and executed; committed build is RED (4/12) and fix build is GREEN (12/12).

---

### 1. Build Verification (`[gxemul -nt source]`)

Both scratch clones were built inside WSL Gentoo from `/mnt/c/DocumentNoSnc/CC/GXEMUL/build` with `rm -f src/devices/*.o && make -j4`:

* **Committed clone (`/tmp/gxagy_maple_c`)**:
  `[ gxemul -nt src/devices/dev_dreamcast_maple.c ]` -> **PASS** (`COMMITTED_BUILD_NT_CHECK=PASS`)
* **Fix clone (`/tmp/gxagy_maple_f`)**:
  `[ gxemul -nt src/devices/dev_dreamcast_maple.c ]` -> **PASS** (`FIX_BUILD_NT_CHECK=PASS`)

---

### 2. Witness Scores and Row Breakdown

The same witness script was executed against both binaries:

* **Committed Build Score**: **`4/12`** (RED)
* **Fix Build Score**: **`12/12`** (GREEN)

#### Row Results Summary

| Row Name | Committed Got | Fix Got | Want | Committed Status | Fix Status | Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `ctrl live` | `0x12345678` | `0x12345678` | `0x12345678` | **ok** | **ok** | Liveness control: RAM store then load round-trips through cold debugger |
| `ctrl devsig sh4` | `0xda74` | `0xda74` | `0xda74` | **ok** | **ok** | Device signature control: SH4 `IPRD` reset value |
| `ctrl devsig maple` | `0x12340000` | `0x12340000` | `0x12340000` | **ok** | **ok** | Maple signature control: `MAPLE_SPEED` masks/shifts `0x12345678` to `0x12340000` |
| `initial zero` | `absent` | `0x0` | `0x0` | **FAIL** | **ok** | Committed emulator process dies on read before debugger can print |
| `read val_a` | `absent` | `0x8c012345` | `0x8c012345` | **FAIL** | **ok** | Value with nonzero high bit and low bits; dies on committed |
| `read val_b` | `absent` | `0xc00001f` | `0xc00001f` | **FAIL** | **ok** | Value with low 5 bits set (`0x1f`); dies on committed |
| `write replace` | `absent` | `0x13579bdf` | `0x13579bdf` | **FAIL** | **ok** | Second store replaces first; dies on read under committed |
| `align refusal` | `absent` | `0x13579bdf` | `0x13579bdf` | **FAIL** | **ok** | Independent alignment refusal fires, readback dies under committed |
| `marker survive` | `absent` | `0x55aa55aa` | `0x55aa55aa` | **FAIL** | **ok** | Marker store instruction following read never runs under committed |
| `read quiet` | `found` | `absent` | `absent` | **FAIL** | **ok** | Diagnostic `TODO: read from dmaaddr` is emitted under committed |
| `exit status` | `exit1` | `exit0` | `exit0` | **FAIL** | **ok** | Process exits with code 1 under committed instead of clean exit 0 |
| `ctrl zlive` | `0xdeadbeef` | `0xdeadbeef` | `0xdeadbeef` | **ok** | **ok** | Trailing liveness control proves apparatus remained alive throughout |

#### Why the Committed Build Fails the Subject Rows
In committed [`src/devices/dev_dreamcast_maple.c`](file:///C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/src/devices/dev_dreamcast_maple.c#L562-L566), `case 0x04:` read arm executes:
```c
fatal("[ dreamcast_maple: TODO: read from dmaaddr ]\n");
odata = d->dmaaddr;
exit(1);
```
When an SH4 guest instruction (`mov.l @r1, r2`) reads `MAPLE_DMAADDR` (`0xa05f6c04`), the emulator emits `[ dreamcast_maple: TODO: read from dmaaddr ]` and immediately calls `exit(1)`. Consequently:
1. The guest instruction cannot return data (`print r2` never executes, yielding `absent`).
2. Subsequent instructions (such as the survival marker store to RAM) never execute.
3. The read diagnostic is present in the transcript (`found` vs `absent`).
4. The process terminates with `exit1` instead of `exit0`.

On the fix build (where `fatal(...)` and `exit(1)` are removed and `odata = d->dmaaddr;` is retained), the guest read completes normally, delivering `d->dmaaddr` across all test values and states, executing following instructions, remaining silent, and exiting cleanly with `exit0`.

---

### 3. Deliverables

All deliverables have been placed in [`GXEMUL-SEC/regress/artifacts/mapledmaaddr/`](file:///C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/mapledmaaddr/):

1. **Witness Script**: [agy_maple_witness_20260912.py](file:///C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/mapledmaaddr/agy_maple_witness_20260912.py)
2. **Committed Output**: [witness_committed.out](file:///C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/mapledmaaddr/witness_committed.out)
3. **Fix Output**: [witness_fix.out](file:///C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/mapledmaaddr/witness_fix.out)
4. **Fix Diff**: [fix.diff](file:///C:/DocumentNoSnc/CC/GXEMUL/GXEMUL-SEC/regress/artifacts/mapledmaaddr/fix.diff)
