import os, shutil


for indice, arquivo in enumerate(os.listdir()):
    shutil.move(arquivo, str(indice)+'.jpg')
