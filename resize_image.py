from PIL import Image

def resize_image(input_image_path,
                 output_image_path,
                 target_width=None,
                 target_height=None):
    """Resizes an image using proper scaling.
       Taken from:
       http://www.blog.pythonlibrary.org/2017/10/12/how-to-resize-a-photo-with-python/
    """
    original_image = Image.open(input_image_path)    
    original_width, original_height = original_image.size
    print('The original image size is {wide} wide x {height} '
          'high'.format(wide=original_width, height=original_height))

    if target_width and target_height:
        max_size = (target_width, target_height)
    elif target_width:
        max_size = (target_width, original_height)
    elif target_height:
        max_size = (original_width, target_height)
    else:
        raise RuntimeError('Target width or target height required!')

    original_image.thumbnail(max_size, Image.ANTIALIAS)
    original_image.save(output_image_path)

    scaled_image = Image.open(output_image_path)
    width, height = scaled_image.size
    print('The scaled image size is {wide} wide x {height} '
          'high'.format(wide=width, height=height))
    # scaled_image.show()

if __name__ == '__main__':
    resize_image(input_image_path='test_image.jpg',
                 output_image_path='test_image_small.jpg',
                 target_width=200)