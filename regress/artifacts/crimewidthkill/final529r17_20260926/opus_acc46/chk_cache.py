import pickle, sys
c = pickle.load(open(sys.argv[1], "rb"))
n_init = sum(t.count("[ACC46INIT n=0]") for _, t, _ in c)
n_hit = sum(t.count("[ACC46HIT") for _, t, _ in c)
clean = sum(1 for _, _, k in c if k)
with_init = sum(1 for _, t, _ in c if "[ACC46INIT n=0]" in t)
print("sessions=%d clean=%d init_markers=%d sessions_with_init=%d hit_markers=%d" % (len(c), clean, n_init, with_init, n_hit))
i = [j for j, (_, t, _) in enumerate(c) if "[ACC46INIT" in t][0]
t = c[i][1]; p = t.index("[ACC46INIT")
print(repr(t[max(0, p - 160):p + 60]))
