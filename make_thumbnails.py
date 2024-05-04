from resize_image import resize_image
from get_source_images import get_source_images

def make_thumbnails(input_path='./originals',
                    output_path='./thumbs'):
    image_list = get_source_images(input_path)
    for image in image_list:
        full_input_path = input_path + '/' + image
        full_output_path = output_path + '/thumb_' + image
        resize_image(full_input_path, full_output_path, 200)

if __name__ == "__main__":
    make_thumbnails()