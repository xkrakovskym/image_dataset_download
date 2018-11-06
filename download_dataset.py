"""
This script should download and shuffle images for image classification problem.
"""
import os
import shutil
import random
from google_images_download import google_images_download


def download_images(keywords, num_of_images, output_path):
    # class instantiation
    response = google_images_download.googleimagesdownload()

    # creating list of arguments
    arguments = {"keywords": keywords, "limit": num_of_images, "print_urls": True,
                 "output_directory": output_path, "chromedriver": "/usr/bin/chromedriver"}
    paths = response.download(arguments)   # passing the arguments to the function
    print(paths)   # printing absolute paths of the downloaded images


def move_files(src, dest, num_to_move=None, rename=False):
    # all files
    files = os.listdir(src)
    # if not passed move all
    if not num_to_move:
        num_to_move = len(files)

    for i, f in enumerate(random.sample(files, num_to_move)):
        if rename:
            shutil.move(src + f, dest + str(i) + '.jpg')
        else:
            shutil.move(src + f, dest)


def create_structure(keywords, set_division):

    list_of_labels = keywords.keys()

    # list of labels in the image folder to be shuffled
    parent_dir = "./images/" + "".join(list_of_labels)
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
        os.mkdir(parent_dir + '/train/')
        os.mkdir(parent_dir + '/valid/')
        os.mkdir(parent_dir + '/test1/')
        os.mkdir(parent_dir + '/models/')

    train_prc = set_division["train_prc"]
    valid_prc = set_division["valid_prc"]
    test_path = parent_dir + '/test1/'
    # train and valid sub-folders
    for folder in list_of_labels:
        train_path = parent_dir + '/train/' + folder + "/"
        valid_path = parent_dir + '/valid/' + folder + "/"
        input_path = './images/' + folder + "/"
        num_of_files = len(os.listdir(input_path))
        # create folder and move files
        if not os.path.exists(train_path):
            os.mkdir(train_path)
        move_files(input_path, train_path, (num_of_files*train_prc)//100)

        # create folder and move files
        if not os.path.exists(valid_path):
            os.mkdir(valid_path)
        move_files(input_path, valid_path, (num_of_files*valid_prc)//100)

        # move the rest of the images to test and remove the folder
        move_files(input_path, test_path)
        os.rmdir(input_path)

    # move rest to the test and rename using just numbers
    move_files(test_path, test_path, rename=True)

    print("The folder structure was created!")


def download_set(keywords, limit=100):
    """
    Download images according to keywords dict to ./images folder and renames them using keys in the keywords
    :param keywords: dict containing label: keyword pairs
    :param limit: num of images to donwload
    """
    for kword in keywords.keys():
        download_images(keywords[kword], limit, './images/')
        while True:
            is_done = input("Did you cleaned the image folder " + os.getcwd() + "/images/" + keywords[kword] +
                            " from images which are not correct?\nPress y(es) to continue.")
            if is_done == 'y':
                break
        # label and rename
        number = 0
        path_to_images = "./images/" + keywords[kword] + '/'
        for file in os.listdir(path_to_images):
            try:
                os.rename(path_to_images + file, path_to_images + kword + "." + str(number) + '.jpg')
                number += 1
            except:
                print("There was error renaming: " + file)

        # this will use label as a name of the folder (should prevent having spaces in the folder name)
        os.rename("./images/" + keywords[kword], "./images/" + kword.replace(' ', ''))


def create_dataset(keywords, limit, do_download=True, create_folders=True, set_division=None):
    """
    :param keywords: dict composed of labels and their respective keywords
                        which should be used for a google image search
    :param limit: number of images to be downloaded per keyword
    :param do_download: bool which decides if download should be done
    :param create_folders: bool which decides if the folder struct should be done
    :param set_division: percentage division between train and valid folders
    """
    # default values are set here
    if not set_division:
        set_division = {'train_prc': 60, 'valid_prc': 20}
    # create images folder if doesn't exist
    if not os.path.exists('./images'):
        os.mkdir('./images')

    if do_download:
        download_set(keywords, limit)
    if create_folders:
        create_structure(keywords, set_division)


if __name__ == "__main__":
    key_words = {"man": "man", "woman": "woman"}
    num_of_images_to_download = 200
    create_dataset(key_words, num_of_images_to_download)
