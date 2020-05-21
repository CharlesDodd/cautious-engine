import cv2 as cv
import numpy as np
import types
import sys

# Retrieve image from same file
img = cv.imread("small_goban.jpg")

# Add a check to make sure the image has been read properly
if img is None:
    sys.exit("Could not read the image.")

# Display the image to test; waitKey ensures window stays open until "k" key is pressed
#cv.imshow("Display", img)
#k = cv.waitKey(0)


# Create function converting string to binary
def toBinary(message):
    if type(message) == str:
        # For each character in the message, convert to binary and join to the string; return the string
        return ''.join([ format(ord(i), "08b") for i in message ])
    elif type(message) == np.ndarray:
        # Later we use the function to convert the pixel RGB data to binary which comes as integers in an np.ndarray
        # We want to output an array in the same way
        return [ format(i, "08b") for i in message ]



# Test by printing
#print(toBinary("Hello"))


# Create function which takes a binary message and an image and outputs the message  hidden in the image
def stegFun(image, bin_message):
    #set an index so we can loop through the message 
    bin_message_index = 0
    max_index = len(bin_message)

    for i in range(img.shape[0]):
       for j in range(img.shape[1]):
           for k in range(3):
               image[i][j][k] = toBinary()




        

