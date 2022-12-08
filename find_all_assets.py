# Find all pdf and tiff assets

import os
import csv

path = "G:\\"
all_files = [['file_name', 'full_path', 'file_size', "machine_readable_size"]]


def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".tif"):
            list_item = [file, os.path.join(root, file), sizeof_fmt(os.path.getsize(os.path.join(root, file))), os.path.getsize(os.path.join(root, file))/1000000]
            all_files.append(list_item)
            print(list_item)

with open('digital_assets_gbssrl_tif.csv', mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(all_files)


