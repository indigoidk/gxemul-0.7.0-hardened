# Regression battery

The harness used to boot‑ and shell‑test the hardened emulator across CPU
architectures. Results live alongside it: [`BATTERY_RESULTS.md`](BATTERY_RESULTS.md)
(post‑boot results), [`BATTERY_PASS_MAP.md`](BATTERY_PASS_MAP.md) (per‑OS pass
map), and [`TEST_BATTERY.md`](TEST_BATTERY.md) (battery definition).

## Scripts
| script | what it does |
|---|---|
| `reg_sweep.sh` | multi‑arch boot + per‑machine device‑attach assertions + panic/fatal/ASan detection |
| `reg_pmax_postboot.sh` | OpenBSD/pmax deep: root login, NAT ping, disk write/read cksum, daemon health |
| `reg_pmax_persist.sh` | reboot persistence + FFS‑clean disk‑integrity |
| `reg_macppc.sh` | macppc `g4` / `g4plus` boot check |
| `shell_luna88k.sh` · `shell_landisk.sh` · `shell_macppc.sh` | M88K / SH4 / PPC interactive‑shell exercises |
| `drive.py` | the expect‑style console driver the scripts use |

## Running them — bring your own bits
These are **illustrative research/QA scripts, not a turnkey suite.** They depend
on things deliberately *not* redistributed here:

- **A built `gxemul`** — `./configure && make` at the repo root (binary → `../gxemul`).
- **Guest kernels / images** in `KERNELS` (default `./kernels`) — download them
  yourself; sources are listed in [`TEST_BATTERY.md`](TEST_BATTERY.md).
- **An installed OpenBSD/pmax rig** in `RIGDIR` (default `./rig`: a `bsd` kernel +
  `disk.img`) for the pmax depth/persistence tests.

Every path is overridable via environment variables (or edit the defaults at the
top of each script):

```sh
GXEMUL=../gxemul  DRIVE=./drive.py  KERNELS=./kernels  RIGDIR=./rig  WORK=./out \
  ./reg_sweep.sh
```

> Origin is a Windows + WSL setup; treat these as a starting point to adapt to
> your environment, not a portable test framework.
