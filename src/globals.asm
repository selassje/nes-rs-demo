.exportzp tmp_1
.exportzp tmp_2
.exportzp ptr_1
.exportzp ptr_2
.exportzp PPUCTRL_SHADOW
.exportzp PPUMASK_SHADOW

.export build_version
.export title_tiles
.export test_text

; Old 8x16 font tile indices (for reference)
E_TILE = $BC
N_TILE = $CE
R_TILE = $D6
S_TILE = $D8
DASH_TILE = $EE

; Mega Man style 32x32 font tile indices (16 tiles per character, 4x4)
; Starting at $80, each char uses 16 consecutive tiles
; Layout: row0[0-3], row1[4-7], row2[8-11], row3[12-15]
BIG_N = $80   ; N uses $80-$8F
BIG_E = $90   ; E uses $90-$9F
BIG_S = $A0   ; S uses $A0-$AF
BIG_R = $B0   ; R uses $B0-$BF
BIG_DASH = $C0 ; - uses $C0-$CF

.export title_row0
.export title_row1
.export title_row2
.export title_row3

.segment "RODATA" ; Prepare data separated from the logic in this segment
build_version: .asciiz "Build: xxxxxx" ; null-terminated string
test_text: .asciiz "HELLO NES"

; Old format for 8x16 font
title_tiles: .byte N_TILE, E_TILE, S_TILE, DASH_TILE, R_TILE, S_TILE,0

; Mega Man style 32x32 "NES-RS" - 4 rows of tiles
; Each character is 4 tiles wide, "NES-RS" = 6 chars = 24 tiles per row
title_row0:
  .byte BIG_N+0, BIG_N+1, BIG_N+2, BIG_N+3      ; N row 0
  .byte BIG_E+0, BIG_E+1, BIG_E+2, BIG_E+3      ; E row 0
  .byte BIG_S+0, BIG_S+1, BIG_S+2, BIG_S+3      ; S row 0
  .byte BIG_DASH+0, BIG_DASH+1, BIG_DASH+2, BIG_DASH+3  ; - row 0
  .byte BIG_R+0, BIG_R+1, BIG_R+2, BIG_R+3      ; R row 0
  .byte BIG_S+0, BIG_S+1, BIG_S+2, BIG_S+3      ; S row 0
  .byte 0

title_row1:
  .byte BIG_N+4, BIG_N+5, BIG_N+6, BIG_N+7      ; N row 1
  .byte BIG_E+4, BIG_E+5, BIG_E+6, BIG_E+7      ; E row 1
  .byte BIG_S+4, BIG_S+5, BIG_S+6, BIG_S+7      ; S row 1
  .byte BIG_DASH+4, BIG_DASH+5, BIG_DASH+6, BIG_DASH+7  ; - row 1
  .byte BIG_R+4, BIG_R+5, BIG_R+6, BIG_R+7      ; R row 1
  .byte BIG_S+4, BIG_S+5, BIG_S+6, BIG_S+7      ; S row 1
  .byte 0

title_row2:
  .byte BIG_N+8, BIG_N+9, BIG_N+10, BIG_N+11    ; N row 2
  .byte BIG_E+8, BIG_E+9, BIG_E+10, BIG_E+11    ; E row 2
  .byte BIG_S+8, BIG_S+9, BIG_S+10, BIG_S+11    ; S row 2
  .byte BIG_DASH+8, BIG_DASH+9, BIG_DASH+10, BIG_DASH+11  ; - row 2
  .byte BIG_R+8, BIG_R+9, BIG_R+10, BIG_R+11    ; R row 2
  .byte BIG_S+8, BIG_S+9, BIG_S+10, BIG_S+11    ; S row 2
  .byte 0

title_row3:
  .byte BIG_N+12, BIG_N+13, BIG_N+14, BIG_N+15  ; N row 3
  .byte BIG_E+12, BIG_E+13, BIG_E+14, BIG_E+15  ; E row 3
  .byte BIG_S+12, BIG_S+13, BIG_S+14, BIG_S+15  ; S row 3
  .byte BIG_DASH+12, BIG_DASH+13, BIG_DASH+14, BIG_DASH+15  ; - row 3
  .byte BIG_R+12, BIG_R+13, BIG_R+14, BIG_R+15  ; R row 3
  .byte BIG_S+12, BIG_S+13, BIG_S+14, BIG_S+15  ; S row 3
  .byte 0

.segment "ZEROPAGE"
tmp_1:  .res 1
tmp_2:  .res 1
ptr_1:   .res 2
ptr_2:   .res 2
PPUCTRL_SHADOW: .res 1
PPUMASK_SHADOW: .res 1
