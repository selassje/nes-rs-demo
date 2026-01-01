.macro PRINT_BIG col, row, label
  LDX #col
  LDY #row
  LDA #<label
  STA ptr_1
  LDA #>label
  STA ptr_1+1
  JSR PrintBigTiles
.endmacro

.macro PRINT_SMALL col, row, label
    LDX #col
    LDY #row
    LDA #<label
    STA ptr_1
    LDA #>label
    STA ptr_1+1
    JSR PrintSmallACII
.endmacro

.macro SCROLL col, row
    LDX #col
    LDY #row
    JSR SetScroll
.endmacro

.macro SET_BACKGOUND_COLORS clr_1, clr_2, clr_3, clr_4
    LDX #clr_1
    LDY #clr_2
    LDA #clr_3
    STA tmp_1
    LDA #clr_4
    STA tmp_2
    JSR SetBackgroundColors
.endmacro

.macro ENABLE_BACKGROUND_DRAWING
    JSR EnableBackgroundDrawing
.endmacro

.macro FILL_BACKGROUND tile_index
    LDA #tile_index
    JSR FillBackground
.endmacro