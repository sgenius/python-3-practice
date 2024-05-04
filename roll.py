from PIL import Image

def roll(input_image_path, delta):
    """Roll an image sideways."""
    image = Image.open(input_image_path)
    xsize, ysize = image.size

    delta = delta % xsize
    if delta == 0:
        return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    image.paste(part1, (xsize - delta, 0, xsize, ysize))
    image.paste(part2, (0, 0, xsize - delta, ysize))

    image.show()

if __name__ == '__main__':
    roll(input_image_path='test_image.jpg', delta=100)