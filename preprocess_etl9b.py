import csv
import cv2
import glob
import numpy as np
import os


file_paths = glob.glob('./original_data/ETL9B/*')
file_paths.sort()
name_index = 0

#24
#1440 #1440
for i, file_path in enumerate(file_paths):
    if '.png' in file_path:
        print(file_path)
        # read img
        img_all = cv2.imread(file_path, 0)
        height = img_all.shape[0]
        width = img_all.shape[1]
        # load labels
        txt_data = open(file_paths[i+1], 'r')
        txt_data = txt_data.read()
        
        labels = []
        n_index = 50
        for i in range(0, len(txt_data), 1):
            if i != n_index:
                labels.append(txt_data[i])
            else:
                n_index = n_index + 51

        for j in range(0, height, 63): # 40
            for k in range(0, width, 64): # 50
                img = img_all[j:j+63, k:k+64]
                label_index = int(j/63)*50 + int(k/64)

                if file_path == './original_data/ETL9B/ETL9B_1_60.png' or file_path == './original_data/ETL9B/ETL9B_2_60.png' or file_path == './original_data/ETL9B/ETL9B_3_60.png' or file_path == './original_data/ETL9B/ETL9B_4_60.png':
                    length_labels = 1440
                elif file_path == './original_data/ETL9B/ETL9B_5_62.png':
                    length_labels = 476
                else:
                    length_labels = 2000

                if label_index < length_labels:
                    label = labels[label_index]

                    label = hex(label.encode("iso-2022-jp")[3])[2:] + hex(label.encode("iso-2022-jp")[4])[2:]
                    
                    dir_name = './processed_data/etl9b/{}'.format(label)
                    os.makedirs(dir_name, exist_ok=True)
                    cv2.imwrite(dir_name + '/' + str(name_index) + '.png', img)
                    name_index = name_index + 1
