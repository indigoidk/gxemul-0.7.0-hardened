#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
#define DEV_SGI_DE_LENGTH 0x1000
#define DEV_SGI_MTE_LENGTH 0x1000
/* POST-FIX struct AS SHIPPED: warned inserted after re_linear_b */
struct post {
	uint16_t re_tlb_a[256]; uint16_t re_tlb_b[256]; uint16_t re_tlb_c[256];
	uint16_t re_tex[112];
	uint32_t re_linear_a[32];
	uint32_t re_linear_b[32];
	uint32_t warned;
	uint32_t de_reg[DEV_SGI_DE_LENGTH/sizeof(uint32_t)];
	uint32_t mte_reg[DEV_SGI_MTE_LENGTH/sizeof(uint32_t)];
};
int main(void){
	struct post d;
	printf("POST-FIX AS SHIPPED:\n");
	printf("  re_linear_b[32] IS de_reg[0] : %s\n",
	  ((void*)&d.re_linear_b[32]==(void*)&d.de_reg[0])?"YES":"NO  <-- COMMENT IS FALSE");
	printf("  re_linear_b[32] IS warned    : %s\n",
	  ((void*)&d.re_linear_b[32]==(void*)&d.warned)?"YES <-- it hits the LATCH":"no");
	printf("  re_linear_a[32] IS re_linear_b[0] : %s\n",
	  ((void*)&d.re_linear_a[32]==(void*)&d.re_linear_b[0])?"YES":"NO");
	return 0;
}
