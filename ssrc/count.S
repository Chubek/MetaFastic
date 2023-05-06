count_bytes_til_newl:
	#define BYTE_PTR %rdi
	#define CNTR_PTR %rsi
	#define BYTE_LEN %rdx
	#define CNTR_REG %rcx
	#define BYTE_REG %r10b
	#define DWRD_REG %r10
	#define TEMP_REG %r11
	#define NEWL_NUM $10


	movq BYTE_LEN, CNTR_REG
	xorq DWRD_REG, DWRD_REG

1:
	movb (BYTE_PTR), BYTE_REG
	cmpb NEWL_NUM, BYTE_REG
	je 2f
	movq (CNTR_PTR, DWRD_REG), TEMP_REG
	incq TEMP_REG
	movq TEMP_REG, (CNTR_PTR, DWRD_REG)
	incq BYTE_PTR
	loop 1b

2:
	ret

	#undef BYTE_PTR
    #undef CNTR_PTR
    #undef BYTE_LEN
    #undef CNTR_REG
    #undef BYTE_REG
    #undef DWRD_REG
    #undef TEMP_REG
    #undef NEWL_NUM
