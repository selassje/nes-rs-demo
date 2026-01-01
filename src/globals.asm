.exportzp tmp_1
.exportzp tmp_2
.exportzp ptr_1
.exportzp PPUCTRL_SHADOW
.exportzp PPUMASK_SHADOW

.export build_version
.export title_tiles

E_TILE = $BC
N_TILE = $CE
R_TILE = $D6
S_TILE = $D8
DASH_TILE = $EE

.segment "RODATA" ; Prepare data separated from the logic in this segment
build_version: .asciiz "Build: xxxxxx" ; null-terminated string
title_tiles: .byte N_TILE, E_TILE, S_TILE, DASH_TILE, R_TILE, S_TILE,0

.segment "ZEROPAGE"
tmp_1:  .res 1
tmp_2:  .res 1
ptr_1:   .res 2
PPUCTRL_SHADOW: .res 1
PPUMASK_SHADOW: .res 1
