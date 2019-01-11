import random

# A palette is a dict with a 'background' and a list of 'colors'.

# A list of all the palettes in this file.
PALETTES = []

# A list of the palettes that contain Direct-to-garment recommended brights
DTG_PALETTES = []

# Palette #1
BEIGE = '#EDEDCF'
YELLOW = '#EEC525'
LIGHT_PINK = '#C05F73'
RASPBERRY = '#9D2045'
PURPLE = '#511253'
PLUM = '#3A1B3D'
PALETTE_1 = {
    'background': BEIGE,
    'colors': [LIGHT_PINK, RASPBERRY, PURPLE, PLUM, YELLOW]
}
PALETTES.append(PALETTE_1)

# Palette #2
BEIGE = '#EDEDCF'
DARK_BLUE = '#102F45'
AQUA = '#27A8A8'
GREY_BLUE = '#78A6A8'
PALETTE_2 = {
    'background': BEIGE,
    'colors': [DARK_BLUE, AQUA, GREY_BLUE]
}
PALETTES.append(PALETTE_2)

# Palette #3
WHITE = '#F6F3F2'
TAN = '#8B7266'
GREY_PURPLE = '#9B8791'
MAROON = '#7B4955'
DARK_PURPLE = '#35303D'
PALETTE_3 = {
    'background': DARK_PURPLE,
    'colors': [WHITE, TAN, GREY_PURPLE, MAROON]
}
PALETTES.append(PALETTE_3)

PALETTE_4 = {
    'background': '#090909',
    'colors': ['#4B5043', '#9BC4BC', '#D3FFE9', '#8DDBE0']
}
PALETTES.append(PALETTE_4)

PALETTE_5 = {
    'background': '#6E44FF',
    'colors': ['#B892FF', '#FFC2E2', '#FF90B3', '#EF7A85']
}
PALETTES.append(PALETTE_5)

PALETTE_6 = {
    'background': PALETTE_5['background'],
    'colors': PALETTE_1['colors'] + PALETTE_5['colors']
}
PALETTES.append(PALETTE_6)

# DTG recommended colors
RASPBERRY_RED = '#E60A96'  # (230, 10, 150)
TRUE_RED = '#D21446'  # (210, 20, 70)
PASTEL_PINK = '#FFAFBE'  # (255, 175, 190)
LIGHT_BLUE = '#0AA5E1'  # (10, 165, 225)
VIOLET_PURPLE = '#9B4BA0'  # (155, 75, 160)
BRIGHT_GREEN = '#19FF46'  # (25, 255, 70)
BRIGHT_YELLOW = '#FFF000'  # (255, 240, 0)
BRIGHT_ORANGE = '#F58228'  # (245, 130, 40)
TRUE_BLACK = '#050000'  # (CMYK 55, 55, 55, 100)

DTG_PALETTE_REDS = {
    'background': TRUE_BLACK,
    'colors': [TRUE_RED, '#FFAC81', '#5C0029', '#912F56', PASTEL_PINK]
}
PALETTES.append(DTG_PALETTE_REDS)
DTG_PALETTES.append(DTG_PALETTE_REDS)

DTG_PALETTE_BLUES = {
    'background': TRUE_BLACK,
    'colors': [LIGHT_BLUE, '#55DDE0', '#587291', '#083D77', '#0B3954']
}
PALETTES.append(DTG_PALETTE_BLUES)
DTG_PALETTES.append(DTG_PALETTE_BLUES)


def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def random_color(palette):
    hex = random.choice(palette['colors'])
    return hex_to_tuple(hex)


def random_colors(palette, n):
    hex = random.choices(palette['colors'], k=n)
    return [hex_to_tuple(h) for h in hex]
