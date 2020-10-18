import random
from . import colors

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

PALETTE_7 = {
    'background': '#91C4F2',
    'colors': ['#8CA0D7', '#9D79BC', '#A14DA0', '#7E1F86', '#D81E5B', '#59C9A5']
}
PALETTES.append(PALETTE_7)

PALETTE_8 = {
    'background': '#000000',
    'colors': ['#785589', '#977390', '#E9AFA3', '#AC7B7D'],
}
PALETTES.append(PALETTE_8)

PALETTE_9 = {
    'background': '#000000',
    'colors': [ '#1E352F', '#425244', '#A8A4A7', '#A3A7A4', '#D6AF1C' ]
}
PALETTES.append(PALETTE_9)

PALETTE_10 = {
    'background': '#B6C1C8',
    'colors': [ '#5B7FA2', '#353953', '#86678D', '#B397A4' ]

}
PALETTES.append(PALETTE_10)

PALETTE_11 = {
    'background': '#000000',
    'colors': [ '#382C33', '#69483A', '#877751', '#8E9884', '#C1B89C' ]
}
PALETTES.append(PALETTE_11)

PALETTE_12 = {
    'background': '#080F1A',
    'colors': [ '#071828', '#113E4D', '#A4B49D', '#EAD868', '#1C8D92', '#BFD88F' ]
}
PALETTES.append(PALETTE_12)

UNICORN = {
    'background': '#ffffff',
    'colors': [ '#AA48FB', '#12E8FD', '#80E9D1', '#5400A2', '#FF7BF7', '#F732B5', '#5116A3' ]
}
PALETTES.append(UNICORN)

RAINBOW = {
    'background': '#ffffff',
    'colors': [ '#8300F2', '#158FE8', '#0FC8F3', '#25CD20', '#F1DE2C', '#F57921', '#DD1A1C' ]
}
PALETTES.append(RAINBOW)

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

DTG_PALETTE_REDS_AND_BLUES = {
    'background': TRUE_BLACK,
    'colors': DTG_PALETTE_REDS['colors'] + DTG_PALETTE_BLUES['colors']
}
PALETTES.append(DTG_PALETTE_REDS_AND_BLUES)
DTG_PALETTES.append(DTG_PALETTE_REDS_AND_BLUES)

# Add as many randomly-generated palettes as we have hardcoded ones
for _ in range(len(PALETTES) + 4):
    PALETTES.append(colors.random_palette(n=5))


# Misc helper functions
def hex_to_tuple(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16)/255 for i in (0, 2, 4))


def random_color(palette):
    hex = random.choice(palette['colors'])
    return hex_to_tuple(hex)


def random_colors(palette, n):
    hex = random.choices(palette['colors'], k=n)
    return [hex_to_tuple(h) for h in hex]
