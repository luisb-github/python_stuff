import os

folder_path = r'C:\Users\luisb\Downloads\lol' # replace with the path to the folder containing the files
new_name = 'new_file_name' # replace with the desired new name for the files
i=1
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'): # change this to match the file extension of the files in the folder
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_name + str(i) + '.txt') # change the extension to match the original files
        os.rename(src, dst)

    i += 1