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

.macro SET_BG_COLORS index, clr_1, clr_2, clr_3
    LDX #index
    LDY #clr_1
    LDA #clr_2
    STA tmp_1
    LDA #clr_3
    STA tmp_2
    JSR SetPaletteColors
.endmacro

.macro SET_SPRITE_COLORS index, clr_1, clr_2, clr_3
  SET_BG_COLORS (index + 4),clr_1,clr_2,clr_3
.endmacro

.macro SET_UNIVERSAL_BACKGROUND_COLOR clr
    LDX #clr
    JSR SetUniversalBackgroundColor
.endmacro

.macro ENABLE_BACKGROUND_DRAWING
    JSR EnableBackgroundDrawing
.endmacro

.macro FILL_BACKGROUND tile_index
    LDA #tile_index
    JSR FillBackground
.endmacro