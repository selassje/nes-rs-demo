; MMIO registers
; Memory-Mapped Input/Output registers
PPUCTRL   = $2000
PPUMASK   = $2001
PPUSTATUS = $2002
PPUSCROLL = $2005
PPUADDR   = $2006
PPUDATA   = $2007

ASCII_A = $41 ; ASCII code of 'A'


.segment "HEADER"
;            EOF
.byte "NES", $1A
.byte 2         ; Number of 16KB PRG-ROM banks
.byte 1         ; Number of 8KB CHR-ROM banks
.byte %00000001 ; Vertical mirroring, no save RAM, no mapper
.byte %00000000 ; No special-case flags set, no mapper
.byte 0         ; No PRG-RAM present
.byte %00000000 ; NTSC format

.segment "CHR"
.incbin "../res/pattern_tables_2.chr" ; include the binary file created with NEXXT

.segment "RODATA" ; Prepare data separated from the logic in this segment
title: .asciiz "NES-0-RS" ; null-terminated string
build_version: .asciiz "Build: xxxxxx" ; null-terminated string

.segment "ZEROPAGE"
tmp:   .res 1
tmp_col:  .res 1
PPUCTRL_SHADOW: .res 1


.segment "CODE"
.export irq_handler
.proc irq_handler ; 6502 requires this handler
  RTI ; Just exit, we have no use for this handler in this program.
.endproc

.export nmi_handler
.proc nmi_handler ; 6502 requires this handler
  RTI ; Just exit, we have no use for this handler in this program.
.endproc

.export reset_handler
.proc reset_handler ; 6502 requires this handler
  SEI ; Deactivate IRQ (non-NMI interrupts)
  CLD ; Deactivate non-existing decimal mode
  ; NES CPU is a MOS 6502 clone without decimal mode
  LDX #%00000000
  STX PPUCTRL ; PPU is unstable on boot, ignore NMI for now
  STX PPUCTRL_SHADOW ; PPU is unstable on boot, ignore NMI for now
  STX PPUMASK ; Deactivate PPU drawing, so CPU can safely write to PPU's VRAM
  BIT PPUSTATUS ; Clear the vblank flag; its value on boot cannot be trusted
  vblankwait1: ; PPU unstable on boot, wait for vertical blanking
    BIT PPUSTATUS ; Clear the vblank flag;
    ; and store its value into bit 7 of CPU status register
    BPL vblankwait1 ; repeat until bit 7 of CPU status register is set (1)
  vblankwait2: ; PPU still unstable, wait for another vertical blanking
    BIT PPUSTATUS
    BPL vblankwait2
  ; PPU should be stable enough now

  ; RAM contents on boot cannot be trusted (visual artifacts)
  ; Clear nametable 0; It is at PPU VRAM's address $2000
  ; CPU registers size is 1 byte, but addresses size is 2 bytes
  LDA PPUSTATUS ; Clear w register,
  ; so the next write to PPUADDR is taken as the VRAM's address high byte.
  ; First, we need the high byte of $2000
  ;                                  ^^
  LDA #$20
  STA PPUADDR ; (this also sets the w register,
  ; so the next write to PPUADDR is taken as the VRAM's address low byte)
  ; Then, the low byte of  $2000
  ;                           ^^
  LDA #$00
  STA PPUADDR ; (this also clears the w register)

  LDX #0 ; index for inner loop; overflows after 256
  LDY #4 ; index for outer loop; repeat overflow 4 times
  empty_background:
    ; The size of a nametable is 1024 bytes
    ; 256 bytes * 4 = 1024 bytes
    ; A register already contains 0
    STA PPUDATA ; After writing, PPUADDR is automatically increased by 1
    INX
    BNE empty_background ; repeat until overflow
    DEY
    BNE empty_background ; repeat 4 times

  ; Background color (index 0 of first color palette)
  ; is at PPU's VRAM address 3f00
  LDX #$3f ; 3f00
  ;          ^^
  STX PPUADDR
  LDX #$00 ; 3f00
  ;            ^^
  STX PPUADDR
  ; Finally, we need indexes of two PPU's internal color
  LDA #$2A ; green for the transparency color (palette 0 color 0)
  STA PPUDATA
  LDA #$17 ; orange for the first background color (palette 0 color 1)
  STA PPUDATA
  LDA #$21   ; color 2: blue
  STA PPUDATA
  LDA #$0F   ; color 3: black
  STA PPUDATA

  LDX #10
  LDY #08
  JSR SetPPUAddr
  JSR SelectPatternTable_0
  LDX #0
 .scope
    print_big:
      LDA title,X
      BEQ done          ; end of string
      SEC
      SBC #ASCII_A
      CLC
      ASL A
      CLC
      ADC #$B4
      CLC
      STA PPUDATA       ; write top tile
      INX
      JMP print_big
    done:
  .endscope
  
  LDX #10
  LDY #09
  JSR SetPPUAddr
  JSR SelectPatternTable_0
  LDX #0
 .scope
    print_big:
      LDA title,X
      BEQ done          ; end of string
      SEC
      SBC #ASCII_A
      CLC
      ASL A
      CLC
      ADC #$B5
      CLC
      STA PPUDATA       ; write top tile
      INX
      JMP print_big
    done:
  .endscope
  
  JSR SelectPatternTable_0
  LDX #10
  LDY #12
  JSR SetPPUAddr
  LDX #0
  LDA build_version,X ; load first character of the string
  .scope
    print:
      STA PPUDATA ; write its ASCII code, which coincides with its tile index
      INX
      LDA build_version,X ; load next character of the string
      BNE print ; repeat until null character is loaded
  .endscope

  ; center viewer to nametable 0
  LDA #0
  STA PPUSCROLL ; X position (this also sets the w register)
  STA PPUSCROLL ; Y position (this also clears the w register)

  ;     BGRsbMmG
  LDA #%00001010
  STA PPUMASK ; Enable background drawing and leftmost 8 pixels of screen

  forever:
    JMP forever ; Make CPU wait forever, while PPU keeps drawing frames forever
.endproc

;-------------------------------------------
; SetPPUAddr
; X = column (0–31)
; Y = row    (0–29)
;-------------------------------------------
SetPPUAddr:
    STX tmp_col        ; save column

    ; ----- low byte -----
    TYA
    ASL A
    ASL A
    ASL A
    ASL A
    ASL A              ; A = (row * 32) low byte
    CLC
    ADC tmp_col
    STA tmp             ; low byte

    ; ----- high byte -----
    TYA
    LSR A
    LSR A
    LSR A              ; A = row / 8
    CLC
    ADC #$20            ; base nametable
    STA tmp_col         ; high byte

    ; ----- write PPUADDR -----
    LDA tmp_col
    STA PPUADDR
    LDA tmp
    STA PPUADDR
    RTS

SelectPatternTable_0:
    LDA PPUCTRL_SHADOW
    ORA #%00000000        ; select background pattern table $1000
    STA PPUCTRL
    STA PPUCTRL_SHADOW
    RTS
SelectPatternTable_1:
    LDA PPUCTRL_SHADOW    ; select background pattern table $1000 (alternate) (default)
    ORA #%00001000
    STA PPUCTRL
    STA PPUCTRL_SHADOW
    RTS


.segment "VECTORS" ; 6502 requires this segment
.addr nmi_handler, reset_handler, irq_handler
