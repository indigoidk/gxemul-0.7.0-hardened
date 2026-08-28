#include <stdio.h>
enum { GDROM_W_LEN_B, GDROM_W_NODATA_B, GDROM_W_NOTWAIT_B,
       GDROM_W_OVERREAD_B, GDROM_W_DMANODATA_B, GDROM_W_DMAARM_B, GDROM_W_NBITS };
#define GDROM_W_LEN       (1u << GDROM_W_LEN_B)
#define GDROM_W_NODATA    (1u << GDROM_W_NODATA_B)
#define GDROM_W_NOTWAIT   (1u << GDROM_W_NOTWAIT_B)
#define GDROM_W_OVERREAD  (1u << GDROM_W_OVERREAD_B)
#define GDROM_W_DMANODATA (1u << GDROM_W_DMANODATA_B)
#define GDROM_W_DMAARM    (1u << GDROM_W_DMAARM_B)
int main(void){
  unsigned want[6]={0x01,0x02,0x04,0x08,0x10,0x20};
  unsigned got[6]={GDROM_W_LEN,GDROM_W_NODATA,GDROM_W_NOTWAIT,
                   GDROM_W_OVERREAD,GDROM_W_DMANODATA,GDROM_W_DMAARM};
  int i,bad=0;
  for(i=0;i<6;i++){ if(got[i]!=want[i]){printf("  MISMATCH %d: 0x%02x want 0x%02x\n",i,got[i],want[i]);bad=1;} }
  printf("  GDROM_W_NBITS = %d, so %d bits remain free in a uint32_t\n", GDROM_W_NBITS, 32-GDROM_W_NBITS);
  printf(bad?"  MASKS DIFFER\n":"  ALL SIX MASKS BIT-IDENTICAL to the hand-assigned originals\n");
  return bad;
}
