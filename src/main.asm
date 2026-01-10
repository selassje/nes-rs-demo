.include "registers.inc"
.include "macros.inc"
.include "colors.inc"

.importzp ptr_1
.importzp ptr_2
.importzp tmp_1
.importzp tmp_2
.import build_version
.import title_tiles
.import test_text
.import title_row0
.import title_row1
.import title_row2
.import title_row3
.import WaitPPUStable
.import PrintSmallACII
.import PrintBigTiles
.import Print16x16Tiles
.import SetScroll
.import SetPaletteColors
.import SetUniversalBackgroundColor
.import EnableBackgroundDrawing
.import FillBackground

.segment "HEADER"
.byte "NES", $1A
.byte 2         ; Number of 16KB PRG-ROM banks
.byte 1         ; Number of 8KB CHR-ROM banks
.byte %00000001 ; Vertical mirroring, no save RAM, no mapper
.byte %00000000 ; No special-case flags set, no mapper
.byte 0         ; No PRG-RAM present
.byte %00000000 ; NTSC format

.segment "CHR"
.incbin "../res/generated_pattern.chr"

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
.proc reset_handler
  SEI
  CLD
  JSR WaitPPUStable

  FILL_BACKGROUND $00

  SET_UNIVERSAL_BACKGROUND_COLOR COLOR_BLACK
  SET_BG_COLORS 0, COLOR_GREEN, COLOR_LIGHT_BLUE, COLOR_BLACK
  SET_SPRITE_COLORS 0, COLOR_GREEN, COLOR_LIGHT_BLUE, COLOR_BLACK

  ; Big 32x32 Mega Man style title "NES-RS"
  ; 6 chars * 4 tiles = 24 tiles wide, centered at column 4
  PRINT_SMALL 4, 6, title_row0
  PRINT_SMALL 4, 7, title_row1
  PRINT_SMALL 4, 8, title_row2
  PRINT_SMALL 4, 9, title_row3
  PRINT_SMALL 10, 12, build_version

  SCROLL 0, 0

  ENABLE_BACKGROUND_DRAWING

  forever:
    JMP forever
.endproc


.segment "VECTORS"
.addr nmi_handler, reset_handler, irq_handler
