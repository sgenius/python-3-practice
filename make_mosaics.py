import os
from make_thumbnails import make_thumbnails

def get_partial_source_images(path='./thumbs',
                              min_x=0,
                              min_y=0,
                              max_x=2,
                              max_y=2):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:

            file_list.append(file)
    return file_list

def make_mosaics(input_path='./thumbs',
                 output_path='./mosaics',
                 min_x=0,
                 min_y=0,
                 max_x=2,
                 max_y=2):
    image