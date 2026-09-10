#!/usr/bin/env python3
#
#  #518 lcabadval kill-table MUTATOR, BATCH B.
#
#  A SEPARATE FILE ON PURPOSE.  Batch A's driver invokes `mutate518.py' once per mutant, and
#  python re-reads the whole file at every invocation -- so editing it mid-table would give
#  different mutants different mutators.  That is the carrier's frozen-copy rule in its python
#  form, and the same hazard that put a moving BASELINE under the first run of this table.
#  Adding dict keys would in fact have been harmless; this costs one file and needs no argument.
#
#  These two mutants were derived from the REPAIRED probe (asrun2) rather than from the code:
#  each targets a row that pass 2 ADDED, asking whether the new row can actually observe the
#  mutant it was written for.
import sys
import mutate518 as A

BASEMASK = A.BASEMASK

EXTRA = {
    #  M35: glm's OWN named mutant for the `wmask0 hif' row -- take the field from the RAW idata
    #  instead of from the masked v, so a write carrying bit 32 is DECLINED rather than masked
    #  down and accepted.  The row drives 0x100100000 and wants 0x100000 -- but 0x100000 is
    #  ALREADY in the register from the phase before it, so "masked, then accepted" and
    #  "declined, previous value kept" read back the SAME value.  Predicted: cannot fire.
    "M35_field_from_idata": ("f = v >> 20;", "f = idata >> 20;", 0),

    #  M37: the CONF announce predicate NARROWED from a bit test to an equality.  Every value any
    #  row drives with bit 1 set is either exactly 0x2 (which still announces) or is written in a
    #  session whose only announce-count row is satisfied by a LATER 0x2 write.  So the two
    #  values that would expose it -- 0x100000002 and 0x6 -- are each in a session that does not
    #  count that announce.  A guest setting type-1 cycles together with any other bit then gets
    #  NO diagnostic at all.
    "M37_conf_ann_eq": ("if (idata & 0x2ULL)", "if (idata == 0x2ULL)", 0),
}

A.M.update(EXTRA)

if __name__ == "__main__":
    if sys.argv[1] == "--list":
        for k in EXTRA:
            print(k)
    elif sys.argv[1] == "--restore":
        import shutil
        shutil.copyfile(A.SEC, A.CLONE)
        print("RESTORED from the frozen baseline")
    else:
        A.apply_one(sys.argv[1])
