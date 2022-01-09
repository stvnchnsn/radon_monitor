import os
import shutil

import numpy as np
from scipy import misc
import matplotlib.pyplot as plt
import imageio
import cv2
import time


fp = '/Volumes/wellington/projects/radon_monitor/data/unlabled_images/'
to_fp = '/Volumes/wellington/projects/radon_monitor/data/unlabled_img_bucket/'

photo_files = [i.name for i in os.scandir(fp)]
photo_path = [fp+i for i in photo_files]
print('Number of files found = {}'.format(len(photo_path)))
start_time = time.time()
#X = np.array(range(0,785))
X = np.genfromtxt('training_data.csv', delimiter=',')
num_to_label = int(input("How many pictures do you want to label? "))
for path in range(num_to_label):
    og_path = photo_path[path]
    to_path = to_fp+photo_files[path]
    data = imageio.imread(og_path)[:,:,0] 
    img = cv2.imread(og_path,0)
    img = cv2.resize(img,(300,300))
    cv2.imshow(og_path,img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    label = input("What is the number? ")
    data_flat = data.flatten()
    data_labeled = np.zeros(785)
    data_labeled[:784] = data_flat
    data_labeled[784] = float(label)
    X = np.vstack([X,data_labeled])
    shutil.move(og_path,to_path)

photo_files = [i.name for i in os.scandir(fp)]   
print('{} files left to go!'.format(len(photo_files)))
np.savetxt("training_data.csv", X, delimiter=",")
print('Labeling {} number of photos took {} seconds'.format(num_to_label,(round(time.time()-start_time,2))))