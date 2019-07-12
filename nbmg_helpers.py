###
# name: nbmg_helpers.py
# author: Emily O'Dean
# purpose: General functions for reuse in NBMG processes
###
import os, errno


def get_list_of_files(path):
    list_of_file = os.listdir(path)
    all_files = list()
    for entry in list_of_file:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)
    return all_files


def get_list_of_folders(path):
    list_of_folders = os.listdir(path)
    all_folders = list()
    for entry in list_of_folders:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            all_folders.append(full_path)
    return all_folders


def create_new_folder(path):
    try:
        os.mkdir(path)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass


        try:
            os.mkdir(path)
        except OSError as exc:
            print("Creation of the directory %s failed" % path)
            print(OSError.strerror)
        else:
            print("Successfully created the directory %s " % path)


def get_list_of_tifs(path):
    image_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".tif") or file.endswith(".TIF"):
                image_files.append(os.path.join(root, file))
    return image_files