#!/usr/bin/env python3
"""Apply the brief's section-4 fix (member 3 at all five sites) to the clone's
dev_footbridge.c.  Text-exact replacements; every one must match exactly once,
or the script refuses (a mutant whose text is not found is a silent no-op, and
this project grades MUTANT-TEXT-NOT-FOUND as a FAIL).
usage: mkfix.py <path-to-dev_footbridge.c> [variant]

variants for the Q2 weakening table ('fix' is the proposal as written):
  fix        the proposal
  m_keepexit keep exit(1) at ONE site (+0x284)            [Q2 a]
  m_unlatch  the announce fires on every access           [Q2 b]
  m_sharebit one latch bit shared by +0x180 and +0x184    [Q2 c]
  m_leak18c  the +0x18c decline keeps odata=d->irq_enable [Q2 d]
  m_store180 the +0x180 decline stores idata into status  [Q2 e]
  m_swallow  IRQ_STATUS READ also returns 0               [Q2 f]
  m_misname  the +0x184 announce names irq status         [Q2 g]
  m_latchrd  the +0x18c latch is cleared by its own read   [Q2 j]
  m_fiqleak  the +0x280 decline-side READ returns fiq_enable (the A4 question)
  m_fiqraw   the +0x280 READ drops the & (returns fiq_status)
"""
import io, sys

PATH = sys.argv[1]
VAR = sys.argv[2] if len(sys.argv) > 2 else "fix"
T3 = "\t\t\t"
T4 = "\t\t\t\t"

src = io.open(PATH, encoding="utf-8", newline="").read()


def sub(old, new, why):
    global src
    n = src.count(old)
    if n != 1:
        sys.stderr.write("REFUSED: %s matched %d times\n" % (why, n))
        sys.exit(9)
    src = src.replace(old, new)


def latch(bit, text):
    """The announce, at 3-tab indent, as the house idiom: per-instance latch
    field + fatal() carrying an explicit (once) suppression marker."""
    if VAR == "m_unlatch":
        return T3 + 'fatal("%s\\n");' % text
    out = [T3 + "if (!(d->warned_access & %s)) {" % bit,
           T4 + "d->warned_access |= %s;" % bit,
           T4 + 'fatal("%s\\n");' % text]
    if VAR == "m_latchrd" and bit == "FB_W_IRQ_ENABLE_CLEAR":
        out.append(T4 + "d->warned_access &= ~%s;" % bit)
    out.append(T3 + "}")
    return "\n".join(out)


#  ---- the struct field + the five bits ----
sub("""	uint32_t	fiq_status;
	uint32_t	fiq_enable;
};""",
    """	uint32_t	fiq_status;
	uint32_t	fiq_enable;

	/*  #540: one bit per declined site, cleared by DEVINIT's memset.  */
	uint32_t	warned_access;
};

#define	FB_W_IRQ_STATUS		0x01
#define	FB_W_IRQ_RAW_STATUS	0x02
#define	FB_W_IRQ_ENABLE_CLEAR	0x04
#define	FB_W_FIQ_STATUS		0x08
#define	FB_W_FIQ_RAW_STATUS	0x10""", "struct field")

B184 = "FB_W_IRQ_STATUS" if VAR in ("m_sharebit", "m_onebit") else "FB_W_IRQ_RAW_STATUS"


def bit(b):
    return "FB_W_IRQ_STATUS" if VAR == "m_onebit" else b


#  ---- +0x180 IRQ_STATUS ----
read180 = "odata = 0;" if VAR == "m_swallow" \
          else "odata = d->irq_status & d->irq_enable;"
body180 = latch("FB_W_IRQ_STATUS",
                "[ WARNING: footbridge write to irq status? (once) ]")
if VAR == "m_store180":
    body180 += "\n" + T3 + "d->irq_status = idata;"
sub("""		if (writeflag == MEM_READ)
			odata = d->irq_status & d->irq_enable;
		else {
			fatal("[ WARNING: footbridge write to irq status? ]\\n");
			exit(1);
		}""",
    "\t\tif (writeflag == MEM_READ)\n" + T3 + read180 +
    "\n\t\telse {\n" + body180 + "\n\t\t}", "+0x180")

#  ---- +0x184 IRQ_RAW_STATUS ----
t184 = "[ footbridge write to irq status (once) ]" if VAR == "m_misname" \
       else "[ footbridge write to irq_raw_status (once) ]"
sub(T3 + 'fatal("[ footbridge write to irq_raw_status ]\\n");\n' + T3 + "exit(1);",
    latch(B184, t184), "+0x184")

#  ---- +0x18c IRQ_ENABLE_CLEAR read ----
keep = (T3 + "odata = d->irq_enable;\n") if VAR == "m_leak18c" else ""
sub(T3 + "odata = d->irq_enable;\n" +
    T3 + 'fatal("[ WARNING: footbridge read from "\n' +
    "\t\t\t    \"ENABLE CLEAR? ]\\n\");\n" + T3 + "exit(1);",
    keep + latch(bit("FB_W_IRQ_ENABLE_CLEAR"),
                 "[ WARNING: footbridge read from ENABLE CLEAR? (once) ]"),
    "+0x18c")

#  ---- +0x280 FIQ_STATUS ----
read280 = "odata = d->fiq_status & d->fiq_enable;"
if VAR == "m_fiqleak":
    read280 = "odata = d->fiq_enable;"
elif VAR == "m_fiqraw":
    read280 = "odata = d->fiq_status;"
sub("""		if (writeflag == MEM_READ)
			odata = d->fiq_status & d->fiq_enable;
		else {
			fatal("[ WARNING: footbridge write to fiq status? ]\\n");
			exit(1);
		}""",
    "\t\tif (writeflag == MEM_READ)\n" + T3 + read280 + "\n\t\telse {\n" +
    latch(bit("FB_W_FIQ_STATUS"),
          "[ WARNING: footbridge write to fiq status? (once) ]") +
    "\n\t\t}", "+0x280")

#  ---- +0x284 FIQ_RAW_STATUS ----
body284 = latch(bit("FB_W_FIQ_RAW_STATUS"),
                "[ footbridge write to fiq_raw_status (once) ]")
if VAR == "m_keepexit":
    body284 += "\n" + T3 + "exit(1);"
sub(T3 + 'fatal("[ footbridge write to fiq_raw_status ]\\n");\n' + T3 + "exit(1);",
    body284, "+0x284")

io.open(PATH, "w", encoding="utf-8", newline="").write(src)
print("APPLIED variant=%s to %s" % (VAR, PATH))
