import os
import sys
from PIL import Image

def get_source_filenames(base_x=0,
                         base_y=0,
                         scale_x=2,
                         scale_y=2,
                         layer=1,
                         prefix=''):
    """
        Get possible filenames for base.
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
    """
        Get filename for a base cell.
    """
    return f"{prefix}{x},{y}.jpg"

def get_layer_cell_filename(
    base_x=0,
    base_y=0,
    scale_x=2,
    scale_y=2,
    layer=1,
    prefix=''
):
    return f"{prefix}l{layer}x{scale_x}y{scale_y}__{base_x},{base_y}.jpg"

def get_base_dimensions(
    input_path='./originals',
    filename='.jpg',
):
    """
        Gets the first image file from the directory matching the "filename" suffix
        and returns its dimensions.
    """
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if file.endswith(filename):
                image = Image.open(f"{input_path}/{file}")
                return image.size

def make_layer_cell(
    input_path='./originals',
    output_path='./layers',
    base_x=0,
    base_y=0,
    scale_x=2,
    scale_y=2,
    layer=1,
    min_x=0,
    max_x=1,
    min_y=0,
    max_y=1,
    output_width=0,
    output_height=0,
    reverse_y=True,
):
    """
        Creates a single layer cell file
    """
    # ensure we have an width and height for the output image
    if output_width == 0 or output_height == 0:
        # use the width and height of the first file
        sample_file = Image.open(f"{input_path}/{get_source_filename(base_x, base_y)}")
        output_width, output_height = sample_file.size

    # create the blank output image
    result = Image.new('RGB', (output_width, output_height))

    # get width and height to resize sources to
    resized_width = output_width // (scale_x ** layer)
    resized_height = output_height // (scale_y ** layer)

    for x in range(
        max([min_x, base_x]),
        min([max_x + 1, base_x + (scale_x ** layer)])
    ):
        for y in range(
            max([min_y, base_y]),
            min([max_y + 1, base_y + (scale_y ** layer)])
        ):
            x_on_canvas = (x - base_x) * resized_width
            y_on_canvas = (y - base_y) * resized_height
            if (reverse_y):
                y_on_canvas = output_height - ((y - base_y) + 1) * resized_height

            try:
                # get the file
                source_file = Image.open(f"{input_path}/{get_source_filename(x, y)}")

                # resize to right size as per scale
                # see: https://pillow.readthedocs.io/en/latest/handbook/concepts.html#filters-comparison-table
                resized_file = source_file.resize((resized_width, resized_height), Image.LANCZOS)

                # paste on canvas
                result.paste(resized_file, (x_on_canvas, y_on_canvas))
            except FileNotFoundError:
                print(f"File not found: {input_path}/{get_source_filename(x, y)}")
                continue

    # write result to disk; for now, assume the output layer exists
    layer_cell_filename = get_layer_cell_filename(base_x, base_y, scale_x, scale_y, layer)
    print(f">> Writing: {output_path}/{layer}/{layer_cell_filename}")
    result.save(f"{output_path}/{layer}/{layer_cell_filename}")

def get_edges(
    input_path='./originals'
):
    """
        Gets the minimum and maximum coordinates available in the original tiles
    """
    # https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints
    min_x = sys.maxsize
    min_y = sys.maxsize
    max_x = -sys.maxsize
    max_y = -sys.maxsize

    for root, dirs, files in os.walk(input_path):
        for file in files:
            try:
                coords1 = file.split(',')
                coords2 = coords1[1].split('.')

                coord_x = int(coords1[0])
                coord_y = int(coords2[0])

                min_x = coord_x if coord_x < min_x else min_x
                max_x = coord_x if coord_x > max_x else max_x
                min_y = coord_y if coord_y < min_y else min_y
                max_y = coord_y if coord_y > max_y else max_y
            except ValueError:
                continue
            except IndexError:
                continue
    return ((min_x, min_y), (max_x, max_y))

def ensure_base_dimensions(
    output_width = 0,
    output_height = 0,
    input_path = './originals'
):
    """
        Returns output_width and output_height. If initially provided as 0,
        the variables are first set to the size of a sample tile
    """
    if output_width == 0 or output_height == 0:
        base_dimensions = get_base_dimensions(input_path, '0,0.jpg')
        if (base_dimensions == None):
            print("Cannot get base dimensions")
            return
        (output_width, output_height) = base_dimensions
        print(f"base dimensions: {base_dimensions}")
    return (output_width, output_height)

def make_layer(
    input_path='./originals',
    output_path='./layers',
    scale_x=2,
    scale_y=2,
    layer=1,
    output_width=0,
    output_height=0,
    reverse_y=True,
):
    """
        Creates a whole layer out of original cells
    """
    ((min_x, min_y), (max_x, max_y)) = get_edges(input_path)
    step_x = int(scale_x ** layer)
    step_y = int(scale_y ** layer)

    # get output dimensions
    (output_width, output_height) = ensure_base_dimensions(output_width, output_height, input_path)

    for x in range(min_x, max_x, step_x):
        for y in range(min_y, max_y, step_y):
            make_layer_cell(input_path, output_path, x, y, scale_x, scale_y, layer, min_x, max_x, min_y, max_y, output_width, output_height, reverse_y)

def make_layers(
    input_path='./originals',
    output_path='./layers',
    scale_x=2,
    scale_y=2,
    output_width=0,
    output_height=0,
    reverse_y=True,
    min_layer=1,
    max_layer=6,
):
    """
        Create a number of layers.
    """
    # get output dimensions
    (output_width, output_height) = ensure_base_dimensions(output_width, output_height, input_path)

    for layer in range(min_layer, max_layer):
        print(f"> Creating layer {layer}.")
        make_layer(input_path, output_path, scale_x, scale_y, layer, output_width, output_height, reverse_y)

if __name__ == '__main__':
    make_layers()
    # make_layer_cell(base_x=0, base_y=4, min_x=-2, max_x=6, min_y=-2, max_y=10)