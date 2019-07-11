###
# name: sort_pdfs_by_md.py
# author: Emily O'Dean
# purpose: Parse filenames of mining district pdfs and move them to appropriate folders for consumption by webapp
###

import nbmg_helpers
from shutil import copy


def move_files_to_md_folders(file_paths):
    for file_path in file_paths:
        district = file_path.split("_")[-1][:-4]
        destination = "G:\\MININGDIST\\NGGDPP 2019\\PDF FINAL\\" + district + "\\"
        copy(file_path, destination)


def main():
    pdfs = nbmg_helpers.get_list_of_files("G:\\MININGDIST\\NGGDPP 2019\\PDF")
    move_files_to_md_folders(pdfs)