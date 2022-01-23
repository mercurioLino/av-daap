import requests
import tempfile

def create_temp_directory():
    temp_dir = tempfile.TemporaryDirectory()
    directory = temp_dir.name
    return directory

def dowload_face_images(image_url, objectid='dowloaded-image'):
    files_objects = []
    if image_url:
        print('image_url', image_url)
        dir = create_temp_directory()
        for i, url in enumerate(image_url):
            filename = f'{objectid}-{i}.png'
            filepath = f'/home/vinicius/Documentos/daap/av-daap/modules/facebook/images/{filename}'

            res = requests.get(url, stream=True)
            print(res)

            # capturar caso de erro em que o request falha
            with open(filepath, "wb+") as f:
                f.write(res.content)

            files_objects.append(open(filepath, "rb"))

    return files_objects