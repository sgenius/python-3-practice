import os

def get_source_images(path='./originals'):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(file)
    return file_list

if __name__ == '__main__':
    get_source_images()