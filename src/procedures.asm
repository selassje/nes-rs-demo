.export PrintSmallACII
.export PrintBigTiles
.export SetScroll
.export WaitPPUStable


.include "registers.inc"

.importzp PPUCTRL_SHADOW
.importzp tmp_1
.importzp tmp_2
.importzp ptr_1

;-------------------------------------------
; Wait for PPU to be stable
;-------------------------------------------
.proc WaitPPUStable
  LDX #%00000000
  STX PPUCTRL
  STX PPUCTRL_SHADOW
  STX PPUMASK
  BIT PPUSTATUS
  vblankwait1:
    BIT PPUSTATUS
    BPL vblankwait1
  vblankwait2:
    BIT PPUSTATUS
    BPL vblankwait2
  LDA PPUSTATUS
  RTS
.endproc

;-------------------------------------------
; Print a small text starting at a given position
; X = column (0–31)
; Y = row    (0–29)
; ptr_1 = pointer to string
;-------------------------------------------
.proc PrintSmallACII
  JSR SetPPUAddr
  LDY #0
  print:
    LDA (ptr_1),Y
    BEQ done
    STA PPUDATA
    INY
    JMP print
  done:
    RTS
.endproc

;-------------------------------------------
; Print text using the 8x16 font tiles
; X = column (0–31)
; Y = row    (0–29)
; ptr_1 = pointer to the left tile indexes of the text
;-------------------------------------------
.proc PrintBigTiles
  JSR SetPPUAddr
  STY tmp_1
  LDY #0
  print_upper:
    LDA (ptr_1),Y
    BEQ end_upper
    STA PPUDATA
    INY
    JMP print_upper
  end_upper:
    LDY tmp_1
    INY
    JSR SetPPUAddr
    LDY #0
  print_lower:
    LDA (ptr_1),Y
    BEQ done
    CLC
    ADC #1
    STA PPUDATA
    INY
    JMP print_lower
  done:
    RTS
.endproc

;-------------------------------------------
; SetPPUAddr
; X = column (0–31)
; Y = row    (0–29)
;-------------------------------------------
.proc SetPPUAddr
    STX tmp_1        ; save column

    ; ----- low byte -----
    TYA
    ASL A
    ASL A
    ASL A
    ASL A
    ASL A              ; A = (row * 32) low byte
    CLC
    ADC tmp_1        ; low byte
    STA tmp_2             ; low byte

    ; ----- high byte -----
    TYA
    LSR A
    LSR A
    LSR A              ; A = row / 8
    CLC
    ADC #$20            ; base nametable
    STA tmp_1         ; high byte

    ; ----- write PPUADDR -----
    LDA tmp_1
    STA PPUADDR
    LDA tmp_2
    STA PPUADDR
    RTS
.endproc

.proc SelectPatternTable_0
    LDA PPUCTRL_SHADOW
    ORA #%00000000 
    STA PPUCTRL
    STA PPUCTRL_SHADOW
    RTS
  .endproc
  
.proc SelectPatternTable_1
    LDA PPUCTRL_SHADOW
    ORA #%00001000
    STA PPUCTRL
    STA PPUCTRL_SHADOW
    RTS
.endproc

.proc SetScroll
    STX PPUSCROLL
    STY PPUSCROLL
    RTS
.endproc
