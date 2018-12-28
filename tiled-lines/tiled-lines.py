import cairo
import random

IMG_HEIGHT = 2160
IMG_WIDTH = 3840

LINE_WIDTH = 5


def draw_line(ctx, x, y, width, height):
    leftToRight = random.random() >= 0.5

    if leftToRight:
        ctx.move_to(x, y)
        ctx.line_to(x + width, y + height)
    else:
        ctx.move_to(x + width, y)
        ctx.line_to(x, y + height)

    ctx.set_line_width(LINE_WIDTH)
    ctx.set_line_cap(cairo.LineCap.ROUND)
    ctx.set_source_rgb(0, 0, 0)
    ctx.stroke()


def main(filename="output.png", step=50):
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
    ctx = cairo.Context(ims)

    # Make background white
    ctx.set_source_rgb(256, 256, 256)
    ctx.rectangle(0, 0, IMG_WIDTH, IMG_HEIGHT)
    ctx.fill()

    for x in range(0, IMG_WIDTH, step):
        for y in range(0, IMG_HEIGHT, step):
            draw_line(ctx, x, y, step, step)

    ims.write_to_png(filename)


if __name__ == "__main__":
    for i in [1, 2, 3]:
        main(filename="output-{}.png".format(i), step=i*30)
