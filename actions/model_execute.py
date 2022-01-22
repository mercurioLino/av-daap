# import requests
# import json
# import shutil
# import requests
# import os
# import joblib
# import numpy as np
# import matplotlib.pyplot as plt
# import os
# import processing
# import utils
# import transform
# import pickle
# from skimage.io import imread
# from sklearn.linear_model import SGDClassifier
# from sklearn.model_selection import cross_val_predict
# from sklearn.preprocessing import StandardScaler, Normalizer
# from sklearn.model_selection import train_test_split
# from skimage.transform import resize
# from joblib import dump, load

# #Função principal para execução do pipeline de classificação
# def pipeline_classification(url_image):
#     warning = {'strike_1': 'False', 'strike_2': 'False', 'send_email': 'False', 'safe': 'False'}
#     describe = {'url': '', 'models': 'nudity, offensive, gore', 'api_user': '133743064', 'api_secret': 'xA9h9Ny3DBzeLPSyKAFL'}
#     describe['url'] = url_image
#     path = 'img.png'

#     #Baixa a imagem a partir da URL fornecida pelo Facebook
#     pull_image(url_image)

#     #Modelo 1 para classificação entre cachorro, gato, humano, vegetação
#     predict_1 = animal_classifier()

#     if predict_1 != 'Dog' and predict_1 != 'Cat':
#         warning['strike_1'] = True

#     predict_2 = offensive_classifier(describe)

#     #Modelo 2 classificação pela API sightengine imagens com conteudo sangrento, ofensivo, ou pornografico
#     if predict_2['safe_prob'] < 0.70:
#         warning['strike_2'] = True

#     #Deleta a imagem criada
#     delete_image(path)

#     if warning['strike_1'] and warning['strike_2'] == True:
#         warning['send_email'] = True
#     elif warning['strike_1'] == True and warning['strike_2'] == False:
#         warning['safe'] = True
#     elif warning['strike_1'] == False and warning['strike_2'] == True:
#         warning['send_email'] = True
#     else:
#         warning['safe'] = True

#     return warning

# #Cria a imagem a partir da URL
# def pull_image(url):
#     response = requests.get(url, stream=True)
#     with open('img.png', 'wb') as out_file:
#         shutil.copyfileobj(response.raw, out_file)
#     del response

# #Após o processamento apaga a imagem para não acumular dados
# def delete_image(path):
#     os.remove(path)

# def animal_classifier():
#     sgd_clf = load_model()
#     data = load_img()
#     data_prepared = transform_data(data)

#     #Prediz a classe para a imagem
#     y_pred = sgd_clf.predict(data_prepared)

#     return y_pred

# def offensive_classifier(describe):  
#     r = requests.get('https://api.sightengine.com/1.0/check.json', params=describe)
#     output = json.loads(r.text)

#     probs = {'gore': '', 'offensive': '', 'safe_prob': ''}
#     probs['gore'] = output['gore']['prob']
#     probs['offensive'] = output['offensive']['prob']
#     probs['safe_prob'] = output['nudity']['safe']

#     return probs

# def create_model():
#     #Carrega o data_set de treinamento 
#     data = joblib.load("data_set_processing\\images_150x150px.pkl")

#     #Função de correção para algumas imagens do data_set de treinamento
#     fix_data = utils.fix_shape(data)

#     #Separação de conjunto de treino e teste
#     X, y = processing.X_y(fix_data)
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=42)

#     ##Cria uma instancia para cada etapa de transformação das imagens
#     grayify = transform.RGB2GrayTransformer()
#     hogify = transform.HogTransformer(pixels_per_cell=(14, 14), cells_per_block=(2,2), orientations=9, block_norm='L2-Hys')
#     scalify = StandardScaler()

#     ##Aplica fit_transform as instancias criadas
#     X_train_gray = grayify.fit_transform(X_train)
#     X_train_hog = hogify.fit_transform(X_train_gray)
#     X_train_prepared = scalify.fit_transform(X_train_hog)

#     #Cria o modelo de classificação
#     sgd_clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
#     sgd_clf.fit(X_train_prepared, y_train)
#     SGDClassifier(random_state=42)

#     file_name = 'model_ready.pkl'
    
#     with open(file_name, 'wb') as open_file:
#         pickle.dump(sgd_clf, open_file)

# def load_model():
#     file_name = 'model_ready.pkl'

#     with open(file_name, 'rb') as open_file:
#         load_classifier = pickle.load(open_file)

#     return load_classifier

# def transform_data(data):
#     ##Cria uma instancia para cada etapa de transformação das imagens
#     grayify = transform.RGB2GrayTransformer()
#     hogify = transform.HogTransformer(pixels_per_cell=(14, 14), cells_per_block=(2,2), orientations=9, block_norm='L2-Hys')
#     scalify = StandardScaler()

#     ##Processamento da imagem de classificação
#     X_test_gray = grayify.fit_transform(data['data'])
#     #Identifica formatos nas imagens utilizando retas
#     X_test_hog = hogify.fit_transform(X_test_gray)
#     #Padroniza o conjunto de dados
#     X_test_prepared = scalify.fit_transform(X_test_hog)

#     return X_test_prepared

# def load_img():
#     #Cria um dict que vai armazenar a imagem
#     data = dict()
#     data['data'] = []

#     #Carrega a imagem para dentro do dict data
#     im = imread(os.path.join('img.png'))
#     #Da um resize na imagem para 150x150
#     im = resize(im, (150, 150))

#     data['data'].append(im)

#     return data

# # url = 'https://clinicaunix.com.br/wp-content/uploads/2019/12/5-pontos-saude-do-homem.jpg'
# # pipeline_classification(url_image=url)