import os
import numpy as np
import pandas as pd
from scipy import misc
import matplotlib.pyplot as plt
import imageio
import cv2
import shutil
import datetime as dt
import time

def test():
    rm = Radon_Monitor()
    

protocol = test

# Paths
REFERENCE_DATA_PATH = './reference_data/' # calibration key
RESULTS_FILE= './results.csv'
RAW_PHOTO_PATH = '/Volumes/sambashare/projects/radon_monitor/data/hourly_tests/'
TO_BE_LABELED_CUTOUTS = '/Volumes/sambashare/projects/radon_monitor/data/unlabled_images/'
LABELED_CUTOUT_IMGS = '/Volumes/sambashare/projects/radon_monitor/data/unlabled_img_bucket/'


class Radon_Monitor:
    def __init__(self):
        global REFERENCE_DATA_PATH, RAW_PHOTO_PATH
        global TO_BE_LABELED_CUTOUTS,RESULTS_FILE

        self.positions_df = pd.read_csv(open(REFERENCE_DATA_PATH+'positions.csv','rb'))
        self.positions_df.loc[:,'coordinates'] = list(map(lambda x:eval(x),self.positions_df.coordinates))
        self.positions_df = self.positions_df.sort_values(by ='date')
        self.calibrated_dates = list(self.positions_df.date.unique())
        self.photo_files = [i.name for i in os.scandir(RAW_PHOTO_PATH)]
        self.photo_path = [RAW_PHOTO_PATH+fn for fn in self.photo_files]
        self.photo_dates = [self._date_extractor(RAW_PHOTO_PATH+fn) for fn in self.photo_files]
        self.date_path_map = pd.DataFrame()
        for i, (date, path) in enumerate(zip(self.photo_dates,self.photo_path)):
            self.date_path_map.loc[i,'date'] = date
            self.date_path_map.loc[i,'path'] = path
        self.date_path_map = self.date_path_map.sort_values(by = 'date').reset_index(drop = True)
        self.date_path_map['day'] = self.date_path_map['date'].dt.strftime('%m/%d/%Y')
        self.date_path_map['hour'] = self.date_path_map['date'].dt.hour
        try:
            self.img_df = pd.read_csv(RESULTS_FILE)
            self.img_df['img_date'] = pd.to_datetime(self.img_df['img_date'])
            self.img_df = self.img_df.dropna(subset = ['short_term_span'])
            self.img_df['month'] = self.img_df['img_date'].dt.month
            self.img_df['day'] = self.img_df['img_date'].dt.day
            self.img_df['year'] = self.img_df['img_date'].dt.year
            print("{} previous radon measurements found".format(len(self.img_df)))
        except:
            print('No previous radon measurements found, intalizing new database')
            self.img_df = pd.DataFrame(columns = ['img_date','img_path','img_name'])
        
    def browse_photos(self,photo_path,return_data = False,figsize = (15,15)):
        '''displays one raw photo image and returns data if selected'''
        photo_data = imageio.imread(photo_path)
        plt.figure(figsize = figsize)
        plt.imshow(photo_data)
        plt.show()
        if return_data:return photo_data
    def _date_extractor(self,fp):
        '''derives the date of the photo by filename'''
        import re
        date_pattern = re.compile('[\d]{2}-[\d]{2}-[\d]{4}_[\d]{4}')
        if date_pattern.search(fp) is None: return None
        else: 
            start_post = date_pattern.search(fp).start()
            end_post = date_pattern.search(fp).end()
        return pd.to_datetime(fp[start_post:end_post],format = '%m-%d-%Y_%H%M')
    def _calibration_date(self,fp,print_results = False):
        '''returns which calibration date to use in the form
        %m/%d/%Y based of the file path'''
        date_of_photo = self._date_extractor(fp)
        temp = self.calibrated_dates.copy()
        #print(type(date_of_photo))
        if date_of_photo.strftime('%m/%d/%Y') in temp: 
            
            return date_of_photo.strftime('%m/%d/%Y')  # in the case when the calibration date matches the date of the photo
        temp.append(date_of_photo.strftime('%m/%d/%Y'))
        temp.sort(key = lambda date: dt.datetime.strptime(date, '%m/%d/%Y'))

        calibration_date = temp[temp.index(date_of_photo.strftime('%m/%d/%Y'))-1]
        if print_results:
            print('''calibrated dates = {}\ndate of photo = {}\nmatched calibration date = {}'''.\
                format(self.calibrated_dates,
                        date_of_photo.strftime('%m/%d/%Y'),
                        calibration_date)
                )
        return calibration_date
    def coordinates(self,fp):
        '''returns the coordinates based on the file path'''
        date_mask =  self.positions_df['date'] == self._calibration_date(fp,print_results = False)
        cols = ['date','position','coordinates']
        return self.positions_df[cols][date_mask]

    def cutout_sub(self,fp,calibration_mode = False, figsize = (10,10),savefig = False):
        '''Shows subplot of cut outs. If calibration_mode = True, then calibration positions
        must be entered, otherwise the calibration posistions are derived using _calibration_date'''
        if not calibration_mode:
            # date_mask =  self.positions_df['date'] == self._calibration_date(fp,print_results = True)
            # position_coords = self.positions_df[date_mask]
            position_coords = self.coordinates(fp)
        else:
            pass
        photo_data = imageio.imread(fp)[:,:,0]
        f, axes = plt.subplots(nrows = 3,ncols = 3,figsize=figsize)
        axes = axes.flatten()
        for i,(position, coord) in enumerate(zip(position_coords['position'],position_coords['coordinates'])):
            sub_photo_data = photo_data[coord['trow']:coord['brow'], coord['lcol']:coord['rcol']]
            axes[i].imshow(sub_photo_data)
            axes[i].set_title(position)
        axes[7].axis('off')
        axes[8].axis('off')
        fig1 = plt.gcf()
        if savefig == True:
            plt.savefig('./figures/calibrator_example.png')
        else:
            plt.show()
        self.browse_photos(fp)
    def scope(self,position,fp,return_data = False,show = True):
        photo_data = imageio.imread(fp)
        photo_data[position['trow']:position['brow'], position['lcol']:position['rcol'],1]=100
        if show:
            plt.figure(figsize=(10,10))
            plt.imshow(photo_data)
        if return_data: return photo_data
    def cutout(self,position,fp,return_data = False,show=True):
        photo_data = imageio.imread(fp)[:,:,0]
        photo_data = photo_data[position['trow']:position['brow'], position['lcol']:position['rcol']]
        if show:
            plt.figure(figsize=(10,10))
            plt.imshow(photo_data)
        if return_data: return photo_data
    def coord_shifter(self,og_coords, direction, pixels):
        '''calibration tool'''
        new_coords = og_coords.copy()
        if direction == 'horizontal':
            new_coords['lcol'] = new_coords['lcol']+pixels
            new_coords['rcol'] = new_coords['rcol'] +pixels
            return new_coords
        if direction == 'vertical':
            new_coords['trow'] = new_coords['trow']+pixels
            new_coords['brow'] = new_coords['brow'] +pixels
            return new_coords
    def calibrate_a_date(self):
        '''place saver to eventually replace the calibrator notebook'''
        pass
    
    def read_image(self):
        pass


    def image_proc_train(self,num_photos_to_add = 1000):
        ''' Used to create unlabeled training set.
        Converts from raw pictures in 'hourly_tests' folder to 
        unlabled cut outs in unlabled_images folder. 
        '''
        failed_file_paths = []
        for k, photo_fp in enumerate(self.photo_path):
            photo_date = self._date_extractor(photo_fp).strftime('%m_%d_%Y')
            try:photo_data = imageio.imread(photo_fp)[:,:,0]
            except:
                failed_file_paths.append(photo_fp)
                print('failed on file path ',photo_fp)
                _ = input('Check Server Connection')
                continue
            date_mask =  self.positions_df['date'] == self._calibration_date(photo_fp,print_results = False)
            position_coords = self.positions_df[date_mask]
            for i,(position, coord) in enumerate(zip(position_coords['position'],position_coords['coordinates'])):
                subphoto_data = photo_data[coord['trow']:coord['brow'], coord['lcol']:coord['rcol']]
                subphoto_data = cv2.resize(subphoto_data,(28,28))
                save_to = TO_BE_LABELED_CUTOUTS+position+'_'+photo_date+'.png'
                imageio.imwrite(save_to,subphoto_data)
                time.sleep(2) # wellington keeps crashing, hoping the giving a 1 second break between saves might help
            
            print('successfully processed ',photo_fp)
            if k > num_photos_to_add:
                print('{} photos processed'.format(num_photos_to_add))
                break
        print(failed_file_paths)
if __name__ == '__main__':
    protocol()