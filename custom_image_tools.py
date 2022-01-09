import os
import numpy as np
import pandas as pd
from scipy import misc
import matplotlib.pyplot as plt
import imageio
import cv2
import shutil
import datetime as dt


def browse_files(photo_path,return_data=False):
    photo_data = imageio.imread(photo_path)
    plt.figure(figsize=(15,15))
    plt.imshow(photo_data)
    if return_data:return photo_data
    
def cutout(position,fp,return_data = False,show=True):
    photo_data = imageio.imread(fp)[:,:,0]
    photo_data = photo_data[position['trow']:position['brow'], position['lcol']:position['rcol']]
    if show:
        plt.figure(figsize=(10,10))
        plt.imshow(photo_data)
    if return_data: return photo_data
def process_photo(img_fp,cut):
    pass

def date_extractor(fp):
    '''returns a timestamp given a filepath'''
    import re
    date_pattern = re.compile('[\d]{2}-[\d]{2}-[\d]{4}_[\d]{4}')
    if date_pattern.search(fp) is None: return None
    else: 
        start_post = date_pattern.search(fp).start()
        end_post = date_pattern.search(fp).end()
    return pd.to_datetime(fp[start_post:end_post],format = '%m-%d-%Y_%H%M')

def send_back_to_training(img_fp, position, label):
    ''' takes image file path, position of inaccurate prediction, and correct label
    and sends to training_data.csv.'''
    ans = input('Are you sure this is the correct label? ')
    if ans == 'n':
        print('not labled')
        return None
    X = np.genfromtxt('training_data.csv', delimiter=',')

    long_term_0 = {'trow':50,'brow':320,'lcol':400,'rcol':580}
    long_term_1 = {'trow':50,'brow':320,'lcol':560,'rcol':740}
    long_term_2 = {'trow':50,'brow':320,'lcol':735,'rcol':915}

    short_term = {'trow':530,'brow':620,'lcol':280,'rcol':360}

    short_term_0 = {'trow':540,'brow':790,'lcol':560,'rcol':660}
    short_term_1 = {'trow':540,'brow':790,'lcol':670,'rcol':770}
    short_term_2 = {'trow':540,'brow':790,'lcol':770,'rcol':870}

    cutout_dic = {'long_term_0':long_term_0,'long_term_1':long_term_1,
            'long_term_2':long_term_2,'short_term':short_term,
            'short_term_0':short_term_0,'short_term_1':short_term_1,
            'short_term_2':short_term_2}
    try:
        photo_data = cutout(cutout_dic[position],img_fp,return_data=True,show=False)
    except KeyError:
        print('''Position must be one of the following:
                long_term_0,long_term_1,long_term_2
                short_term
                short_term_0,short_term_1,short_term_2''')
    photo_data = cv2.resize(photo_data,(28,28))
    data_flat = photo_data.flatten()
    data_labeled = np.zeros(785)
    data_labeled[:784] = data_flat
    data_labeled[784] = float(label)
    X = np.vstack([X,data_labeled])
    np.savetxt("training_data.csv", X, delimiter=",")
    
def read_cutout(cut,model):
    the_image = cutout(cut,image_fp_,return_data=True,show = False)
    the_image = cv2.resize(the_image,(28,28)).flatten()
    pred = model.predict(the_image.reshape((1,-1)))[0]
    if returns_array:return pred.argmax()
    else: return pred

def cutout_sub(fp,show=True,figsize = (10,10)):
    positions_df = pd.read_csv(open('./reference_data/positions.csv','rb'))
    positions_df.loc[:,'coordinates'] = list(map(lambda x:eval(x),positions_df.coordinates))
    positions_df = positions_df.sort_values(by = 'date')
    print('calibrated dates = {}'.format(positions_df.date.unique()))
    date_of_photo = date_extractor(fp)
    print('date of photo = ',date_of_photo.strftime('%m/%d/%Y'))
    
    # find which calibration date to use
    temp = list(positions_df['date'].unique())
    temp.append(date_of_photo.strftime('%m/%d/%Y'))
    temp.sort(key = lambda date: dt.datetime.strptime(date, '%m/%d/%Y'))
    calibration_date = temp[temp.index(date_of_photo.strftime('%m/%d/%Y'))-1] 
    print('calibration date = ',calibration_date)
    
    date_mask = positions_df['date']== calibration_date
    position_coords = positions_df[date_mask]
    photo_data = imageio.imread(fp)[:,:,0]
    f, axes = plt.subplots(nrows = 3,ncols = 3,figsize=figsize)
    axes = axes.flatten()
    for i,(position, coord) in enumerate(zip(position_coords['position'],position_coords['coordinates'])):
        sub_photo_data = photo_data[coord['trow']:coord['brow'], coord['lcol']:coord['rcol']]
        axes[i].imshow(sub_photo_data)
        axes[i].set_title(position)
    axes[7].axis('off')
    axes[8].axis('off')