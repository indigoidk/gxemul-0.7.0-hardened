import os, pty, select, sys, time
BIN = sys.argv[1]; label = sys.argv[2]
open("/tmp/pcc2_dummy_p5.bin","wb").write(b"\0\0\0\0")
pid, fd = pty.fork()
if pid == 0:
    os.execv(BIN, [BIN, "-V", "-x", "-E", "mvme88k", "-e", "mvme187", "-M", "64", "0x10000:/tmp/pcc2_dummy_p5.bin"]); os._exit(127)
buf = ""
def rd(t):
    global buf
    end = time.time() + t
    while time.time() < end:
        r,_,_ = select.select([fd],[],[],0.1)
        if not r: continue
        try:
            d = os.read(fd, 65536)
            if not d: return
            buf += d.decode("latin-1","replace")
        except OSError: return
rd(1.5)
for c in ["put h 0xfff42003, 0xaabb", "quit"]:
    os.write(fd, (c+"\n").encode()); rd(1.2)
try: os.waitpid(pid, 0)
except OSError: pass
buf = buf.replace("\r","")
open("/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/pcc2p5_fable/pty_%s.txt" % label, "w").write(buf)
print("%s: FAILED!=%d  'failed ]'=%d  declined=%d  DATA_ACCESS/exception=%d" % (label, buf.count("FAILED!"), buf.count("failed ]"), buf.count("declined."), buf.lower().count("exception")))
