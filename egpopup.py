# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 15:34:22 2016

@author: rohanbali
"""

from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W

class FilterFunctionPopup(Toplevel):
    
    def __init__(self,parent,inType):
    
        Toplevel.__init__(self)   
        self.inputDevice = inType
        self.parent  = parent
        self.transient(parent)
        self.focus()
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (sw/4, sh/4, sw/2-sw/8, sh/2-sh/8))
        self.grab_set()
        self.title("Select Filter Function")
                
        filterFunctionObjects = self.inputDevice.allowedFilterFunctions

        for i in range(len(filterFunctionObjects)):
                classObject = filterFunctionObjects[i]
                b = Button(self,text=classObject.name,relief=RAISED,command=lambda classObject = classObject : self.filterButtonPressed(classObject))
                b.grid(row=i,column=1, sticky=N+S+E+W,padx=2,pady =2)
                self.rowconfigure(i,weight=1)

        self.columnconfigure(1,weight=1)

    def filterButtonPressed(self,filterFunction):
        self.destroy()
        FilterTypePopup(self.parent,filterFunction)


class FilterTypePopup(Toplevel):
    
    def __init__(self,parent,filterFunction):
    
        Toplevel.__init__(self)   
        self.filterFunction = filterFunction
        self.transient(parent)
        self.focus()
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (sw/4, sh/4, sw/2-sw/8, sh/2-sh/8))
        self.grab_set()
        self.title("Select Filter")
                
        headFiltersList = self.filterFunction.headFilters
        jawFiltersList = self.filterFunction.jawFilters

        for i in range(len(headFiltersList)):
                classObject = headFiltersList[i]
                b = Button(self,text=classObject,relief=RAISED,command=None)
                b.grid(row=i,column=1, sticky=N+S+E+W,padx=2,pady =2)
                self.rowconfigure(i,weight=1)

        for i in range(len(headFiltersList)):
                classObject = headFiltersList[i]
                b = Button(self,text=classObject,relief=RAISED,command=None)
                b.grid(row=i,column=2, sticky=N+S+E+W,padx=2,pady =2)

        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
