# Download negative/background images.

import cv2
import urllib.request
import numpy as np
import os


def scale_raw_images():
    for rawimg in os.listdir('neg'):
        try:
            if os.path.isfile("neg/" + rawimg):
                img = cv2.imread("neg/" + rawimg)
                resized_image = cv2.resize(img, (100, 100))
                cv2.imwrite("neg/scale_100/" + rawimg, resized_image)
        except Exception as e:
            print(str(e))

    pass


def store_raw_images():

    #     neg_images_link = '//image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152'
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1

    if not os.path.exists('neg/scale'):
        os.makedirs('neg/scale')

    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg/" + str(pic_num) + ".jpg")
            img = cv2.imread("neg/" + str(pic_num) +
                             ".jpg", cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            if not os.path.exists('neg/scale_100'):
                os.makedirs('neg/scale_100')

            cv2.imwrite("neg/scale_100/" + str(pic_num) +
                        ".jpg", resized_image)

            pic_num += 1

        except Exception as e:
            print(str(e))


def find_uglies():
    match = False
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type) + '/' + str(img)
                    ugly = cv2.imread('uglies/' + str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly, question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))


def create_pos_n_neg():
    for file_type in ['neg/scale_100']:

        for img in os.listdir(file_type):

            if file_type == 'pos':
                line = file_type + '/' + img + ' 1 0 0 50 50\n'
                with open('info.dat', 'a') as f:
                    f.write(line)
            elif file_type == 'neg/scale_100':
                line = file_type + '/' + img + '\n'
                with open('bg.txt', 'a') as f:
                    f.write(line)


store_raw_images()
# create_pos_n_neg()
# scale_raw_images()
