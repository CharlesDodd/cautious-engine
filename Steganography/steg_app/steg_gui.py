import tkinter as tk
import cv2 as cv
import numpy as np
import types
from tkinter import filedialog
from tkinter import ttk
import time, os, sys
import random
import string
import steg_functions
import secrets

LARGE_FONT = ("Verdana", 12)

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(expand=1, padx=50,pady=25)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (PageOne, PageTwo):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageOne)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def addSecretImage(self):
        imagename = filedialog.askopenfilename(initialdir="/", title="Select File")
        labelSecret = tk.Label(text="You have selected "+os.path.basename(imagename) + " to hide")
        labelSecret.config(wraplength=300)
        labelSecret.pack()
        self.imagename = cv.imread(imagename)
        
    def addCoverImage(self):
        covername = filedialog.askopenfilename(initialdir="/", title="Select File")
        labelCover = tk.Label(text="You have selected "+ os.path.basename(covername) + " to be the cover image")
        labelCover.config(wraplength=300)
        labelCover.pack()
        self.save_covername = covername
        self.covername = cv.imread(covername)

    def rnd_img(self, x_dim, y_dim):
        empty_img = np.zeros((x_dim,y_dim,3),np.uint8)
        for i in range(x_dim):
            for j in range(y_dim):
                for k in range(3):
                    empty_img[i][j][k] = secrets.choice(range(0,255))
        cv.imwrite(self.frames[PageTwo].entryRandomName.get(), empty_img)
        labelRnd = tk.Label(text="You have saved "+str(self.frames[PageTwo].entryRandomName.get()) )
        labelRnd.config(wraplength=300)
        labelRnd.pack()

    def steganographicFunction(self):
        print(self.frames[PageOne].var_bw.get())
        if self.frames[PageOne].var_bw.get() == 1:
            binary_image = steg_functions.blackWhiteToBinary(self.imagename)
            hidden_image = steg_functions.hideBlackWhite(binary_image,self.covername)
            cv.imwrite(self.frames[PageOne].entrySavedName.get(), hidden_image)
        
        else:
            c_binary_image = steg_functions.colourToBinary(self.imagename)
            c_hidden_image = steg_functions.hideImage(c_binary_image, self.covername)
            cv.imwrite(self.frames[PageOne].entrySavedName.get(),c_hidden_image)
            return 

    def retriever(self):
        if self.frames[PageOne].var_bw.get() == 1:
            ogImage = steg_functions.blackWhiteRetriever(self.covername)
            cv.imwrite(self.frames[PageOne].entrySavedName.get(), ogImage)

        else:
            ogImage = steg_functions.colourImageRetriever(self.covername, self.frames[PageOne].entryImageSize.get())
            cv.imwrite(self.frames[PageOne].entrySavedName.get(), ogImage)

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
        self.entryImageSize.insert(0, "Image size eg '100x200'")

        self.entrySavedName = tk.Entry(self, bg="#CACACA")
        self.entrySavedName.pack()
        self.entrySavedName.insert(0, "Saved image name")

        buttonHide = tk.Button(self, text="Hide Image",
                            command=lambda: controller.steganographicFunction())
        buttonHide.pack()

        buttonTest = tk.Button(self, text="Retrieve Image",
                            command=lambda: controller.retriever())
        buttonTest.pack()

        button2 = tk.Button(self, text="Create Random Image",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()








class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Create a random cover image", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.entryXSize = tk.Entry(self, bg="#CACACA")
        self.entryXSize.pack()
        self.entryXSize.insert(0, "X dimension")

        self.entryYSize = tk.Entry(self, bg="#CACACA")
        self.entryYSize.pack()
        self.entryYSize.insert(0, "Y dimension")

        self.entryRandomName = tk.Entry(self, bg="#CACACA")
        self.entryRandomName.pack()
        self.entryRandomName.insert(0, "Image_saved_name.png")

        buttonRandomimg = tk.Button(self, text="Create Random Image",
                            command=lambda: controller.rnd_img(int(self.entryYSize.get()), int(self.entryXSize.get())))
        buttonRandomimg.pack()

        buttonReturn = tk.Button(self, text="Back",
                            command=lambda: controller.show_frame(PageOne))
        buttonReturn.pack()





app = App()
#app.geometry("400x200")
app.update()
app.mainloop()
