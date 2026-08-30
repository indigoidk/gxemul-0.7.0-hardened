#!/usr/bin/env python3
#
#  PreToolUse guard: `wsl ... -c '<string with an unescaped $>'` LOSES THE DOLLAR.
#
#  WHY THIS EXISTS, and why it is a hook rather than a precommit check.
#  ---------------------------------------------------------------------------
#  Measured 2026-08-29 (regress/artifacts/makercfalse/wsl_dollar_20260829.out):
#
#      bash -c 'false; echo $?'             -> 1     ordinary, local
#      wsl -- bash -c 'false; echo $?'      -> 0     THE DEFECT
#      wsl -- bash -c 'X=hello; echo [$X]'  -> []    set and used in ONE command
#      wsl -- bash -c 'echo "a  b"'         -> a  b  quoting DOES survive
#
#  SINGLE QUOTES DO NOT PROTECT through this path.  A mutant that is never
#  applied then scores the BASE binary and reports a clean table.
#
#  It has bitten SIX times against FOUR prior write-ups (nightly_battery.sh's
#  header 2026-08-17, af4884c 2026-08-20, CHANGELOG #477-era, asanbaselinedrift
#  2026-08-28, once more the same hour the fifth was documented, and once more
#  on 2026-08-29 THROUGH THIS HOOK -- see the scoping note below).  Prose is
#  measured ineffective for this class.
#
#  A PRECOMMIT GREP WAS MEASURED TO HAVE **ZERO RECALL**: `wsl.*bash -c` appears
#  exactly four times in the committed tree and all four are QUOTATIONS OF THE
#  DEFECT.  Every one of the occurrences was an interactive, ad-hoc command.  So
#  the only surface where this class can be caught before it produces a phantom
#  is the one where it is TYPED.  Hence a hook.
#
#  WHAT IT DOES WHEN THE THING IS FALSE (the check-that-cannot-fail question):
#  a wsl invocation with no `-c`, or whose `-c` string has no bare `$`, or which
#  uses either measured-safe form, produces NO output and exit 0.  It is silent
#  in the safe case and loud in the unsafe one, which is the whole test.
#
#  FAIL-SAFE BY CONSTRUCTION: this runs on every Bash call, so any internal
#  error exits 0 (allow).  A guard that can wedge the session is worse than the
#  defect it guards against.
#
#  *** AND THAT GUARANTEE HAS A HOLE THAT WAS MEASURED, NOT REASONED. ***  A
#  SyntaxError DEFEATS IT ENTIRELY: the file never parses, so the try/except
#  never runs, and every Bash call in the session gets a traceback instead of a
#  decision.  That happened on 2026-08-29 while editing this file.  The fail-safe
#  covers RUNTIME errors only.
#
#      => ANY edit to this hook is syntax-checked BEFORE it is installed:
#         python -c "import ast,io; ast.parse(io.open(PATH,encoding='utf-8').read())"
#
#  Controls: regress/artifacts/makercfalse/hook_controls_20260829/ -- 18 rows,
#  9 that must FIRE and 9 that must stay SILENT.  A suite that only proves the
#  guard fires is half a suite.
#
import json
import re
import sys

#  `$(` is a DELIBERATE outer-shell substitution -- the caller means git-bash to
#  expand it before wsl ever sees it -- so it is not the defect and is exempt.
#  `\$` is the measured-safe escaped form.  Everything else that is a bare `$`
#  followed by a name, a brace, or `?` is the hazard.
BARE_DOLLAR = re.compile(r'(?<!\\)\$(?!\()[A-Za-z_?{]')

#  Match a wsl invocation that carries a -c (or --command) string.
WSL_CALL = re.compile(r'(?:^|[|;&]|\s)wsl(?:\.exe)?\b')
#  *** THE THIRD ALTERNATIVE WAS ADDED 2026-08-30 AFTER THIS GUARD FAILED TO FIRE
#  ON A REAL, COSTLY INSTANCE: `wsl -d Gentoo -- bash -lc '...'`. ***
#
#  `\s-c\b` requires a BARE -c.  `-lc` is a COMBINED SHORT-FLAG CLUSTER and is
#  perfectly idiomatic bash, so the guard walked straight past it.  The command ran
#  with every $VAR stripped: $O emptied, so a probe was handed /base/gxemul and
#  /fix/gxemul, measured NOTHING, and printed a table of `??` under a VERDICT line
#  reading 'declined' for BOTH legs.  A false PASS -- the shape this guard exists
#  to prevent -- and the controls in the table were the only thing that said so.
#
#  The cluster form is anchored to a SHELL NAME on purpose.  A bare `-[a-z]*c` would
#  also match `find ... -exec`, and a guard that BLOCKS a legitimate command is one
#  that gets switched off -- worse than a guard with a gap.  Requiring bash/sh/zsh/
#  dash immediately before the cluster admits the dangerous shape and nothing else.
DASH_C = re.compile(r'\s-c\b|\s--command\b'
                    r'|(?:bash|sh|zsh|dash)\s+-[a-zA-Z]*c\b')

#  A heredoc body and a comment line are PROSE.  The carrier records the general
#  class: a quoted marker re-arms the tool that reads it, and a guard that blocks
#  people writing ABOUT a defect is one that gets switched off.  Strip both
#  before looking for an invocation.  `<<<` is a here-STRING with no body.
HEREDOC = re.compile(r"""<<-?\s*(['"]?)([A-Za-z_][A-Za-z0-9_]*)\1""")


def _strip_mentions(cmd):
    """Drop heredoc bodies and comment lines, preserving line structure."""
    out = []
    lines = cmd.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith('#'):
            out.append('')
            i += 1
            continue
        m = HEREDOC.search(line)
        if m and '<<<' not in line:
            out.append(line[:m.start()])
            term = m.group(2)
            i += 1
            while i < len(lines) and lines[i].strip() != term:
                out.append('')
                i += 1
            i += 1                      # consume the terminator line itself
            continue
        out.append(line)
        i += 1
    return '\n'.join(out)


def _quoted_arg(text, pos):
    """The argument the -c introduces, WHICH MAY SPAN NEWLINES.

    Line-scoping's whole defect was stopping at the first newline.  A real
    invocation is `wsl ... -c '<string>'` and that string is frequently a
    multi-line script.  Falls back to the rest of the line when unquoted.
    """
    k = pos
    while k < len(text) and text[k] in ' \t':
        k += 1
    if k < len(text) and text[k] in ("'", '"'):
        q = text[k]
        end = text.find(q, k + 1)
        return text[k + 1:end if end != -1 else len(text)]
    nl = text.find('\n', k)
    return text[k:nl if nl != -1 else len(text)]


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        return 0
    data = json.loads(raw)

    if data.get("tool_name") != "Bash":
        return 0
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if not cmd:
        return 0

    #  *** SCOPED TO THE QUOTED -c ARGUMENT, AFTER STRIPPING PROSE. ***
    #
    #  This replaced LINE-SCOPING, which was measured to have FOUR defects
    #  (before_lineScoped.out in the controls dir, 14 of 18):
    #
    #    2 FALSE NEGATIVES -- a multi-line `bash -c '...'` block whose bare
    #      dollar sits on a later line than the -c.  That is the shape that
    #      actually bites.  It ran on 2026-08-29, through this hook, and lost
    #      both its variables: a `cmp` compared against /src/... and reported
    #      DIVERGED, and gcc looked for /src/devices/... and reported
    #      not-found.  TWO confident wrong answers from one stripped variable,
    #      and the guard built for exactly this was silent.
    #
    #    2 FALSE POSITIVES that line-scoping never fixed.  It was adopted to
    #      stop firing on prose ABOUT the defect -- and a control of the very
    #      shape its own comment cited (a heredoc whose COMMENTS mention
    #      `wsl ... -c`) still fired.  It killed two INSTANCES, not the CLASS,
    #      because those two happened to split across lines.
    #
    #  The discriminator was never WHICH LINE the dollar is on.  It is whether
    #  the text is an INVOCATION or a MENTION.
    text = _strip_mentions(cmd)
    hits = []
    for m in DASH_C.finditer(text):
        head = text[:m.start()]
        #  The -c must belong to a wsl call.  Check the segment since the last
        #  command separator so an unrelated `-c` elsewhere is ignored.
        seg = re.split(r'[|;&\n]', head)[-1] if head else ''
        if not WSL_CALL.search(seg):
            continue
        hits.extend(BARE_DOLLAR.findall(_quoted_arg(text, m.end())))
    if not hits:
        return 0
    hits = sorted(set(hits))
    sys.stderr.write(
        "WSL DOLLAR GUARD -- this command will LOSE its shell variables.\n"
        "\n"
        "`wsl ... -c '<string>'` does not deliver `$?` or `$VARS` to the inner\n"
        "shell, EVEN INSIDE SINGLE QUOTES.  Measured, with controls, in\n"
        "GXEMUL-SEC/regress/artifacts/makercfalse/wsl_dollar_20260829.out.\n"
        "A variable set and used in one command comes back EMPTY, and the\n"
        "wrong answer REASSURES: an emptied loop variable once printed\n"
        "'(no binary)' for four trees that all had binaries.\n"
        "\n"
        "Bare dollar(s) found after the -c: %s\n"
        "\n"
        "TWO MEASURED-SAFE FORMS -- use either:\n"
        "  1. escape it            wsl -d Gentoo -- bash -c 'false; echo \\$?'\n"
        "  2. run a SCRIPT FILE    wsl -d Gentoo -- bash /mnt/c/.../script.sh\n"
        "\n"
        "`$(...)` is exempt: that is a deliberate outer-shell substitution.\n"
        "If you truly want git-bash to expand this before wsl sees it, use\n"
        "the $(...) form or assign to a variable first.\n"
        % ", ".join(hits))
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        #  Fail-safe: never wedge the session on this guard's own defect.
        #  NOTE: this cannot catch a SyntaxError in this file -- see the header.
        sys.exit(0)
