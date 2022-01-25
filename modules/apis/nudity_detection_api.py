import requests
import json
import os


"""
Comumente o usuário envia mais de uma imagem, por isso, essa função
itera pelas imagens e invoca, para cada imagem, a função que de fato
realiza a chamada a API que identifica nudez explicita, sangue e
conteúdo ofensivo.
"""
def safe_api(image_url):
    if image_url is None or image_url == '' or image_url == []:
        print('Nenhum link foi especificado')
        return None
    safe = None
    for image in image_url:
        safe = offensive_classifier(image)
        # se alguma imagem não for segura nem precisa olhar a seguinte
        if safe is False:
            return safe
    return safe

"""
Realiza uma requisição a API que identifica nudez explicita, sangue e conteúdo
ofensivo em uma imagem, para garantir que as diretrizes do Facebook não
serão desrespeitadas ao publicar a imagem.

Essa API retorna um conjunto de probabilidades, que são analisadas pela função
e representadas por uma única variável booleana. Essa variável indica se as
imagens são seguras ou não para serem publicadas no Facebook.
"""
def offensive_classifier(image):  
    describe = {'url': image, 'models': 'nudity, offensive, gore', 'api_user': os.environ['SAFE_API_USER_ID'], 'api_secret': os.environ['SAFE_API_TOKEN']}
    try:
        r = requests.get('https://api.sightengine.com/1.0/check.json', params=describe)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(e)
        return None
    except requests.exceptions.RequestException as e:
        print(e)
        return None
    
    output = json.loads(r.text)
    print(output)
    if output:
        safe = True
        probs = {'gore': output['gore']['prob'], 
                 'offensive': output['offensive']['prob'],
                 'safe_nudity': output['nudity']['safe']}
        
        # Se a probabilidade de gore for maior que 10%
        if probs['gore'] > 0.1:
            safe = False
        # Se a probabilidade de offensive for maior que 10%
        if probs['offensive'] > 0.1:
            safe = False
        # Se o nível de safe para nudity for menor que 90%
        if probs['safe_nudity'] < 0.9:
            safe = False 
        return safe
    return None