	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 13, 0	sdk_version 13, 3
	.globl	_getFileData                    ; -- Begin function getFileData
	.p2align	2
_getFileData:                           ; @getFileData
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #80
	.cfi_def_cfa_offset 80
	stp	x29, x30, [sp, #64]             ; 16-byte Folded Spill
	add	x29, sp, #64
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	stur	x0, [x29, #-16]
	ldur	x0, [x29, #-16]
	adrp	x1, l_.str@PAGE
	add	x1, x1, l_.str@PAGEOFF
	bl	_fopen
	stur	x0, [x29, #-24]
	ldur	x0, [x29, #-24]
	mov	x1, #0
	str	x1, [sp, #8]                    ; 8-byte Folded Spill
	mov	w2, #2
	bl	_fseek
	ldur	x0, [x29, #-24]
	bl	_ftell
	ldr	x1, [sp, #8]                    ; 8-byte Folded Reload
	str	x0, [sp, #32]
	ldur	x0, [x29, #-24]
	mov	w2, #0
	bl	_fseek
	ldr	x8, [sp, #32]
	add	x0, x8, #1
	bl	_malloc
	str	x0, [sp, #24]
	ldr	x8, [sp, #24]
	subs	x8, x8, #0
	cset	w8, ne
	tbnz	w8, #0, LBB0_2
	b	LBB0_1
LBB0_1:
	ldur	x0, [x29, #-24]
	bl	_fclose
	adrp	x8, l_.str.1@PAGE
	add	x8, x8, l_.str.1@PAGEOFF
	stur	x8, [x29, #-8]
	b	LBB0_5
LBB0_2:
	ldr	x0, [sp, #24]
	ldr	x2, [sp, #32]
	ldur	x3, [x29, #-24]
	mov	x1, #1
	bl	_fread
	str	x0, [sp, #16]
	ldr	x8, [sp, #16]
	ldr	x9, [sp, #32]
	subs	x8, x8, x9
	cset	w8, eq
	tbnz	w8, #0, LBB0_4
	b	LBB0_3
LBB0_3:
	ldr	x0, [sp, #24]
	bl	_free
	ldur	x0, [x29, #-24]
	bl	_fclose
	adrp	x8, l_.str.2@PAGE
	add	x8, x8, l_.str.2@PAGEOFF
	stur	x8, [x29, #-8]
	b	LBB0_5
LBB0_4:
	ldr	x8, [sp, #24]
	ldr	x9, [sp, #32]
	add	x8, x8, x9
	strb	wzr, [x8]
	ldur	x0, [x29, #-24]
	bl	_fclose
	ldr	x8, [sp, #24]
	stur	x8, [x29, #-8]
	b	LBB0_5
LBB0_5:
	ldur	x0, [x29, #-8]
	ldp	x29, x30, [sp, #64]             ; 16-byte Folded Reload
	add	sp, sp, #80
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:
	stp	x29, x30, [sp, #-16]!           ; 16-byte Folded Spill
	.cfi_def_cfa_offset 16
	mov	x29, sp
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	sub	sp, sp, #96
	adrp	x8, ___stack_chk_guard@GOTPAGE
	ldr	x8, [x8, ___stack_chk_guard@GOTPAGEOFF]
	ldr	x8, [x8]
	stur	x8, [x29, #-8]
	stur	wzr, [x29, #-12]
	adrp	x8, l_.str.3@PAGE
	add	x8, x8, l_.str.3@PAGEOFF
	stur	x8, [x29, #-24]
	ldur	x0, [x29, #-24]
	bl	_getFileData
	stur	x0, [x29, #-32]
	stur	wzr, [x29, #-36]
	stur	wzr, [x29, #-40]
	stur	wzr, [x29, #-44]
	b	LBB1_1
LBB1_1:                                 ; =>This Inner Loop Header: Depth=1
	ldursw	x8, [x29, #-44]
	stur	x8, [x29, #-72]                 ; 8-byte Folded Spill
	ldur	x0, [x29, #-32]
	bl	_strlen
	ldur	x8, [x29, #-72]                 ; 8-byte Folded Reload
	subs	x8, x8, x0
	cset	w8, hs
	tbnz	w8, #0, LBB1_6
	b	LBB1_2
LBB1_2:                                 ;   in Loop: Header=BB1_1 Depth=1
	ldur	x8, [x29, #-32]
	ldursw	x9, [x29, #-44]
	ldrsb	w8, [x8, x9]
	subs	w8, w8, #10
	cset	w8, ne
	tbnz	w8, #0, LBB1_4
	b	LBB1_3
LBB1_3:                                 ;   in Loop: Header=BB1_1 Depth=1
	ldur	w8, [x29, #-36]
	add	w8, w8, #1
	stur	w8, [x29, #-36]
	b	LBB1_4
LBB1_4:                                 ;   in Loop: Header=BB1_1 Depth=1
	ldur	w8, [x29, #-40]
	add	w8, w8, #1
	stur	w8, [x29, #-40]
	b	LBB1_5
LBB1_5:                                 ;   in Loop: Header=BB1_1 Depth=1
	ldur	w8, [x29, #-44]
	add	w8, w8, #1
	stur	w8, [x29, #-44]
	b	LBB1_1
LBB1_6:
	ldur	w8, [x29, #-36]
                                        ; kill: def $x8 killed $w8
	mov	x9, sp
	stur	x9, [x29, #-56]
	lsl	x9, x8, #3
	add	x9, x9, #15
	and	x9, x9, #0xfffffffffffffff0
	stur	x9, [x29, #-88]                 ; 8-byte Folded Spill
	adrp	x16, ___chkstk_darwin@GOTPAGE
	ldr	x16, [x16, ___chkstk_darwin@GOTPAGEOFF]
	blr	x16
	ldur	x10, [x29, #-88]                ; 8-byte Folded Reload
	mov	x9, sp
	subs	x0, x9, x10
	mov	sp, x0
	stur	x8, [x29, #-64]
	stur	wzr, [x29, #-12]
	ldur	x8, [x29, #-56]
	mov	sp, x8
	ldur	w8, [x29, #-12]
	stur	w8, [x29, #-76]                 ; 4-byte Folded Spill
	ldur	x9, [x29, #-8]
	adrp	x8, ___stack_chk_guard@GOTPAGE
	ldr	x8, [x8, ___stack_chk_guard@GOTPAGEOFF]
	ldr	x8, [x8]
	subs	x8, x8, x9
	cset	w8, eq
	tbnz	w8, #0, LBB1_8
	b	LBB1_7
LBB1_7:
	bl	___stack_chk_fail
LBB1_8:
	ldur	w0, [x29, #-76]                 ; 4-byte Folded Reload
	mov	sp, x29
	ldp	x29, x30, [sp], #16             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.section	__TEXT,__cstring,cstring_literals
l_.str:                                 ; @.str
	.asciz	"r"

l_.str.1:                               ; @.str.1
	.asciz	"MEMORY ALLOCATION FAILED CHECK FILE\n"

l_.str.2:                               ; @.str.2
	.asciz	"ERROR READING FILE\n"

l_.str.3:                               ; @.str.3
	.asciz	"./BRCA2_hg38_extracted.txt"

.subsections_via_symbols
