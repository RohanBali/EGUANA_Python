# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 18:05:49 2016

@author: rohanbali
"""

from tkinter import *

root = Tk()
for r in range(3):
    for c in range(4):
        Label(root, text='R%s/C%s'%(r,c),borderwidth=1 ).grid(row=r,column=c)

root.mainloop(  )