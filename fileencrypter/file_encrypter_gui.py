import tkinter as tk
import cv2 as cv
import numpy as np
import types
from tkinter import filedialog
from tkinter import ttk
import time, os, sys
import random
import string


import PyVigDec, PyVigEnc

LARGE_FONT = ("Verdana", 12)


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(expand=1, padx=50,pady=25)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def addFile(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                              filetypes=(("Text", "*.txt"), ("All files", "*.*")))
        print(filename)
        labelName = tk.Label(text="You have selected "+os.path.basename(filename))
        labelName.config(wraplength=300)
        labelName.pack()

        fileObj = open(filename)
        self.content = fileObj.read()
        fileObj.close()

    def keyReader(key):
        key_slices = key.split('x')
        return key_slices

    def addSecretImage(self):
        imagename = filedialog.askopenfilename(initialdir="/", title="Select File")
        print(imagename)
        labelSecret = tk.Label(text="You have selected "+os.path.basename(imagename) + " to hide")
        labelSecret.config(wraplength=300)
        labelSecret.pack()
        self.imagename = cv.imread(imagename)

    def addCoverImage(self):
        imagename = filedialog.askopenfilename(initialdir="/", title="Select File")
                                             
        print(imagename)
        labelCover = tk.Label(text="You have selected "+ os.path.basename(imagename) + " to be the cover image")
        labelCover.config(wraplength=300)
        labelCover.pack()
        self.save_covername = imagename
        self.covername = cv.imread(imagename)
        
       
    def returnSecretImageName(self):
        return self.imagename

    def returnCoverImageName(self):
        return self.covername

    def runEncryption(self):
        convertedContent = PyVigEnc.encrypt(self.frames[StartPage].entryKey.get(), self.content)
        print(convertedContent)
        print(self.frames[StartPage].entryOutputFile.get())
        outputFileObj = open(self.frames[StartPage].entryOutputFile.get(), 'w')
        outputFileObj.write(convertedContent)
        outputFileObj.close()

    def runDecryption(self):
        convertedContent = PyVigDec.decrypt(self.frames[StartPage].entryKey.get(), self.content)
        outputFileObj = open(self.frames[StartPage].entryOutputFile.get(), 'w')
        outputFileObj.write(convertedContent)
        outputFileObj.close()

    def genOneTimePad(self):
        keyLength = len(str(self.content))
        print(keyLength)
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ',.!1234567890[]}{@#£$%^&*?()_+abcdefghijklmnopqrstuvwxyz"
        padKey = ''
        for i in range(keyLength): #-1?
            padKey += random.choice(letters)
        return padKey

    def runOneTimePad(self):
        pad_Key = self.genOneTimePad()
        convertedContent = PyVigEnc.encrypt(pad_Key, self.content)
        print(convertedContent)
        # outputFileObj = open(self.frames[StartPage].entryOutputFile.cget("text"), 'w')
        print(self.frames[StartPage].entryOutputFile.get())
        outputFileObj = open(self.frames[StartPage].entryOutputFile.get(), 'w')
        outputFileObj.write(convertedContent)
        outputFileObj.close()

        savedKeyFile = open('Saved_Pad_Key_for_' + self.frames[StartPage].entryOutputFile.get(), 'w')
        savedKeyFile.write(pad_Key)
        savedKeyFile.close()

    def blackWhiteToBinary(self, picture):
        binary_image = ''
        for i in range(picture.shape[0]):
            for j in range(picture.shape[1]):
                if picture[i][j][0] == 0:
                    binary_image += '0'
                else:
                    binary_image += '1'
        return binary_image

    def hideBlackWhite(self,image_data, cover_image):
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

    def colourToBinary(self,picture):
        binary_image = ''
        for i in range(picture.shape[0]):
            for j in range(picture.shape[1]):
                for k in range(3):
                    binary_image += str(( format(picture[i][j][k], "08b") ))

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

    def bwTestPrint(self):
            print('bw selected')
        
    def colourTestPrint(self):
            print('colour selected')

    def steganographicFunction(self):
        if self.frames[PageOne].var_bw.get() == 1:
            binary_image = self.blackWhiteToBinary(self.imagename)
            hidden_image = self.hideBlackWhite(binary_image,self.covername)
            cv.imwrite(self.frames[PageOne].entrySavedName.get(),hidden_image)
            return self.bwTestPrint()
        
        else:
            c_binary_image = self.colourToBinary(self.imagename)
            c_hidden_image = self.hideBlackWhite(c_binary_image, self.covername)
            cv.imwrite(self.frames[PageOne].entrySavedName.get(),c_hidden_image)
            return self.colourTestPrint()
        


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)#, bg="#252D33")
        
        frameTitle = tk.Label(self, text="Cryptography", font=LARGE_FONT, fg="#252D33")
        frameTitle.pack(pady=10, padx=10)

        openFileButton = tk.Button(self, text="Choose File",
                                   command=lambda: controller.addFile())
        openFileButton.pack()

        self.entryKey = tk.Entry(self, bg="#CACACA")
        self.entryKey.pack()
        self.entryKey.insert(0, "Input Key")

        self.entryOutputFile = tk.Entry(self, bg="#CACACA")
        self.entryOutputFile.pack()
        self.entryOutputFile.insert(0, "Saved file name")

        encryptFile = tk.Button(self, text="Encrypt File", padx=10, pady=5, fg="white", bg="#252D33",
                                command=lambda: controller.runEncryption())
        encryptFile.pack(side='left')

        decryptFile = tk.Button(self, text="Decrypt File", padx=10, pady=5, fg="white", bg="#252D33",
                                command=lambda: controller.runDecryption())
        decryptFile.pack(side='right')

        oneTimePad = tk.Button(self, text="One Time Pad", padx=10, pady=5, fg="white", bg="#252D33",
                                command=lambda: controller.runOneTimePad())
        oneTimePad.pack(side='top')

        nextPage = tk.Button(self, text="Steganography", padx=7, pady=5, fg="white", bg="#FFA200",
                    command=lambda: controller.show_frame(PageOne))
        nextPage.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Steganography", font=LARGE_FONT, fg="#FFA200")
        label.pack(pady=10, padx=10)

        chooseSecretImageButton = tk.Button(self, text="Choose image to hide",
                                   command=lambda: controller.addSecretImage())
        chooseSecretImageButton.pack()

        chooseCoverImageButton = tk.Button(self, text="Choose cover image",
                                   command=lambda: controller.addCoverImage())
        chooseCoverImageButton.pack()

        self.var_bw = tk.IntVar()
        self.var_bw.set(0)
        self.check_bw = tk.Checkbutton(self, text='Image to hide is black and white',variable=self.var_bw, onvalue=1, offvalue=0)
        self.check_bw.pack()

        self.entryImageSize = tk.Entry(self, bg="#CACACA")
        self.entryImageSize.pack()
        self.entryImageSize.insert(0, "Size of image")

        self.entrySavedName = tk.Entry(self, bg="#CACACA")
        self.entrySavedName.pack()
        self.entrySavedName.insert(0, "Saved image file name")

        button1 = tk.Button(self, text="Hide Image",
                            command=lambda: controller.steganographicFunction())
        button1.pack()

        lastPage = tk.Button(self, text="Cryptography", padx=7, pady=5, fg="white", bg="#252D33",
                    command=lambda: controller.show_frame(StartPage))
        lastPage.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


app = App()
#app.geometry("400x200")
app.update()
app.mainloop()


