import cv2 as cv
import numpy as np
import types
import sys


imge = cv.imread("input_output/small_goban.jpg")
imge2 = cv.imread("input_output/big_foot_small.jpg")
imge3 = cv.imread("input_output/simple_message_paint.jpg")

# Key is the dimensions of the hidden image
key1 = "100x41"




# Turn colour image into a binary string to iterate over
def colourToBinary(picture):
    binary_image = ''

    # For each row i, and each column j, cycle through the rgb values k. 

    for i in range(picture.shape[0]):
        for j in range(picture.shape[1]):
            for k in range(3):

                # Convert to binary and add to a string.
                binary_image += str(( format(picture[i][j][k], "08b") ))

    return binary_image            


""" test_imge_data = colourToBinary(imge2) """


# Turn black and white image into binary
def blackWhiteToBinary(picture):

    binary_image = ''
    # For each row i, ad each column j, check if black or white.
      
    for i in range(picture.shape[0]):
        for j in range(picture.shape[1]):
            if picture[i][j][0] == 0:
                binary_image += '0'
            else:
                binary_image += '1'
            

    return binary_image




# Hide binary image data in another picture
def hideImage(image_data, cover_image):

    index_binary = 0
    index_max = len(image_data)

   # For every pixel in cover image
    for i in range(cover_image.shape[0]):
        for j in range(cover_image.shape[1]):

            # For each RGB value
        
            for k in range(3):
                # We want to keep going as long as there are bits left in the data
                if index_binary >= index_max:
                    break
                # Remove last (least significant) bit, and add the next bit in image_data
                else:
                    binary_rgb = str(format(cover_image[i][j][k], "08b") )
                    cover_image[i][j][k] = int(binary_rgb[:-1] + image_data[index_binary],2)
                    index_binary += 1

    return cover_image




# Hide in a different way for black and white image data, in such a way that we dont need a key
def hideBlackWhite(image_data, cover_image):
    index_binary = 0
    index_max = len(image_data)

# For every pixel in cover image
    for i in range(cover_image.shape[0]):
        for j in range(cover_image.shape[1]):

            # For the first RGB value 
            # We want to keep going as long as there are bits left in the data
            if index_binary > index_max:
                break
            # Convert RGB to binary then remove last (least significant) bit, and add the next bit from image_data
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
    #number of bits hidden is number (ogImage pixel count) x (3 RGB slots) x (8 bits in colour info)
    data_limit = x_dim*y_dim*3*8
    bit_string = ''
    print(data_limit)
    
    # Retrieve original bit string
    for i in range(cover_image.shape[0]):
        for j in range(cover_image.shape[1]):
            for k in range(3):
                if data_index < data_limit:
                    binary_rgb = str(format(cover_image[i][j][k], "08b") )
                    bit_string += binary_rgb[7]
                    data_index += 1
                else:
                    break

    # Break bit_string into a list of strings each w/ length 8
    ordered_rgb = [ bit_string[i:i+8] for i in range(0, len(bit_string), 8)]
    
    
    
    for i in range(ogImage.shape[0]):
        for j in range(ogImage.shape[1]):
            for k in range(3):
                ogImage[i][j][k] = int(ordered_rgb[0],2)
                ordered_rgb.pop(0)
    return ogImage
#imge.shape[0] = h




def blackWhiteRetriever(cover_image):
    # Construct empty array in the dimentions of the image
    ogImage = np.empty((cover_image.shape[0],cover_image.shape[1],3))

    for i in range(cover_image.shape[0]):
        for j in range(cover_image.shape[1]):
            for k in range(3):

                # Fill ogImage pixel color values with the bit from the corresponding cover_image pixel. 
                # ogImage data is now either 1 or 0, but will be read as either 255 or 0.
                binary_rgb = str(format(cover_image[i][j][0], "08b") )
                ogImage[i][j][k] = int(binary_rgb[7],2)
    
    return ogImage
    





""" cv.imshow("Hidden", hideImage(test_imge_data, imge))
cv.imshow("Original", imge)
# cv.imwrite("bigfoot_hidden_in_goban.jpg", hideImage(test_imge_data, imge))
k = cv.waitKey(0)
 """


# cv.imwrite("bigfoot_hidden_in_goban.jpg", hideImage(test_imge_data, imge))


c_image = hideBlackWhite(blackWhiteToBinary(imge3), imge)
ogImage = blackWhiteRetriever(c_image)


#
test_bit_string = colourToBinary(imge2)
hidden_picture = hideImage(test_bit_string,imge)
ogImage1 = colourImageRetriever(hidden_picture,key1)

cv.imshow("Original", imge2)
cv.imshow("Hidden", hidden_picture)
cv.imshow("Extracted", ogImage1)
k = cv.waitKey(0)

#



""" for i in range(ogImage1.shape[0]):
        for j in range(ogImage1.shape[1]):
            for k in range(3): """

""" cv.imshow("Original", imge3)
cv.imshow("Hidden", c_image)
cv.imshow("Extracted", ogImage) """
# cv.imwrite("bigfoot_hidden_in_goban.jpg", hideImage(test_imge_data, imge))
k = cv.waitKey(0)