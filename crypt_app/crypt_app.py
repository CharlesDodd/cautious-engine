
import tkinter as tk
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
        tk.Tk.wm_title(self, "Cautious Engine")
        

        container = tk.Frame(self)
        container.pack(expand=1, padx=50,pady=25)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageTwo):
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

    def runEncryption(self):
        convertedContent = PyVigEnc.encrypt(self.frames[StartPage].entryKey.get(), self.content)
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
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz"
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

        openFileButton = ttk.Button(self, text="Choose File",
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
