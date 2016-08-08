# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 15:34:22 2016

@author: rohanbali
"""

from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W

class FilterPopup(Toplevel):
    
     def __init__(self,parent,inType):
    
        Toplevel.__init__(self)   
        self.inputDevice = inType
        
        self.transient(parent)
        self.focus()
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (sw/4, sh/4, sw/2-sw/8, sh/2-sh/8))
        self.grab_set()
        self.title("Select Filter")
        self.supportedFilters = []
                
        filterFunctionFiles = self.inputDevice.getAllowedFilterFunctionsName()
        for i in range(len(filterFunctionFiles)):
                fileName = filterFunctionFiles[i]
                components = fileName.split('.')
                fileName = components[0]
                className = fileName[0].upper() + fileName[1:]
                module = __import__("filterConfig."+fileName,fromlist=["filterConfig."])                        
                classVar = getattr(module,className)
                classObject = classVar()
                self.supportedFilters.append(classObject)
                b = Button(self,text=classObject.name,relief=RAISED,command=classObject.filterButtonPressed)
                b.grid(row=i,column=1, sticky=N+S+E+W,padx=2,pady =2)
                self.rowconfigure(i,weight=1)


        self.columnconfigure(1,weight=1)
