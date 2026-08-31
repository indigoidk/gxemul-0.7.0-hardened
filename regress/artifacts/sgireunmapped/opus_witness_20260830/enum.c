/* Enumeration of the sgi_re window cascade.
 * Predicates COPY-PASTED from GXEMUL-SEC/src/devices/dev_sgi_re.c and
 * constants taken from the REAL header, not transcribed. */
#include <stdio.h>
#include <stdint.h>
#include "thirdparty/crmfbreg.h"

int main(void)
{
    long total=0, kill=0;
    long w[8]={0,0,0,0,0,0,0,0};
    long killlo=-1, killhi=-1;
    long runs=0; int prevkill=0;

    printf("CONSTANTS AS COMPILED (not transcribed):\n");
    printf("  CRIME_RE_TLB_A    = 0x%x\n", CRIME_RE_TLB_A);
    printf("  CRIME_RE_TLB_B    = 0x%x\n", CRIME_RE_TLB_B);
    printf("  CRIME_RE_TLB_C    = 0x%x\n", CRIME_RE_TLB_C);
    printf("  CRIME_RE_TEX      = 0x%x\n", CRIME_RE_TEX);
    printf("  CRIME_RE_CLIP_IDS = 0x%x\n", CRIME_RE_CLIP_IDS);
    printf("  CRIME_RE_LINEAR_A = 0x%x\n", CRIME_RE_LINEAR_A);
    printf("  CRIME_RE_LINEAR_B = 0x%x\n", CRIME_RE_LINEAR_B);
    printf("\n");

    /* domain: registered at baseaddr+0x1000 with length 0x1000,
     * so handler receives relative_addr in [0,0x1000); it then does += 0x1000 */
    for (long raw = 0; raw < 0x1000; raw++) {
        uint64_t relative_addr = (uint64_t)raw;
        relative_addr += 0x1000;
        total++;
        int k = 0;
        if (relative_addr >= CRIME_RE_TLB_A && relative_addr < CRIME_RE_TLB_B) w[0]++;
        else if (relative_addr >= CRIME_RE_TLB_B && relative_addr < CRIME_RE_TLB_C) w[1]++;
        else if (relative_addr >= CRIME_RE_TLB_C && relative_addr < CRIME_RE_TLB_C + 0x200) w[2]++;
        else if (relative_addr >= CRIME_RE_TEX && relative_addr < CRIME_RE_TEX + 0xe0) w[3]++;
        else if (relative_addr >= CRIME_RE_LINEAR_A && relative_addr < CRIME_RE_LINEAR_A + 0x80) w[4]++;
        else if (relative_addr >= CRIME_RE_LINEAR_B && relative_addr < CRIME_RE_LINEAR_B + 0x80) w[5]++;
        else { k=1; kill++; }

        if (k && !prevkill) { runs++; killlo = relative_addr; }
        if (k) killhi = relative_addr;
        if (!k && prevkill) printf("  KILL RUN: 0x%lx - 0x%lx  (%ld bytes)\n", killlo, killhi, killhi-killlo+1);
        prevkill = k;
    }
    if (prevkill) printf("  KILL RUN: 0x%lx - 0x%lx  (%ld bytes)\n", killlo, killhi, killhi-killlo+1);

    printf("\n  TLB_A    matched %ld\n", w[0]);
    printf("  TLB_B    matched %ld\n", w[1]);
    printf("  TLB_C    matched %ld\n", w[2]);
    printf("  TEX      matched %ld\n", w[3]);
    printf("  LINEAR_A matched %ld\n", w[4]);
    printf("  LINEAR_B matched %ld\n", w[5]);
    printf("  ------------------------\n");
    printf("  walked   %ld\n", total);
    printf("  KILL     %ld   in %ld contiguous run(s)\n", kill, runs);
    printf("  sum      %ld\n", w[0]+w[1]+w[2]+w[3]+w[4]+w[5]+kill);

    /* the brief's specific claim */
    printf("\n  KSEG1 0xb5001800 -> raw 0x800 -> relative 0x%x -> %s\n",
        0x800+0x1000, "check below");
    {
        uint64_t relative_addr = 0x800; relative_addr += 0x1000;
        int hit = (relative_addr >= CRIME_RE_TLB_A && relative_addr < CRIME_RE_TLB_B)
               || (relative_addr >= CRIME_RE_TLB_B && relative_addr < CRIME_RE_TLB_C)
               || (relative_addr >= CRIME_RE_TLB_C && relative_addr < CRIME_RE_TLB_C + 0x200)
               || (relative_addr >= CRIME_RE_TEX && relative_addr < CRIME_RE_TEX + 0xe0)
               || (relative_addr >= CRIME_RE_LINEAR_A && relative_addr < CRIME_RE_LINEAR_A + 0x80)
               || (relative_addr >= CRIME_RE_LINEAR_B && relative_addr < CRIME_RE_LINEAR_B + 0x80);
        printf("    relative_addr=0x%llx  matched_a_window=%d  -> %s\n",
            (unsigned long long)relative_addr, hit, hit?"WINDOW":"FALLS TO THE KILL");
    }
    return 0;
}
