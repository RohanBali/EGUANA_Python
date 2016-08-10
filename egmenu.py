# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:15:51 2016

@author: rohanbali
"""
from tkinter import Menu, DISABLED, NORMAL
from tkinter import BooleanVar

class EguanaMenu(Menu):
    
 def __init__(self, parent,delegate):
        Menu.__init__(self, parent)   
        
        self.delegate = delegate
        self.initUI()
        self.inputDevice = None
        self.toggleBooleanButtonStates = []
 def initUI(self):
 
    self.menu_file = Menu(self)
    self.menu_file.add_command(label='Load 3D')
    self.menu_file.add_command(label='Load 2D')

    self.menu_file.add_command(label='Exit',command=self.delegate.quit)
    
    self.add_cascade(menu=self.menu_file, label='File')
    
 def filterSelected(self,buttonIndex):
     for i in range(4):
         if not i == buttonIndex:
             b = getattr(self,'b'+str(i))
             b.set(False)
        
        
 def inputSelected(self,inputDevice):
    self.inputDevice = inputDevice
    filterFunctionObjects = self.inputDevice.allowedFilterFunctions

    menu_Filter = Menu(self)

    for i in range(len(filterFunctionObjects)):
        classObject = filterFunctionObjects[i]
        buttonBool = BooleanVar()
        self.toggleBooleanButtonStates.append(buttonBool)
        menu_Filter.add_checkbutton(label=classObject.name, onvalue=1, offvalue=0, variable=buttonBool, command=classObject.filterButtonPressed)


    self.add_cascade(menu=menu_Filter, label='Filter')
                