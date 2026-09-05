import sys, types, io, contextlib
for _m in ("pty","select","termios","fcntl"):
    sys.modules.setdefault(_m, types.ModuleType(_m))
src = open("probe_dry.py").read()
ns = {"__name__": "__main__"}
with contextlib.redirect_stdout(io.StringIO()):
    try:
        exec(compile(src, "probe_dry.py", "exec"), ns)
    except SystemExit:
        pass
names = [n for n, _ in ns["rows"]]
open("emitted_names.txt", "w").write("\n".join(names) + "\n")
print("EMITTED_COUNT=%d" % len(names))
print("DUP=%d" % (len(names) - len(set(names))))
