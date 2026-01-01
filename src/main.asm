.include "registers.inc"
.include "macros.inc"
.include "colors.inc"

.importzp ptr_1
.importzp tmp_1
.importzp tmp_2
.import build_version
.import title_tiles
.import WaitPPUStable
.import PrintSmallACII
.import PrintBigTiles
.import SetScroll
.import SetBackgroundColors
.import EnableBackgroundDrawing
.import FillBackground

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
.proc reset_handler
  SEI
  CLD
  JSR WaitPPUStable

  FILL_BACKGROUND $00

  SET_BACKGOUND_COLORS COLOR_LIME, COLOR_GREEN, COLOR_LIGHT_BLUE, COLOR_BLACK

  PRINT_BIG 10, 8, title_tiles
  PRINT_SMALL 10, 12, build_version

  SCROLL 0, 0

  ENABLE_BACKGROUND_DRAWING

  forever:
    JMP forever
.endproc


.segment "VECTORS"
.addr nmi_handler, reset_handler, irq_handler
