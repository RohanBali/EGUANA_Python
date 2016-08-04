# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 15:34:22 2016

@author: rohanbali
"""

from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED

class FilterPopup(Toplevel):
    
     def __init__(self, parent,inType):
    
        Toplevel.__init__(self)   
        self.delegate = parent
        self.inputDevice = inType
        
        self.transient(parent)
        self.focus()
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (sw/4, sh/4, sw/2-sw/8, sh/2-sh/8))
        self.grab_set()
        self.title("Select Filter")

        if self.inputDevice.speech3DFilterButtonState == NORMAL : 
            first = Button(self,text='Speech 3D',relief=RAISED,command=self.delegate.speech3DButtonPressed)
            first.pack(side=TOP,expand=1,fill = X,padx=2,pady =2)
        if self.inputDevice.swallow3DFilterButtonState == NORMAL : 
            third = Button(self,text='Sawllow 3D',relief=RAISED,command=self.delegate.swallow3DButtonPressed)
            third.pack(side=TOP,expand=1,fill = X,padx=2,pady =2)
        if self.inputDevice.speech2DFilterButtonState == NORMAL : 
            second = Button(self,text='Speech 2D',relief=RAISED,command=self.delegate.speech2DButtonPressed)
            second.pack(side=TOP,expand=1,fill = X,padx=2,pady =2)
        if self.inputDevice.swallow2DFilterButtonState == NORMAL : 
            fourth = Button(self,text='Swallow 2D',relief=RAISED,command=self.delegate.swallow2DButtonPressed)
            fourth.pack(side=TOP,expand=1,fill = X,padx=2,pady =2)
