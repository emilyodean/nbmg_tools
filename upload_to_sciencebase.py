import glob
import sciencebasepy
import os
import time

sb = sciencebasepy.SbSession()

username = ""
password = "" #input("enter the password")  #
sb.login(username, password)

sb.is_logged_in()
sb.get_session_info()
sb.logout()


path = "G:\\datasets\\mining_district\\nggdpp\\NGGDPP 2019\\TIF"
files = [f for f in glob.glob(path + "**/*.zip", recursive=False)]

files = files[46:]


for file in files:
    file_id = os.path.splitext(os.path.basename(file))[0]
    print("file ready for upload")
    new_item = {'title': file_id, 'parentId': '5da8e3dfe4b09fd3b0c9c7bc'}
    print("new item created")
    #new_item = sb.create_item(new_item)
    CHUNK_SIZE = 10485760
    sb.upload_file_to_item(new_item, file, scrape_file=False, streaming=True)
    print(file)


for file in files:
    sb.upload_file_and_create_item('5da8e3dfe4b09fd3b0c9c7bc', file)
    print(file)



#### If we don't want to zip up everything

folders = [x[0] for x in os.walk(path)]
folders = folders[1:]  # it keeps the parent folder as item 0

for folder in folders:
    folder_id = os.path.splitext(os.path.basename(folder))[0]
    new_item = {'title': folder_id, 'parentId': '5da8e3dfe4b09fd3b0c9c7bc'}
    files = [f for f in glob.glob(folder + "**/*.tif", recursive=False)]
    sb.upload_files_to_item(new_item, files, scrape_file=False)
