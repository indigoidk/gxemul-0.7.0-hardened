#include <stdio.h>
#include <stddef.h>
#include <stdint.h>
#define DEV_SGI_DE_LENGTH 0x1000
#define DEV_SGI_MTE_LENGTH 0x1000
struct sgi_re_data {
	uint16_t	re_tlb_a[256];
	uint16_t	re_tlb_b[256];
	uint16_t	re_tlb_c[256];
	uint16_t	re_tex[112];
	uint32_t	re_linear_a[32];
	uint32_t	re_linear_b[32];
	uint32_t	de_reg[DEV_SGI_DE_LENGTH / sizeof(uint32_t)];
	uint32_t	mte_reg[DEV_SGI_MTE_LENGTH / sizeof(uint32_t)];
};
int main(void){
	struct sgi_re_data d;
	printf("sizeof struct        = %zu\n", sizeof d);
	printf("off re_linear_a      = %zu\n", offsetof(struct sgi_re_data, re_linear_a));
	printf("off re_linear_b      = %zu\n", offsetof(struct sgi_re_data, re_linear_b));
	printf("off de_reg           = %zu\n", offsetof(struct sgi_re_data, de_reg));
	printf("&re_linear_a[32]     = %+d bytes rel re_linear_b[0]\n",
	    (int)((char*)&d.re_linear_a[32] - (char*)&d.re_linear_b[0]));
	printf("&re_linear_b[32]     = %+d bytes rel de_reg[0]\n",
	    (int)((char*)&d.re_linear_b[32] - (char*)&d.de_reg[0]));
	printf("re_linear_a[32] IS re_linear_b[0] : %s\n",
	    ((void*)&d.re_linear_a[32]==(void*)&d.re_linear_b[0])?"YES":"NO");
	printf("re_linear_b[32] IS de_reg[0]      : %s\n",
	    ((void*)&d.re_linear_b[32]==(void*)&d.de_reg[0])?"YES":"NO");
	return 0;
}
