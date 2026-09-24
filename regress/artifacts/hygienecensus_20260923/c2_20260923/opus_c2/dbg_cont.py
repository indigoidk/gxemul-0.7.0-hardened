import io, tokenize, sys
EW = "ends" + "with"
variants = {
 "cont_mid":   "x = buf.rstrip() \\n     .%s(\"GXemul>\")\n" % EW,
 "cont_after_call": "x = buf.rstrip().%s(\\n     \"GXemul>\")\n" % EW,
 "cont_simple": "x = 1 + \\n    2\n",
 "no_cont":    "x = buf.rstrip().%s(\"GXemul>\")\n" % EW,
}
for name, src in variants.items():
    print("==", name, repr(src))
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
        print("   tokens:", [(tokenize.tok_name[t.type], t.string) for t in toks if t.type not in
              (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT, tokenize.ENCODING, tokenize.ENDMARKER)])
    except Exception as e:
        print("   EXC", type(e).__name__, repr(str(e)))
print(sys.version)
