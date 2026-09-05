import re
b=open('/mnt/c/Users/User00/AppData/Local/Temp/claude/C--DocumentNoSnc-CC-GXEMUL/8e474f41-4d47-4c99-bf11-3406a84c4fcd/scratchpad/brief_pcc2_p10.md',encoding='utf-8',errors='replace').read()
fence = chr(96)*3
m=re.search(r'## THE REPAIR DIFF.*?\n'+fence+r'diff\n(.*?)\n'+fence, b, re.S)
if not m:
    print("NO DIFF BLOCK FOUND"); raise SystemExit
d=m.group(1)
print('brief hunks:', len(re.findall(r'^@@', d, re.M)))
print('brief added:', len(re.findall(r'^\+[^+]', d, re.M)), 'removed:', len(re.findall(r'^-[^-]', d, re.M)))
# enclosing code section
fence2 = chr(96)*3
m2=re.search(r'## THE ENCLOSING CODE([^\n]*)\n\n'+fence2+r'c\n(.*?)\n'+fence2, b, re.S)
print()
print('ENCLOSING CODE heading:', m2.group(1) if m2 else 'NOT FOUND')
if m2:
    body=m2.group(2)
    print('ENCLOSING CODE block, %d lines:' % len(body.split(chr(10))))
    for ln in body.split(chr(10)):
        print('   |'+ln)
