import tkinter as tk
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
        container.pack(expand=1)
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

    def addSecretImage(self):
        imagename = filedialog.askopenfilename(initialdir="/", title="Select File")
        print(imagename)
        labelName = tk.Label(text="You have selected "+os.path.basename(imagename) + " to hide")
        labelName.config(wraplength=300)
        labelName.pack()

        self.imagename = imagename

    def addCoverImage(self):
        imagename = filedialog.askopenfilename(initialdir="/", title="Select File")
                                             
        print(imagename)
        labelName = tk.Label(text="You have selected "+ os.path.basename(imagename) + " to be the cover image")
        labelName.config(wraplength=300)
        labelName.pack()

        self.covername = imagename
        
       
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

        self.entrySavedName = tk.Entry(self, bg="#CACACA")
        self.entrySavedName.pack()
        self.entrySavedName.insert(0, "Saved image file name")

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        lastPage = tk.Button(self, text="Steganography", padx=7, pady=5, fg="white", bg="#252D33",
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
app.geometry("400x200")
app.mainloop()



