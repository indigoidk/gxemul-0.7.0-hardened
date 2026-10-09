import io
p="mutr4.py"; L=io.open(p,newline="").read().split("\n")
# lines 51..58 (idx 50..57), 60..67 (59..66), 71..73 (70..72)
new_pop_force = ['    "N_pop_forceN": [(I, POP_TAIL, POP_TAIL.replace("ARM_FLAG_MODE);", "ARM_FLAG_MODE) | 0x80000000;", 1))],']
new_pop_or = ['    "N_pop_orold": [(I, POP_TAIL, POP_TAIL.replace("ARM_FLAG_MODE);", "ARM_FLAG_MODE) | (cpu->cd.arm.cpsr & 0xffffff00);", 1))],']
new_msr = ['    "M_msr_forceN": [(I, MSR_DEC, TB + TB + "mask &= ~(ARM_FLAG_MODE | 0x80000000);" + NL + TB + TB + "cpu->cd.arm.flags |= 8;" + NL)],']
L = L[:50] + new_pop_force + L[58:59] + new_pop_or + L[67:70] + new_msr + L[73:]
s="\n".join(L)
hdr = 'CUR = "(cpu->cd.arm.cpsr & ARM_FLAG_MODE)"'
s = s.replace(hdr, hdr + '\nNL, TB = chr(10), chr(9)\nPOP_TAIL = TB*3 + "    (cpu->cd.arm.cpsr & ARM_FLAG_MODE);" + NL + TB*2 + "}" + NL + NL + TB*2 + "switch_register_banks"', 1)
io.open(p,"w",newline="").write(s)
