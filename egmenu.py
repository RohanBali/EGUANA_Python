# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:15:51 2016

@author: rohanbali
"""
from tkinter import Menu
from tkinter import BooleanVar

class EguanaMenu(Menu):
    
 def __init__(self, parent,delegate):
        Menu.__init__(self, parent)   
        
        self.delegate = delegate
        self.initUI()
        
 def initUI(self):
 
    self.menu_file = Menu(self)
    self.menu_file.add_command(label='Load 3D')
    self.menu_file.add_command(label='Load 2D')

    self.menu_file.add_command(label='Exit',command=self.delegate.quit)
    
    self.add_cascade(menu=self.menu_file, label='File')

    self.menu_Filter = Menu(self)
    
    bV = BooleanVar()
    bV2 = BooleanVar()
    
    self.menu_Filter.add_checkbutton(label="Speech 3D", onvalue=1, offvalue=0, variable=bV, command=self.delegate.speech3DButtonPressed)
    self.menu_Filter.add_checkbutton(label='Speech 2D',onvalue=1, offvalue=0, variable=bV2, command=self.delegate.speech2DButtonPressed)
    self.menu_Filter.add_command(label='Swallow 3D',command=self.delegate.swallow3DButtonPressed)
    self.menu_Filter.add_command(label='Swallow 2D',command=self.delegate.swallow2DButtonPressed)

    self.add_cascade(menu=self.menu_Filter, label='Filter')
    
    self.entryconfigure('Filter', state = 'disabled')