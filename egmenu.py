# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:15:51 2016

@author: rohanbali
"""
from tkinter import Menu, DISABLED, NORMAL
from tkinter import BooleanVar

from constants import InputType

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
    
    self.b0 = BooleanVar()
    self.b1 = BooleanVar()
    self.b2 = BooleanVar()
    self.b3 = BooleanVar()

    self.menu_Filter.add_checkbutton(label="Speech 3D", onvalue=1, offvalue=0, variable=self.b0, command=self.delegate.speech3DButtonPressed)
    self.menu_Filter.add_checkbutton(label='Swallow 3D',onvalue=1, offvalue=0, variable=self.b2,command=self.delegate.swallow3DButtonPressed)
    self.menu_Filter.add_checkbutton(label='Speech 2D',onvalue=1, offvalue=0, variable=self.b1, command=self.delegate.speech2DButtonPressed)    
    self.menu_Filter.add_checkbutton(label='Swallow 2D',onvalue=1, offvalue=0, variable=self.b3,command=self.delegate.swallow2DButtonPressed)

    self.add_cascade(menu=self.menu_Filter, label='Filter')
    
    self.entryconfigure('Filter', state = 'disabled')
    
    
    
 def filterSelected(self,buttonIndex):
     for i in range(4):
         if not i == buttonIndex:
             b = getattr(self,'b'+str(i))
             b.set(False)
        
        
 def inputSelected(self,inType):
     self.entryconfigure('Filter', state = 'active')
     
     if inType == InputType.threeDEma:
         self.menu_Filter.entryconfig(0, state=NORMAL)
         self.menu_Filter.entryconfig(1, state=NORMAL)
         self.menu_Filter.entryconfig(2, state=DISABLED)
         self.menu_Filter.entryconfig(3, state=DISABLED)
     else:
         
         self.menu_Filter.entryconfig(0, state=DISABLED)
         self.menu_Filter.entryconfig(1, state=DISABLED)
         self.menu_Filter.entryconfig(2, state=NORMAL)
         self.menu_Filter.entryconfig(3, state=NORMAL)
