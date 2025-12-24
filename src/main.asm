.segment "HEADER"
.byte "NES", $1A
.byte 1        ; 1 x 16KB PRG
.byte 1        ; 1 x 8KB CHR
.byte $00
.byte $00
.res 8, 0

.segment "CODE"

RESET:
    sei
    cld
    ldx #$FF
    txs

    inx
    stx $2000
    stx $2001
    stx $4010

vblank_wait:
    bit $2002
    bpl vblank_wait

    lda #$3F
    sta $2006
    lda #$00
    sta $2006

    lda #$0F
    sta $2007

    lda #$20
    sta $2006
    lda #$00
    sta $2006

    ldx #0
print_loop:
    lda message, x
    beq done
    sta $2007
    inx
    bne print_loop

done:
    lda #%10000000
    sta $2000
    lda #%00011110
    sta $2001

forever:
    jmp forever

message:
    .byte "HELLO NES-RS", 0

.segment "VECTORS"
.word RESET
.word RESET
.word RESET

