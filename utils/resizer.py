from PIL import Image, ImageDraw
import os

def save_and_resize(image_file, upload_folder, filename):
    path = os.path.join(upload_folder, filename)

    img = Image.open(image_file).convert("RGBA")

    img = img.resize((200, 200))

    # create circular mask same size as image
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)

    img.putalpha(mask)

    img.save(path, format="PNG")  # IMPORTANT

    return path