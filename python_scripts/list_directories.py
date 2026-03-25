import os
def listdirectory():
    path_name = input("Enter the path:").split(' ')
    print(path_name)
    for paths in path_name:
        try:
            files = os.listdir(paths)
        except FileNotFoundError:
            print("Enter Valid Folder Path")
            continue
    #for path in paths:
#print(path)
#print(files)
        for file in files:
            print(file)
listdirectory()