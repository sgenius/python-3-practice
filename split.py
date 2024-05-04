from PIL import Image, ImageFilter, ImageChops

def findContourLines(input_image_path):
    image = Image.open(input_image_path)
    source = image.split()
    R, G, B = 0, 1, 2

    # select regions where blue is > 100
    lightYellowMaskR = source[R].point(lambda i: (i > 210 and i < 255) and 255)
    lightYellowMaskG = source[G].point(lambda i: (i > 210 and i < 280) and 255)
    lightYellowMaskB = source[B].point(lambda i: (i > 130 and i < 190) and 255)

    # out2 = source[R].point(lambda i: int(i * 0.4))

    lightYellowMask = ImageChops.darker(lightYellowMaskR, lightYellowMaskG)
    lightYellowMask = ImageChops.darker(lightYellowMaskB, lightYellowMask)
    lightYellowInvertedMask = ImageChops.invert(lightYellowMask).filter(ImageFilter.MinFilter)

    darkYellowMaskR = source[R].point(lambda i: (i > 205 and i < 235) and 255)
    darkYellowMaskG = source[G].point(lambda i: (i > 145 and i < 175) and 255)
    darkYellowMaskB = source[B].point(lambda i: (i > 65 and i < 95) and 255)

    darkYellowMask = ImageChops.darker(darkYellowMaskR, darkYellowMaskG)
    darkYellowMask = ImageChops.darker(darkYellowMaskB, darkYellowMask)
    darkYellowInvertedMask = ImageChops.invert(darkYellowMask).filter(ImageFilter.MinFilter)

    invertedYellowMask = ImageChops.darker(darkYellowInvertedMask, lightYellowInvertedMask)
    # invertedYellowMask = ImageChops.invert(yellowMask)

    image.show()
    # lightYellowInvertedMask.show()
    # darkYellowInvertedMask.show()
    invertedYellowMask.show()

def doPoint(input_image_path):
    image = Image.open(input_image_path)
    image2 = image.point(lambda i: int(i * 1.2))
    image2.show()

if __name__ == '__main__':
    findContourLines(input_image_path='originals/9,-7.jpg')
