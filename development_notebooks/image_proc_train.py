import os
import numpy as np
import imageio
import cv2
import shutil
import time
#### To be depreciated due to calibration requirements for positions ####
''' Used to create training set.
Converts from raw pictures in 'hourly_tests' folder to 
unlabled cut outs in unlabled_images folder. 
Also transfers original file to og_images folder'''

fp = '/Volumes/wellington/projects/radon_monitor/data/hourly_tests/'
photo_files = [i.name for i in os.scandir(fp)]
photo_path = [fp+i for i in photo_files]
print('Number of files found = {}'.format(len(photo_path)))

# positions.  See image_explorer.ipynb for method 



long_term_0 = {'trow':50,'brow':320,'lcol':400,'rcol':580}
long_term_1 = {'trow':50,'brow':320,'lcol':560,'rcol':740}
long_term_2 = {'trow':50,'brow':320,'lcol':735,'rcol':915}

short_term = {'trow':530,'brow':620,'lcol':280,'rcol':360}

short_term_0 = {'trow':540,'brow':790,'lcol':560,'rcol':660}
short_term_1 = {'trow':540,'brow':790,'lcol':670,'rcol':770}
short_term_2 = {'trow':540,'brow':790,'lcol':770,'rcol':870}

cutout_dic = {'long_term0':long_term_0,'long_term1':long_term_1,
            'long_term2':long_term_2,'short_term':short_term,
            'short_term_0':short_term_0,'short_term_1':short_term_1,
            'short_term_2':short_term_2}
class Image_Processor():
    '''to do convert the below functions into a class'''
    pass


def cutout(position,fp,return_data = False,show=True):
    try: photo_data = imageio.imread(fp)
    except: print(fp)
    photo_data = photo_data[position['trow']:position['brow'], position['lcol']:position['rcol']]
    if show:
        plt.figure(figsize=(10,10))
        plt.imshow(photo_data)
    if return_data: return photo_data

def process_photo():
    for photo in photo_path:
        for position,cut in cutout_dic.items():
            photo_data = cutout(cut,photo,return_data=True,show=False)
            photo_data = cv2.resize(photo_data,(28,28))
            imageio.imwrite('./data/unlabled_images/'+position+photo[-18:],photo_data)
        shutil.move(photo,'./data/og_images')

if __name__ == '__main__':
    start_time = time.time()
    process_photo()
    print("Processing time = ".format(time.time() - start_time))