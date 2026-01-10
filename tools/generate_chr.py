#!/usr/bin/env python3
"""
NES CHR Pattern File Generator
Generates an 8KB CHR file (512 tiles, 16 bytes each)
"""

import struct

def create_tile(pixels):
    """
    Create a 16-byte NES tile from an 8x8 pixel array.
    Each pixel is 0-3 (2-bit color index).
    Returns 16 bytes: 8 low-plane bytes, then 8 high-plane bytes.
    """
    low_plane = []
    high_plane = []

    for row in pixels:
        low_byte = 0
        high_byte = 0
        for i, pixel in enumerate(row):
            bit = 7 - i
            if pixel & 1:
                low_byte |= (1 << bit)
            if pixel & 2:
                high_byte |= (1 << bit)
        low_plane.append(low_byte)
        high_plane.append(high_byte)

    return bytes(low_plane + high_plane)

def empty_tile():
    """Tile 0: Empty (all transparent)"""
    return create_tile([[0]*8 for _ in range(8)])

def solid_tile(color=1):
    """Solid filled tile"""
    return create_tile([[color]*8 for _ in range(8)])

def checkerboard_tile():
    """Checkerboard pattern"""
    pixels = []
    for y in range(8):
        row = []
        for x in range(8):
            row.append(1 if (x + y) % 2 == 0 else 0)
        pixels.append(row)
    return create_tile(pixels)

def gradient_h_tile():
    """Horizontal gradient"""
    pixels = []
    for y in range(8):
        row = [0, 0, 1, 1, 2, 2, 3, 3]
        pixels.append(row)
    return create_tile(pixels)

def gradient_v_tile():
    """Vertical gradient"""
    pixels = []
    for y in range(8):
        color = y // 2
        pixels.append([color] * 8)
    return create_tile(pixels)

def border_tile():
    """Border/frame tile"""
    pixels = [[1]*8 for _ in range(8)]
    for y in range(1, 7):
        for x in range(1, 7):
            pixels[y][x] = 0
    return create_tile(pixels)

def corner_tl():
    """Top-left corner"""
    pixels = [[1]*8 for _ in range(8)]
    for y in range(1, 8):
        for x in range(1, 8):
            pixels[y][x] = 0
    return create_tile(pixels)

def corner_tr():
    """Top-right corner"""
    pixels = [[1]*8 for _ in range(8)]
    for y in range(1, 8):
        for x in range(0, 7):
            pixels[y][x] = 0
    return create_tile(pixels)

def corner_bl():
    """Bottom-left corner"""
    pixels = [[1]*8 for _ in range(8)]
    for y in range(0, 7):
        for x in range(1, 8):
            pixels[y][x] = 0
    return create_tile(pixels)

def corner_br():
    """Bottom-right corner"""
    pixels = [[1]*8 for _ in range(8)]
    for y in range(0, 7):
        for x in range(0, 7):
            pixels[y][x] = 0
    return create_tile(pixels)

def edge_top():
    """Top edge"""
    pixels = [[0]*8 for _ in range(8)]
    pixels[0] = [1]*8
    return create_tile(pixels)

def edge_bottom():
    """Bottom edge"""
    pixels = [[0]*8 for _ in range(8)]
    pixels[7] = [1]*8
    return create_tile(pixels)

def edge_left():
    """Left edge"""
    pixels = [[0]*8 for _ in range(8)]
    for y in range(8):
        pixels[y][0] = 1
    return create_tile(pixels)

def edge_right():
    """Right edge"""
    pixels = [[0]*8 for _ in range(8)]
    for y in range(8):
        pixels[y][7] = 1
    return create_tile(pixels)

# Simple 8x8 font bitmaps (1-bit, will be converted to color 3)
FONT = {
    '0': [
        "  ####  ",
        " #    # ",
        " #   ## ",
        " #  # # ",
        " # #  # ",
        " ##   # ",
        " #    # ",
        "  ####  ",
    ],
    '1': [
        "    #   ",
        "   ##   ",
        "  # #   ",
        "    #   ",
        "    #   ",
        "    #   ",
        "    #   ",
        "  ##### ",
    ],
    '2': [
        "  ####  ",
        " #    # ",
        "      # ",
        "     #  ",
        "   ##   ",
        "  #     ",
        " #      ",
        " ###### ",
    ],
    '3': [
        "  ####  ",
        " #    # ",
        "      # ",
        "   ###  ",
        "      # ",
        "      # ",
        " #    # ",
        "  ####  ",
    ],
    '4': [
        "     #  ",
        "    ##  ",
        "   # #  ",
        "  #  #  ",
        " #   #  ",
        " ###### ",
        "     #  ",
        "     #  ",
    ],
    '5': [
        " ###### ",
        " #      ",
        " #      ",
        " #####  ",
        "      # ",
        "      # ",
        " #    # ",
        "  ####  ",
    ],
    '6': [
        "   ###  ",
        "  #     ",
        " #      ",
        " #####  ",
        " #    # ",
        " #    # ",
        " #    # ",
        "  ####  ",
    ],
    '7': [
        " ###### ",
        "      # ",
        "     #  ",
        "    #   ",
        "   #    ",
        "   #    ",
        "   #    ",
        "   #    ",
    ],
    '8': [
        "  ####  ",
        " #    # ",
        " #    # ",
        "  ####  ",
        " #    # ",
        " #    # ",
        " #    # ",
        "  ####  ",
    ],
    '9': [
        "  ####  ",
        " #    # ",
        " #    # ",
        " #    # ",
        "  ##### ",
        "      # ",
        "     #  ",
        "  ###   ",
    ],
    'A': [
        "   ##   ",
        "  #  #  ",
        " #    # ",
        " #    # ",
        " ###### ",
        " #    # ",
        " #    # ",
        " #    # ",
    ],
    'B': [
        " #####  ",
        " #    # ",
        " #    # ",
        " #####  ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #####  ",
    ],
    'C': [
        "  ####  ",
        " #    # ",
        " #      ",
        " #      ",
        " #      ",
        " #      ",
        " #    # ",
        "  ####  ",
    ],
    'D': [
        " ####   ",
        " #   #  ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #   #  ",
        " ####   ",
    ],
    'E': [
        " ###### ",
        " #      ",
        " #      ",
        " #####  ",
        " #      ",
        " #      ",
        " #      ",
        " ###### ",
    ],
    'F': [
        " ###### ",
        " #      ",
        " #      ",
        " #####  ",
        " #      ",
        " #      ",
        " #      ",
        " #      ",
    ],
    'G': [
        "  ####  ",
        " #    # ",
        " #      ",
        " #      ",
        " #  ### ",
        " #    # ",
        " #    # ",
        "  ####  ",
    ],
    'H': [
        " #    # ",
        " #    # ",
        " #    # ",
        " ###### ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
    ],
    'I': [
        "  ####  ",
        "    #   ",
        "    #   ",
        "    #   ",
        "    #   ",
        "    #   ",
        "    #   ",
        "  ####  ",
    ],
    'J': [
        "   #### ",
        "      # ",
        "      # ",
        "      # ",
        "      # ",
        " #    # ",
        " #    # ",
        "  ####  ",
    ],
    'K': [
        " #    # ",
        " #   #  ",
        " #  #   ",
        " ###    ",
        " #  #   ",
        " #   #  ",
        " #    # ",
        " #    # ",
    ],
    'L': [
        " #      ",
        " #      ",
        " #      ",
        " #      ",
        " #      ",
        " #      ",
        " #      ",
        " ###### ",
    ],
    'M': [
        " #    # ",
        " ##  ## ",
        " # ## # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
    ],
    'N': [
        " #    # ",
        " ##   # ",
        " # #  # ",
        " #  # # ",
        " #   ## ",
        " #    # ",
        " #    # ",
        " #    # ",
    ],
    'O': [
        "  ####  ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        "  ####  ",
    ],
    'P': [
        " #####  ",
        " #    # ",
        " #    # ",
        " #####  ",
        " #      ",
        " #      ",
        " #      ",
        " #      ",
    ],
    'Q': [
        "  ####  ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #  # # ",
        " #   #  ",
        "  ### # ",
    ],
    'R': [
        " #####  ",
        " #    # ",
        " #    # ",
        " #####  ",
        " #  #   ",
        " #   #  ",
        " #    # ",
        " #    # ",
    ],
    'S': [
        "  ####  ",
        " #    # ",
        " #      ",
        "  ####  ",
        "      # ",
        "      # ",
        " #    # ",
        "  ####  ",
    ],
    'T': [
        " ###### ",
        "    #   ",
        "    #   ",
        "    #   ",
        "    #   ",
        "    #   ",
        "    #   ",
        "    #   ",
    ],
    'U': [
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        "  ####  ",
    ],
    'V': [
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        "  #  #  ",
        "   ##   ",
        "   ##   ",
    ],
    'W': [
        " #    # ",
        " #    # ",
        " #    # ",
        " #    # ",
        " # ## # ",
        " # ## # ",
        " ##  ## ",
        " #    # ",
    ],
    'X': [
        " #    # ",
        " #    # ",
        "  #  #  ",
        "   ##   ",
        "   ##   ",
        "  #  #  ",
        " #    # ",
        " #    # ",
    ],
    'Y': [
        " #    # ",
        " #    # ",
        "  #  #  ",
        "   ##   ",
        "    #   ",
        "    #   ",
        "    #   ",
        "    #   ",
    ],
    'Z': [
        " ###### ",
        "      # ",
        "     #  ",
        "    #   ",
        "   #    ",
        "  #     ",
        " #      ",
        " ###### ",
    ],
    ' ': [
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
    ],
    ':': [
        "        ",
        "   ##   ",
        "   ##   ",
        "        ",
        "        ",
        "   ##   ",
        "   ##   ",
        "        ",
    ],
    '-': [
        "        ",
        "        ",
        "        ",
        " ###### ",
        "        ",
        "        ",
        "        ",
        "        ",
    ],
    '.': [
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "   ##   ",
        "   ##   ",
        "        ",
    ],
}

# Add lowercase letters (same as uppercase)
for upper in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    lower = upper.lower()
    if upper in FONT:
        FONT[lower] = FONT[upper]

def char_to_tile(char, fg_color=1):
    """Convert a character bitmap to a tile"""
    if char not in FONT:
        return empty_tile()

    bitmap = FONT[char]
    pixels = []
    for row in bitmap:
        pixel_row = []
        for c in row:
            pixel_row.append(fg_color if c == '#' else 0)
        pixels.append(pixel_row)
    return create_tile(pixels)

# Mega Man style 32x32 BIG font (4x4 tiles per character)
# Each character is defined as a 32x32 pixel grid
MEGAMAN_FONT_BIG = {
    'N': [
        "    ####                    ####",
        "   ######                  #####",
        "   ######                 ######",
        "   #######                ######",
        "   ########               ######",
        "   ########               ######",
        "   ##  #####              ######",
        "   ##   #####             ######",
        "   ##    #####            ######",
        "   ##     #####           ######",
        "   ##      #####          ######",
        "   ##       #####         ######",
        "   ##        #####        ######",
        "   ##         #####       ######",
        "   ##          #####      ######",
        "   ##           #####     ######",
        "   ##            #####    ######",
        "   ##             #####   ######",
        "   ##              #####  ######",
        "   ##               ##### ######",
        "   ##               ############",
        "   ##                ###########",
        "   ##                 ##########",
        "   ##                  #########",
        "   ##                   ########",
        "   ##                    #######",
        "   ##                     ######",
        "   ##                      #####",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
    ],
    'E': [
        "  ############################  ",
        "  ############################  ",
        "  ############################  ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######################        ",
        "  ######################        ",
        "  ######################        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  ############################  ",
        "  ############################  ",
        "  ############################  ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
    ],
    'S': [
        "      ####################      ",
        "    ########################    ",
        "   ##########################   ",
        "  #######              #######  ",
        "  ######                ######  ",
        "  ######                        ",
        "  ######                        ",
        "  ######                        ",
        "  #######                       ",
        "   ########                     ",
        "    ##########                  ",
        "      ###########               ",
        "         ###########            ",
        "            ###########         ",
        "               ##########       ",
        "                  ########      ",
        "                    #######     ",
        "                      ######    ",
        "                       ######   ",
        "                        ######  ",
        "                        ######  ",
        "                        ######  ",
        "  ######                ######  ",
        "  #######              #######  ",
        "   ##########################   ",
        "    ########################    ",
        "      ####################      ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
    ],
    '-': [
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "    ########################    ",
        "    ########################    ",
        "    ########################    ",
        "    ########################    ",
        "    ########################    ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
    ],
    'R': [
        "  #####################         ",
        "  #######################       ",
        "  ########################      ",
        "  ######           #######      ",
        "  ######            ######      ",
        "  ######             ######     ",
        "  ######             ######     ",
        "  ######             ######     ",
        "  ######            ######      ",
        "  ######           #######      ",
        "  ########################      ",
        "  #######################       ",
        "  #####################         ",
        "  ######   ######               ",
        "  ######    ######              ",
        "  ######     ######             ",
        "  ######      ######            ",
        "  ######       ######           ",
        "  ######        ######          ",
        "  ######         ######         ",
        "  ######          ######        ",
        "  ######           ######       ",
        "  ######            ######      ",
        "  ######             ######     ",
        "  ######              ######    ",
        "  ######               ######   ",
        "  ######                ######  ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
        "                                ",
    ],
}

def create_big32_char_tiles(char):
    """
    Create 16 tiles (4x4) for a 32x32 Mega Man-style character.
    Returns tiles in row order: [row0: TL,T,T,TR], [row1: L,C,C,R], etc.
    """
    if char not in MEGAMAN_FONT_BIG:
        return [empty_tile()] * 16

    bitmap = MEGAMAN_FONT_BIG[char]

    # Ensure bitmap is 32x32
    while len(bitmap) < 32:
        bitmap.append("                                ")

    tiles = []

    # Process each 8x8 tile (4 rows x 4 cols = 16 tiles)
    for tile_row in range(4):
        for tile_col in range(4):
            pixels = []
            for y in range(8):
                row = []
                for x in range(8):
                    bx = tile_col * 8 + x
                    by = tile_row * 8 + y
                    char_at = bitmap[by][bx] if bx < len(bitmap[by]) else ' '
                    row.append(1 if char_at == '#' else 0)
                pixels.append(row)
            tiles.append(create_tile(pixels))

    return tiles

# Mega Man style 16x16 big font (2x2 tiles per character) - keeping for reference
MEGAMAN_FONT = {
    'N': [
        "  ##          ##",
        " ####        ###",
        " ####       ####",
        " #####      ####",
        " ## ###     ####",
        " ##  ###    ####",
        " ##   ###   ####",
        " ##    ###  ####",
        " ##     ### ####",
        " ##      ######",
        " ##       #####",
        " ##        ####",
        " ##         ###",
        " ##          ##",
        "                ",
        "                ",
    ],
    'E': [
        " ##############",
        " ##############",
        " ####          ",
        " ####          ",
        " ####          ",
        " ###########   ",
        " ###########   ",
        " ####          ",
        " ####          ",
        " ####          ",
        " ####          ",
        " ##############",
        " ##############",
        "               ",
        "               ",
        "               ",
    ],
    'S': [
        "   ##########  ",
        "  ############ ",
        " ####      ####",
        " ####          ",
        " #####         ",
        "  #######      ",
        "    ########   ",
        "       ######  ",
        "          #### ",
        "          #### ",
        " ####     #### ",
        " ############# ",
        "  ###########  ",
        "               ",
        "               ",
        "               ",
    ],
    '-': [
        "                ",
        "                ",
        "                ",
        "                ",
        "                ",
        "  ############  ",
        "  ############  ",
        "  ############  ",
        "                ",
        "                ",
        "                ",
        "                ",
        "                ",
        "                ",
        "                ",
        "                ",
    ],
    'R': [
        " ###########   ",
        " ############  ",
        " ####     #### ",
        " ####      ####",
        " ####     #### ",
        " ############  ",
        " ###########   ",
        " #### ####     ",
        " ####  ####    ",
        " ####   ####   ",
        " ####    ####  ",
        " ####     #### ",
        " ####      ####",
        "               ",
        "               ",
        "               ",
    ],
}

def create_big_char_tiles(char):
    """
    Create 4 tiles (2x2) for a 16x16 Mega Man-style character.
    Returns tiles in order: top-left, top-right, bottom-left, bottom-right
    """
    if char not in MEGAMAN_FONT:
        return [empty_tile()] * 4

    bitmap = MEGAMAN_FONT[char]

    # Ensure bitmap is 16x16
    while len(bitmap) < 16:
        bitmap.append("                ")

    tiles = []

    # Process each quadrant
    for quad_y in range(2):  # top, bottom
        for quad_x in range(2):  # left, right
            pixels = []
            for y in range(8):
                row = []
                for x in range(8):
                    bx = quad_x * 8 + x
                    by = quad_y * 8 + y
                    char_at = bitmap[by][bx] if bx < len(bitmap[by]) else ' '
                    row.append(1 if char_at == '#' else 0)
                pixels.append(row)
            tiles.append(create_tile(pixels))

    return tiles

def smiley_tile():
    """Simple smiley face"""
    pixels = [
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 3, 0, 0, 0, 0, 3, 0],
        [3, 0, 3, 0, 0, 3, 0, 3],
        [3, 0, 0, 0, 0, 0, 0, 3],
        [3, 0, 3, 0, 0, 3, 0, 3],
        [3, 0, 0, 3, 3, 0, 0, 3],
        [0, 3, 0, 0, 0, 0, 3, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
    ]
    return create_tile(pixels)

def heart_tile():
    """Heart shape"""
    pixels = [
        [0, 3, 3, 0, 0, 3, 3, 0],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [0, 3, 3, 3, 3, 3, 3, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    return create_tile(pixels)

def star_tile():
    """Star shape"""
    pixels = [
        [0, 0, 0, 3, 3, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [0, 3, 3, 3, 3, 3, 3, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 3, 3, 0, 0, 3, 3, 0],
        [3, 3, 0, 0, 0, 0, 3, 3],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    return create_tile(pixels)

def arrow_up():
    """Up arrow"""
    pixels = [
        [0, 0, 0, 3, 3, 0, 0, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 3, 3, 3, 3, 3, 3, 0],
        [3, 3, 0, 3, 3, 0, 3, 3],
        [0, 0, 0, 3, 3, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0],
    ]
    return create_tile(pixels)

def arrow_down():
    """Down arrow"""
    pixels = [
        [0, 0, 0, 3, 3, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0],
        [3, 3, 0, 3, 3, 0, 3, 3],
        [0, 3, 3, 3, 3, 3, 3, 0],
        [0, 0, 3, 3, 3, 3, 0, 0],
        [0, 0, 0, 3, 3, 0, 0, 0],
    ]
    return create_tile(pixels)

def arrow_left():
    """Left arrow"""
    pixels = [
        [0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 3, 3, 0, 0, 0, 0],
        [0, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [0, 3, 3, 3, 3, 3, 3, 3],
        [0, 0, 3, 3, 0, 0, 0, 0],
        [0, 0, 0, 3, 0, 0, 0, 0],
    ]
    return create_tile(pixels)

def arrow_right():
    """Right arrow"""
    pixels = [
        [0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 3, 3, 0, 0],
        [3, 3, 3, 3, 3, 3, 3, 0],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 0],
        [0, 0, 0, 0, 3, 3, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0],
    ]
    return create_tile(pixels)

def generate_chr():
    """Generate the full 8KB CHR file"""
    tiles = []

    # Tile 0x00: Empty
    tiles.append(empty_tile())

    # Tile 0x01: Solid
    tiles.append(solid_tile(3))

    # Tile 0x02: Checkerboard
    tiles.append(checkerboard_tile())

    # Tile 0x03: Horizontal gradient
    tiles.append(gradient_h_tile())

    # Tile 0x04: Vertical gradient
    tiles.append(gradient_v_tile())

    # Tile 0x05: Border box
    tiles.append(border_tile())

    # Tiles 0x06-0x09: Corners (TL, TR, BL, BR)
    tiles.append(corner_tl())
    tiles.append(corner_tr())
    tiles.append(corner_bl())
    tiles.append(corner_br())

    # Tiles 0x0A-0x0D: Edges (Top, Bottom, Left, Right)
    tiles.append(edge_top())
    tiles.append(edge_bottom())
    tiles.append(edge_left())
    tiles.append(edge_right())

    # Tiles 0x0E-0x11: Arrows (Up, Down, Left, Right)
    tiles.append(arrow_up())
    tiles.append(arrow_down())
    tiles.append(arrow_left())
    tiles.append(arrow_right())

    # Tiles 0x12-0x14: Special shapes
    tiles.append(smiley_tile())
    tiles.append(heart_tile())
    tiles.append(star_tile())

    # Pad to tile 0x20 (space character in ASCII)
    while len(tiles) < 0x20:
        tiles.append(empty_tile())

    # Tiles 0x20-0x7E: Full ASCII printable characters
    # 0x20 = space, 0x30-0x39 = 0-9, 0x3A = ':', 0x41-0x5A = A-Z, 0x61-0x7A = a-z
    for code in range(0x20, 0x7F):
        char = chr(code)
        if char in FONT:
            tiles.append(char_to_tile(char))
        else:
            tiles.append(empty_tile())

    # Mega Man style 32x32 BIG font for "NES-RS" starting at tile 0x80
    # Each character uses 16 tiles (4x4 arrangement)
    # Layout per char: row by row, left to right
    big_font_start = 0x80

    # Pad to big font start
    while len(tiles) < big_font_start:
        tiles.append(empty_tile())

    # Add big 32x32 font tiles for NES-RS
    for char in "NESR-":
        char_tiles = create_big32_char_tiles(char)
        tiles.extend(char_tiles)

    # Fill remaining tiles in first pattern table (256 tiles)
    while len(tiles) < 256:
        tiles.append(empty_tile())

    # Second pattern table (sprites) - copy big font for sprites too
    # Starting at tile 0x100 (index 256)
    for i in range(256):
        tiles.append(empty_tile())

    # Write CHR file
    chr_data = b''.join(tiles)
    return chr_data

if __name__ == "__main__":
    import os

    chr_data = generate_chr()

    # Write to res directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "..", "res", "generated_pattern.chr")

    with open(output_path, "wb") as f:
        f.write(chr_data)

    print(f"Generated CHR file: {output_path}")
    print(f"Size: {len(chr_data)} bytes (512 tiles)")
    print("\nTile Layout:")
    print("  0x00: Empty")
    print("  0x01: Solid")
    print("  0x02: Checkerboard")
    print("  0x03: Horizontal gradient")
    print("  0x04: Vertical gradient")
    print("  0x05: Border box")
    print("  0x06-0x09: Corners (TL, TR, BL, BR)")
    print("  0x0A-0x0D: Edges (Top, Bottom, Left, Right)")
    print("  0x0E-0x11: Arrows (Up, Down, Left, Right)")
    print("  0x12: Smiley face")
    print("  0x13: Heart")
    print("  0x14: Star")
    print("  0x20: Space")
    print("  0x30-0x39: Numbers 0-9")
    print("  0x41-0x5A: Letters A-Z")
    print("  0x61-0x7A: Lowercase a-z")
    print("\n  === MEGA MAN STYLE BIG FONT (16x16, 2x2 tiles each) ===")
    print("  Each char uses 4 tiles: [TL, TR, BL, BR]")
    print("  0x80-0x83: N")
    print("  0x84-0x87: E")
    print("  0x88-0x8B: S")
    print("  0x8C-0x8F: R")
    print("  0x90-0x93: - (dash)")
    print("\n  To display 'NES-RS' use these tile indices in a 2-row layout:")
    print("  Row 1: $80 $81  $84 $85  $88 $89  $90 $91  $8C $8D  $88 $89")
    print("  Row 2: $82 $83  $86 $87  $8A $8B  $92 $93  $8E $8F  $8A $8B")
