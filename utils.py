import os


def rename_files():
    for file in os.scandir('Templates'):
        if file.is_file():
            if file.path.split('.')[1]=='htm':
                os.rename(file.path,f'{file.path.split(".")[0]}.html')
