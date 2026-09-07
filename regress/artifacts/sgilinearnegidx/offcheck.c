/*  Settles the ONE derivation sgilinearnegidx rests on: does re_linear_a follow re_tex with
 *  no padding, so that re_linear_a[-1] lands on the guest-writable re_tex[110..111]?
 *
 *  Field order and types copied from struct sgi_re_data in dev_sgi_re.c.
 *  Printed rather than asserted, so a surprising answer is visible instead of silent.  */
#include <stdio.h>
#include <stddef.h>
#include <stdint.h>

struct layout {
	uint16_t	re_tlb_a[256];
	uint16_t	re_tlb_b[256];
	uint16_t	re_tlb_c[256];
	uint16_t	re_tex[112];
	uint32_t	re_linear_a[32];
};

int main(void)
{
	size_t tex_off  = offsetof(struct layout, re_tex);
	size_t tex_end  = tex_off + sizeof(((struct layout *)0)->re_tex);
	size_t lin_off  = offsetof(struct layout, re_linear_a);

	printf("  offsetof(re_tex)       = %zu\n", tex_off);
	printf("  re_tex ends at         = %zu\n", tex_end);
	printf("  offsetof(re_linear_a)  = %zu\n", lin_off);
	printf("  padding between        = %zu byte(s)\n", lin_off - tex_end);

	if (lin_off == tex_end) {
		printf("  => NO PADDING: re_linear_a[-1] is bytes %zu..%zu\n", lin_off - 4, lin_off - 1);
		printf("  => that is re_tex[110] and re_tex[111], both GUEST-WRITABLE\n");
	} else {
		printf("  => PADDING PRESENT: re_linear_a[-1] lands in padding, NOT on re_tex\n");
		printf("  => the escalation does NOT hold on this ABI\n");
	}
	return 0;
}
