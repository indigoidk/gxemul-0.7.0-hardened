#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
#define DEV_SGI_DE_LENGTH 0x1000
#define DEV_SGI_MTE_LENGTH 0x1000
/* SHIPPED struct: warned LAST */
struct ship {
	uint16_t re_tlb_a[256]; uint16_t re_tlb_b[256]; uint16_t re_tlb_c[256];
	uint16_t re_tex[112];
	uint32_t re_linear_a[32];
	uint32_t re_linear_b[32];
	uint32_t de_reg[DEV_SGI_DE_LENGTH/sizeof(uint32_t)];
	uint32_t mte_reg[DEV_SGI_MTE_LENGTH/sizeof(uint32_t)];
	uint32_t warned;
};
int main(void){
	struct ship d; int bad = 0;
	int a = ((void*)&d.re_linear_a[32]==(void*)&d.re_linear_b[0]);
	int b = ((void*)&d.re_linear_b[32]==(void*)&d.de_reg[0]);
	int c = ((void*)&d.re_linear_b[32]==(void*)&d.warned);
	printf("SHIPPED STRUCT (warned last):\n");
	printf("  re_linear_a[32] IS re_linear_b[0] : %s\n", a?"YES":"NO");
	printf("  re_linear_b[32] IS de_reg[0]      : %s\n", b?"YES":"NO");
	printf("  re_linear_b[32] IS warned         : %s\n", c?"YES <-- BAD":"no  (good)");
	if(!a||!b||c) bad=1;
	printf("ADJACENCY_AS_DOCUMENTED=%s\n", bad?"NO":"YES");
	return bad;
}
