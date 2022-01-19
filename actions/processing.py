import joblib
import os
import matplotlib.pyplot as plt
import pprint
import numpy as np
import pandas as pd
from collections import Counter
from skimage.io import imread
from skimage.transform import resize
from sklearn.metrics import confusion_matrix

def resize_all(src, name_arc, include, width=150, height=None):
    """
    load images from path, resize them and write them as arrays to a dictionary, 
    together with labels and metadata. The dictionary is written to a pickle file 
    named '{pklname}_{width}x{height}px.pkl'.
     
    Parameter
    ---------
    src: str
        path to data
    pklname: str
        path to output file
    width: int
        target width of the image in pixels
    include: set[str]
        set containing str
    """
     
    height = height if height is not None else width
     
    data = dict()
    data['description'] = 'resized ({0}x{1})animal images in rgb'.format(int(width), int(height))
    data['label'] = []
    data['filename'] = []
    data['data'] = []   
     
    pklname = f"{name_arc}_{width}x{height}px.pkl"
 
    # read all images in PATH, resize and write to DESTINATION_PATH
    for subdir in os.listdir(src):
        if subdir in include:
            print(subdir)
            current_path = os.path.join(src, subdir)
 
            for file in os.listdir(current_path):
                if file[-3:] in {'jpg', 'png'}:
                    im = imread(os.path.join(current_path, file))
                    im = resize(im, (width, height)) #[:,:,::-1]
                    data['label'].append(subdir[:-4])
                    data['filename'].append(file)
                    data['data'].append(im)
 
        joblib.dump(data, pklname)

def describe_data(path):
    data = joblib.load(path)

    print('Numero de exemplos: ', len(data['data']))
    print('Keys: ', list(data.keys()))
    print('Descrição: ', data['description'])
    print('Formato da imagem: ', data['data'][0].shape)
    print('Labels: ', np.unique(data['label']))
    print(Counter(data['label']))

#Funciona apenas fora do terminal, de preferencia em um notebook
def visualize_data(path):
    data = joblib.load(path)

    labels = np.unique(data['label'])
    fig, axes = plt.subplots(1, len(labels))
    fig.set_size_inches(15, 4)
    fig.tight_layout()

    for ax, label in zip(axes, labels):
        idx = data['label'].index(label)

        ax.imshow(data['data'][idx])
        ax.axis('off')
        ax.set_title(label)


def X_y(data_input):
    X = np.array(data_input['data'])
    y = np.array(data_input['label'])

    return X, y

def plot_bar(y, loc='left', relative=True):
    width = 0.35
    if loc == 'left':
        n = -0.5
    elif loc == 'right':
        n = 0.5
     
    # calculate counts per type and sort, to ensure their order
    unique, counts = np.unique(y, return_counts=True)
    sorted_index = np.argsort(unique)
    unique = unique[sorted_index]
     
    if relative:
        # plot as a percentage
        counts = 100*counts[sorted_index]/len(y)
        ylabel_text = '% count'
    else:
        # plot counts
        counts = counts[sorted_index]
        ylabel_text = 'count'
         
    xtemp = np.arange(len(unique))
     
    plt.bar(xtemp + n*width, counts, align='center', alpha=.7, width=width)
    plt.xticks(xtemp, unique, rotation=45)
    plt.xlabel('equipment type')
    plt.ylabel(ylabel_text)

def visualize_plot_bar(y_train, y_test):
    plt.suptitle('relative amount of photos per type')
    plot_bar(y_train, loc='left')
    plot_bar(y_test, loc='right')
    plt.legend(['train ({0} photos)'.format(len(y_train)), 'test ({0} photos)'.format(len(y_test))])
    plt.show()

def visualize_confusion_matrix(true_label, predict):
    df = pd.DataFrame(np.c_[true_label, predict], columns=['true_label', 'prediction'])
    label_names = ['Dog', 'Cat', 'Human']
    cmx = confusion_matrix(true_label, predict, labels=label_names)
    df = pd.DataFrame(cmx, columns=label_names, index=label_names)
    df.columns.name = 'prediction'
    df.index.name = 'true_label'
    print(df)