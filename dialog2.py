# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 23:24:40 2016

@author: rohanbali
"""

from tkinter import Tk,simpledialog, Label, Entry

class MyDialog(simpledialog.Dialog):

    def body(self, master):
        self.focus()
        Label(master, text="First:").grid(row=0)
        Label(master, text="Second:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        
        return self.e1 # initial focus

    def apply(self):
        first = int(self.e1.get())
        second = int(self.e2.get())
        print (first)
        print(second) # or something

