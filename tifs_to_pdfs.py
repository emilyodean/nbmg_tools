###
# name: tifs_to_pdfs.py
# author: Emily O'Dean
# purpose: For each subfolder in a directory, take all tifs and knit them into pdfs
###

import img2pdf
import nbmg_helpers


def pdf_it(folder_name):
    path = "G:\\new_structure\\datasets\\cores_cuttings\\pdfs\\"
    tifs = nbmg_helpers.get_list_of_tifs(folder_name)
    image_files = sort_list(tifs)

    if image_files:
        id = folder_name.split("\\")[-1]
        new_path = path + id
        nbmg_helpers.create_new_folder(new_path)
        output_file = new_path + "\\" + id + ".pdf"
        pdf_bytes = img2pdf.convert(image_files)
        file = open(output_file, "wb")
        file.write(pdf_bytes)
        file.close()
    else:
        print("Couldn't find any TIFs")


def sort_list(image_files):
    first = []
    second = []
    third = []
    fourth = []
    for name in image_files:
        if "INFO" in name:
            first.append(name)
        elif "TS" in name:
            second.append(name)
        elif "PPL" in name:
            third.append(name)
        else:
            fourth.append(name)
    updated_list = first + second + third + fourth
    return updated_list


def main():
    image_directory = 'G:\\new_structure\\datasets\\cores_cuttings\\scans'
    folders = nbmg_helpers.get_list_of_folders(image_directory)
    for folder in folders:
        pdf_it(folder)

