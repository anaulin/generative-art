from math import pi

import cairo
import os
import sys
import random

sys.path.append(os.path.abspath('..'))
from lib import colors, palettes


def draw_robot(ctx, x, y, x2, y2, palette):
    margin = int(min(x2 - x, y2 -y) / 20)
    antenna_height = draw_antennas(ctx, x, y, x2, y2, margin, palette)
    face_top = y + margin + antenna_height
    face_bottom = y2 - margin

    # Face.
    face_hex = random.choice(palette['colors'])
    non_face_palette = [c for c in palette['colors'] if c != face_hex]
    face_color = palettes.hex_to_tuple(face_hex)
    face_radius = random.randint(margin, 5 * margin)
    draw_rounded_rect(ctx, x + margin, x2 - margin, face_top, face_bottom,
                      face_radius, face_color)

    # Eyes. Ensure color different from face.
    eye_color = palettes.hex_to_tuple(random.choice(non_face_palette))
    draw_eyes(ctx, x, x2, face_top, face_bottom, margin, eye_color)

    # Mouth
    mouth_color = palettes.hex_to_tuple(random.choice(non_face_palette))
    draw_mouth(ctx, x, x2, face_top, face_bottom, margin, mouth_color)

    draw_screws(ctx, x, x2, face_top, face_bottom, margin)

    draw_ears(ctx, x, x2, face_top, face_bottom, face_color, margin)


def draw_ears(ctx, x, x2, face_top, face_bottom, face_color, margin):
    # This matches the eye_x
    ear_top = face_top + (face_bottom - face_top) / 3
    ear_width = margin // 2
    ear_height = (face_bottom - ear_top - margin) / random.randint(2, 5)
    if random.randint(1, 10) <= 5:
        draw_rounded_rect(ctx,
            x + margin - ear_width,
            x + margin + 2, # a bit of fuzz to make sure it connects, in case of very rounded faces
            ear_top,
            ear_top + ear_height,
            1, face_color)
        draw_rounded_rect(ctx,
            x2 - margin - 2,
            x2 - margin + ear_width,
            ear_top,
            ear_top + ear_height,
            1, face_color)


def draw_screws(ctx, x, x2, face_top, face_bottom, margin):
    screw_count = random.randint(0, 5)
    screw_x = random.choice([x + 3 * margin, x2 - 3 * margin])
    screw_radius = margin // 3
    for i in range(screw_count):
        screw_y = (face_bottom - face_top) // 3 + face_top + i * screw_radius * 3
        draw_screw(ctx, screw_x, screw_y, screw_radius, margin)


def draw_screw(ctx, x, y, radius, margin):
    line_width = margin // 12
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(pi / 4)

    # Grey circle
    ctx.arc(0, 0, radius, 0, 2 *pi)
    ctx.set_source_rgb(*palettes.hex_to_tuple('#acb4bf'))
    ctx.fill()

    # Outline
    ctx.arc(0, 0, radius, 0, 2 *pi)
    ctx.set_source_rgb(0, 0, 0)
    ctx.set_line_width(line_width)
    ctx.stroke()

    # Cross-threads
    space_from_edge = 2 + line_width
    draw_line(ctx, 0, -radius + space_from_edge, 0, radius - space_from_edge, line_width, (0, 0, 0))
    draw_line(ctx, -radius + space_from_edge, 0, radius -space_from_edge, 0, line_width, (0, 0, 0))

    ctx.restore()

def draw_mouth(ctx, x, x2, face_top, face_bottom, margin, color):
    mouth_y = face_top + 2 * (face_bottom - face_top) / 3 + margin
    mouth_margin = random.randint(int((x2 - x - 2 * margin) / 4), int((x2 - x - 2 * margin) / 3))
    mouth_x_left = x + margin + mouth_margin
    mouth_x_right = x2 - margin - mouth_margin
    mouth_line_width = random.randint(margin // 2, margin)

    if random.randint(1, 10) <= 5:
        draw_line(
            ctx,
            mouth_x_left, mouth_y,
            mouth_x_right, mouth_y,
            mouth_line_width,
            color
        )
        smile = random.choice([True, False])
        if smile:
            corner_left = (mouth_x_left - mouth_line_width, mouth_y - mouth_line_width)
            corner_right = (mouth_x_right + mouth_line_width, mouth_y - mouth_line_width)
        else:
            corner_left =  (mouth_x_left, mouth_y - mouth_line_width)
            corner_right = (mouth_x_right, mouth_y - mouth_line_width)
        draw_line(
            ctx,
            mouth_x_left, mouth_y,
            *corner_left,
            mouth_line_width, color
        )
        draw_line(
            ctx,
            mouth_x_right, mouth_y,
            *corner_right,
            mouth_line_width, color
        )
    else:
        fine_line_width = mouth_line_width // 9
        draw_rounded_rect(
            ctx, mouth_x_left, mouth_x_right, mouth_y - mouth_line_width, mouth_y + mouth_line_width, 10, color,
            outline = True, outline_width=fine_line_width
        )
        tooth_interval = (mouth_x_right - mouth_x_left) // 5
        for x in range(int(mouth_x_left + tooth_interval), int(mouth_x_right - tooth_interval + 2), int(tooth_interval)):
            draw_line(
                ctx,
                x, mouth_y - mouth_line_width,
                x, mouth_y + mouth_line_width,
                fine_line_width,
                (0, 0, 0))
        draw_line(ctx, mouth_x_left, mouth_y, mouth_x_right, mouth_y, fine_line_width, (0, 0, 0))

def draw_line(ctx, x1, y1, x2, y2, line_width, color):
    ctx.move_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.set_line_width(line_width)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(*color)
    ctx.stroke()


def draw_eyes(ctx, x, x2, face_top, face_bottom, margin, color):
    eye_y = face_top + (face_bottom - face_top) / 3
    eye_x1 = (x2 - x - 2 * margin) / 3 + x + margin
    eye_x2 = 2 * (x2 - x - 2 * margin) / 3 + x + margin
    eye_radius_base = random.randint(margin, margin * 2)
    if random.randint(1, 10) <= 5:
        draw_line(ctx, eye_x1, eye_y, eye_x2, eye_y, eye_radius_base / 3, color)
    pupil_radius_factor = random.randint(2, 5)
    make_pupil = random.randint(1, 10) >= 5
    make_double_pupil = random.randint(1, 10) >= 5
    for x in [eye_x1, eye_x2]:
        modified_eye_radius = random.randint(int(0.8 * eye_radius_base), int(1.5 * eye_radius_base))
        ctx.arc(x, eye_y, modified_eye_radius, 0, 2 * pi)
        ctx.set_source_rgb(*color)
        ctx.fill()
        if make_pupil:
            ctx.arc(x, eye_y, modified_eye_radius * (1 - 1 / pupil_radius_factor), 0, 2 * pi)
            ctx.set_source_rgb(0, 0, 0)
            ctx.fill()
        if make_double_pupil:
            ctx.arc(x, eye_y, (modified_eye_radius * (1 - 1 / pupil_radius_factor)) / 2, 0, 2 * pi)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill()


def draw_antennas(ctx, x, y, x2, y2, margin, palette):
    antenna_color = palettes.hex_to_tuple(random.choice(palette['colors']))
    antenna_height = random.randint(
        (y2 - y - 2 * margin) // 5, (y2 - y - 2 * margin) // 2)
    antenna_count = random.randint(1, 3)
    antenna_bottom = y + margin + antenna_height
    antenna_interval = (x2 - x - 2 * margin) / (antenna_count + 1)
    antenna_width = random.randint(margin // 2, margin)
    for i in range(antenna_count):
        antenna_x = x + margin + antenna_interval * (i + 1)
        ctx.move_to(antenna_x, antenna_bottom)
        ctx.line_to(antenna_x, antenna_bottom - antenna_height + margin)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_width(antenna_width)
        ctx.set_source_rgb(*antenna_color)
        ctx.stroke()
        if random.randint(1, 10) <= 7:
            ctx.arc(
                antenna_x,
                antenna_bottom - antenna_height + margin,
                random.randint(int(antenna_width * 1.5), antenna_width * 2),
                0, 2*pi
            )
            ctx.set_source_rgb(*antenna_color)
            ctx.fill()
    return antenna_height

def draw_rounded_rect(ctx, left, right, top, bottom, radius, color, outline=False, outline_width=1):
    """ draws rectangles with rounded (circular arc) corners """
    ctx.arc(left + radius, top + radius, radius, 2*(pi/2), 3*(pi/2))
    ctx.arc(right - radius, top + radius, radius, 3*(pi/2), 4*(pi/2))
    ctx.arc(right - radius, bottom - radius, radius, 0*(pi/2), 1*(pi/2))
    ctx.arc(left + radius, bottom - radius, radius, 1*(pi/2), 2*(pi/2))
    ctx.close_path()
    ctx.set_source_rgb(*color)
    ctx.fill()

    if outline:
        ctx.arc(left + radius, top + radius, radius, 2*(pi/2), 3*(pi/2))
        ctx.arc(right - radius, top + radius, radius, 3*(pi/2), 4*(pi/2))
        ctx.arc(right - radius, bottom - radius, radius, 0*(pi/2), 1*(pi/2))
        ctx.arc(left + radius, bottom - radius, radius, 1*(pi/2), 2*(pi/2))
        ctx.close_path()
        ctx.set_line_width(outline_width)
        ctx.set_source_rgb(0, 0, 0)
        ctx.stroke()




def main(filename="output.png", img_width=2000, img_height=2000, count=5, palette=random.choice(palettes.PALETTES)):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, img_width, img_height)
    ctx = cairo.Context(ims)

    # Make background solid color
    ctx.rectangle(0, 0, img_width, img_height)
    ctx.set_source_rgb(*palettes.hex_to_tuple(palette['background']))
    ctx.fill()

    x_size = img_width // count
    y_size = img_width // count
    for x in range(count):
        for y in range(count):
            draw_robot(ctx, x * x_size, y * y_size, (x+1)
                       * x_size, (y+1) * y_size, palette)

    ims.write_to_png(filename)


def make_random(filename="output.png", p=random.choice(palettes.PALETTES), img_width=2000, img_height=2000):
    c = random.randint(3, 10)
    print(filename, os.path.basename(__file__), c, p)
    main(filename=filename, count=c, palette=p,
         img_height=img_height, img_width=img_width)


if __name__ == "__main__":
    for idx in range(5):
        make_random(filename="output-{}.png".format(idx),
                    p=random.choice(palettes.PALETTES))
