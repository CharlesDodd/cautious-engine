import cv2 as cv
import numpy as np
import types
import sys

def colourToBinary(picture):
    binary_image = ''
    for i in range(picture.shape[0]):
        for j in range(picture.shape[1]):
            for k in range(3):
                binary_image += str(( format(picture[i][j][k], "08b") ))
    return binary_image     

def blackWhiteToBinary(picture):
    binary_image = ''
    for i in range(picture.shape[0]):
        for j in range(picture.shape[1]):
            if picture[i][j][0] == 0:
                binary_image += '0'
            else:
                binary_image += '1'
    return binary_image

def hideImage(image_data, cover_image):
    index_binary = 0
    index_max = len(image_data)
    for i in range(cover_image.shape[0]):
        for j in range(cover_image.shape[1]):
            for k in range(3):
                if index_binary >= index_max:
                    break
                else:
                    binary_rgb = str(format(cover_image[i][j][k], "08b") )
                    cover_image[i][j][k] = int(binary_rgb[:-1] + image_data[index_binary],2)
                    index_binary += 1
    return cover_image

def hideBlackWhite(image_data, cover_image):
    index_binary = 0
    index_max = len(image_data)
    for i in range(cover_image.shape[0]):
        for j in range(cover_image.shape[1]):
            if index_binary > index_max:
                break
            else:
                binary_rgb = str(format(cover_image[i][j][0], "08b") )
                cover_image[i][j][0] = int(binary_rgb[:-1] + image_data[index_binary],2)
                index_binary += 1
    return cover_image

def keyReader(key):
    key_slices = key.split('x')
    return key_slices

def colourImageRetriever(cover_image,key):
    x_dim = int(keyReader(key)[1])
    y_dim = int(keyReader(key)[0])
    ogImage = np.zeros((x_dim,y_dim,3),np.uint8)
    data_index = 0
    data_limit = x_dim*y_dim*3*8
    bit_string = ''
    print(data_limit)
    for i in range(cover_image.shape[0]):
        for j in range(cover_image.shape[1]):
            for k in range(3):
                if data_index < data_limit:
                    binary_rgb = str(format(cover_image[i][j][k], "08b") )
                    bit_string += binary_rgb[7]
                    data_index += 1
                else:
                    break
    ordered_rgb = [ bit_string[i:i+8] for i in range(0, len(bit_string), 8)]
    for i in range(ogImage.shape[0]):
        for j in range(ogImage.shape[1]):
            for k in range(3):
                ogImage[i][j][k] = int(ordered_rgb[0],2)
                ordered_rgb.pop(0)
    return ogImage

def blackWhiteRetriever(cover_image):
    print("passing in cover image",cover_image)
    ogImage = np.zeros((cover_image.shape[0],cover_image.shape[1],3))
    for i in range(cover_image.shape[0]):
        for j in range(cover_image.shape[1]):
            for k in range(3):
                binary_rgb = str(format(cover_image[i][j][0], "08b") )
                ogImage[i][j][k] = int(binary_rgb[-1],2)*255 # -1 instead of 7 on binary_rgb
    print("og image before being returned(after hiding)",ogImage)
    return ogImage

