import numpy as np
import glob
import cv2
import os

# resize function
# resize pic by adding margin
def resize(img):
    width = int(img.shape[1])
    height = int(img.shape[0])
        
    if width == height:
        return_img = img
    elif width > height:
        return_img = np.zeros((width, width))
        return_img[:,:] = 0
        margin = int((width - height) / 2)
        extra = (width - height) % 2
        return_img[margin+extra:width-margin, 0:width] = img[:,:]
    else:
        return_img = np.zeros((height, height))
        return_img[:,:] = 0
        margin = int((height - width) / 2)
        extra = (height - width) % 2
        return_img[0:height, margin+extra:height-margin] = img[:,:]
        
    return_img = cv2.resize(return_img, (64, 64))
    
    # return img_data
    return return_img
    
document_path = './original_data/all/*'
kmnist_aug_path = './processed_data/kuzushiji/'
documents = glob.glob(document_path)

count = 0

for i, document in enumerate(documents):
    char_classes = glob.glob(document + '/characters/*')
    print(document)
    
    for j, char_class in enumerate(char_classes):
        samples = glob.glob(char_class + '/*')
        
        for k, sample in enumerate(samples):
            img = cv2.imread(sample, 0)
            _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            img = cv2.bitwise_not(img)
            img = resize(img)

            u_index = 100
            
            for l in range(0, len(sample), 1):
                if sample[l] == 'U':
                    u_index = l
                if l > u_index and sample[l] == '/':
                    end_index = l
                    break

            os.makedirs(kmnist_aug_path + sample[u_index:end_index], exist_ok = True)
            cv2.imwrite(kmnist_aug_path + sample[u_index:end_index] + '/' + str(count) + '.png', img)
            count = count + 1
