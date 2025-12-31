.include "registers.inc"
.include "macros.inc"

.importzp PPUCTRL_SHADOW
.importzp ptr_1
.import build_version
.import title_tiles
.import WaitPPUStable
.import PrintSmallACII
.import PrintBigTiles
.import SetScroll

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
.incbin "../res/pattern_tables.chr"

.segment "CODE"
.export irq_handler
.proc irq_handler
  RTI
.endproc

.export nmi_handler
.proc nmi_handler
  RTI
.endproc

.export reset_handler
.proc reset_handler ; 6502 requires this handler
  SEI
  CLD
  JSR WaitPPUStable
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

  PRINT_BIG 10, 8, title_tiles
  PRINT_SMALL 10, 12, build_version

  ; center viewer to nametable 0
  SCROLL 0, 0

  ;     BGRsbMmG
  LDA #%00001000
  STA PPUMASK ; Enable background drawing and leftmost 8 pixels of screen

  forever:
    JMP forever ; Make CPU wait forever, while PPU keeps drawing frames forever
.endproc


.segment "VECTORS" ; 6502 requires this segment
.addr nmi_handler, reset_handler, irq_handler
