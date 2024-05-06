import os
from PIL import Image

def get_source_filenames(base_x=0,
                         base_y=0,
                         scale_x=2,
                         scale_y=2,
                         layer=1,
                         prefix=''):
    """Get possible filenames for base.
    """
    filename_list = []
    if scale_x <= 0 or scale_y <= 0 or layer < 1:
        return filename_list
    for x in range(base_x, base_x + scale_x - 1):
        for y in range(base_y, base_y + scale_y - 1):
            filename_list.append(f"{prefix}{x},{y}.jpg")
    return filename_list

def get_source_filename(x=0,
                        y=0,
                        prefix=''):
    """Get filename for a base cell.
    """
    return f"{prefix}{x},{y}.jpg"

# def get_verified_source_filenames(path='./originals',
#                                   base_x=0,
#                                   base_y=0,
#                                   scale_x=2,
#                                   scale_y=2,
#                                   layer=1):
#     """Get the existing base files for a cell
#     """
#     file_list = []
#     wanted_filenames = get_source_filenames(base_x, base_y, scale_x, scale_y, layer)
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             if file in wanted_filenames:
#                 file_list.append(file)
#     return file_list

def get_layer_cell_filename(
    base_x=0,
    base_y=0,
    scale_x=2,
    scale_y=2,
    layer=1,
    prefix=''
):
    return f"{prefix}l{layer}x{scale_x}y{scale_y}-{base_x},{base_y}.jpg"

def make_layer_cell(
    input_path='./originals',
    output_path='./layers',
    base_x=0,
    base_y=0,
    scale_x=2,
    scale_y=2,
    layer=1,
    output_width=0,
    output_height=0,
    min_x=0,
    max_x=1,
    min_y=0,
    max_y=1,
    reverse_y=True,
):
    """Creates a single layer cell file
    """
    # ensure we have an width and height for the output image
    if output_width == 0 or output_height == 0:
        # use the width and height of the first file
        sample_file = Image.open(input_path + '/' + get_source_filename(base_x, base_y))
        output_width, output_height = sample_file.size

    # create the blank output image
    result = Image.new('RGB', (output_width, output_height))

    # get width and height to resize sources to
    resized_width = output_width // (scale_x ** layer)
    resized_height = output_height // (scale_y ** layer)

    x_on_canvas = 0
    for x in range(
        max([min_x, base_x]),
        min([max_x + 1, base_x + (scale_x ** layer)])
    ):
        y_on_canvas = (output_height - resized_height) if reverse_y else 0
        for y in range(
            max([min_y, base_y]),
            min([max_y + 1, base_y + (scale_y ** layer)])
        ):
            # get the file
            source_file = Image.open(f"{input_path}/{get_source_filename(x, y)}")

            print(f"source file: {source_file}")

            # resize to right size as per scale
            resized_file = source_file.resize((resized_width, resized_height), Image.BOX)

            # paste on canvas
            result.paste(resized_file, (x_on_canvas, y_on_canvas))

            y_on_canvas = y_on_canvas - resized_height if reverse_y else y_on_canvas + resized_height

        x_on_canvas = x_on_canvas + resized_width

    result.show()

    # write result to disk; for now, assume the output layer exists
    result.save(f"{output_path}/{layer}/{get_layer_cell_filename(base_x, base_y, scale_x, scale_y, layer)}")

if __name__ == '__main__':
    make_layer_cell()