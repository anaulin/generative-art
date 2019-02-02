from PIL import Image

def overlay(filename, overlay_filename, save_filename):
  bg = Image.open(filename).convert("RGBA")
  overlay = Image.open(overlay_filename).convert("RGBA")
  #bg.paste(overlay, (0, 0), overlay)
  #bg.show()
  Image.alpha_composite(bg, overlay).save(save_filename)

if __name__ == "__main__":
  overlay('/Users/anaulin/src/github.com/anaulin/generative-art/nested-squares/output-all-palettes-submission.png','/Users/anaulin/Desktop/1200x1200_duffel-bag.png', '/Users/anaulin/Desktop/duffel-nested-squares-all-colors.png')
