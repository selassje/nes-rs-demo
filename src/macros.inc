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