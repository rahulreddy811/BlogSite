from PIL import Image,ImageDraw
import os

def save_and_resize(image_file,UPLOAD_FOLDER,filename):
    path = os.path.join(UPLOAD_FOLDER,filename)
    img = Image.open(image_file)
    img.thumbnail((200,200))
    mask = Image.new('L', (200, 200), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 200, 200), fill=255)

    # Apply mask
    img.putalpha(mask)

    img.save(path)
    return path