import requests
import tempfile
import os

def create_temp_directory():
    temp_dir = tempfile.TemporaryDirectory()
    directory = temp_dir.name
    return directory

"""
Para realizar o post no facebook é necessário possuir a imagem localmente.
Devido a isso é realizado o download da imagem.
"""
def dowload_face_images(image_url, objectid='dowloaded-image'):
    files_objects = []
    if image_url:
        print('image_url', image_url)
        for i, url in enumerate(image_url):
            filename = f'{objectid}-{i}.png'
            dirname = os.path.dirname(__file__)
            dir = os.path.join(dirname, 'images')
            filepath = os.path.join(dir, filename)

            res = requests.get(url, stream=True)
            print(res)

            # capturar caso de erro em que o request falha
            with open(filepath, "wb+") as f:
                f.write(res.content)

            files_objects.append(open(filepath, "rb"))

    return files_objects