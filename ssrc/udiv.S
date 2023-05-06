divide_numbers_with_reciprocals:
	#define DIVD_NUM %rdi
	#define DIVS_NUM %rsi
	#define MAGC_PTR %rdx
	#define CNTR_REG %rcx
	#define ACCM_REG %rax
	#define RETR_REG %rax
	#define MAGC_REG %r8
	#define SHR1_REG %r10
	#define SHR2_REG %r11
	#define UI24_MAX $0xffffff
	#define UI16_MAX $0xffff
	#define UI04_MAX $15
	#define UI32_BIT $32
	#define UI16_BIT $16
	#define UI08_BIT $8
	#define UI04_BIT $4

	movq (MAGC_PTR, DIVS_NUM), CNTR_REG
	movq CNTR_REG, MAGC_REG
	movq CNTR_REG, SHR1_REG
	movq CNTR_REG, SHR2_REG

	shrq UI04_BIT, SHR2_REG
	shrq UI08_BIT, MAGC_REG

	andq UI04_MAX, SHR1_REG
	andq UI04_MAX, SHR2_REG
	andq UI24_MAX, MAGC_REG

	movq DIVD_NUM, ACCM_REG
	mulq MAGC_REG
	shrq UI16_BIT, ACCM_REG
	andq UI16_MAX, ACCM_REG
	subq ACCM_REG, DIVD_NUM
	movq SHR1_REG, CNTR_REG
	shrq DIVD_NUM
	addq ACCM_REG, DIVD_NUM
	movq SHR2_REG, CNTR_REG
	shrq DIVD_NUM

	movq DIVD_NUM, RETR_REG
	ret


	#undef DIVD_NUM
	#undef DIVS_NUM
	#undef MAGC_PTR
	#undef CNTR_REG
	#undef ACCM_REG
	#undef RETR_REG
	#undef MAGC_REG
	#undef SHR1_REG
	#undef SHR2_REG
	#undef UI24_MAX
	#undef UI16_MAX
	#undef UI04_MAX
	#undef UI32_BIT
	#undef UI16_BIT
	#undef UI08_BIT
	#undef UI04_BIT