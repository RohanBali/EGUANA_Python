# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 15:34:22 2016

@author: rohanbali
"""

from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label
from eguanaModel import EguanaModel

class FilterFunctionPopup(Toplevel):
    
    def __init__(self,parent):
    
        Toplevel.__init__(self) 
        self.selectedFilter = None  
        self.parent  = parent
        self.transient(parent)
        self.focus()
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (sw/4, sh/4, sw/2-sw/8, sh/2-sh/8))
        self.grab_set()
        self.title("Select Filter Function")
                
        filterFunctionObjects = EguanaModel().getAllowedFilterFunctions()

        for i in range(len(filterFunctionObjects)):
                classObject = filterFunctionObjects[i]
                b = Button(self,text=classObject.name,relief=RAISED,command=lambda classObject = classObject : self.filterButtonPressed(classObject))
                b.grid(row=i,column=1, sticky=N+S+E+W,padx=2,pady =2)
                self.rowconfigure(i,weight=1)

        self.columnconfigure(1,weight=1)
        self.wait_window(self)


    def filterButtonPressed(self,filterFunction):
        self.selectedFilter = filterFunction
        self.destroy()
        # FilterTypePopup(self.parent,filterFunction)


class FilterTypePopup(Toplevel):
    
    def __init__(self,parent,filterFunction):
    
        Toplevel.__init__(self)   
        self.filterFunction = filterFunction
        self.selectedJawFilterType = None
        self.selectedHeadFilterType = None


        self.transient(parent)
        self.focus()
        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (sw/4, sh/4, sw/2-sw/8, sh/2-sh/8))
        self.grab_set()
        self.title("Select Filter")
                
        headFiltersList = EguanaModel().getAllowedHeadFilterTypes()
        jawFiltersList = EguanaModel().getAllowedJawFilterTypes()



        self.jawButtonList = []
        self.headButtonList = []


        headNameLabel = Label(self, text="Head Filter",relief=FLAT)
        headNameLabel.grid(row=0,column=0, sticky=N+S+E+W,padx=2,pady =2)

        jawNameFilter = Label(self, text="Jaw Filter",relief=FLAT)
        jawNameFilter.grid(row=0,column=1, sticky=N+S+E+W,padx=2,pady =2)


        for i in range(len(headFiltersList)):
                classObject = headFiltersList[i]
                b = Button(self,text=classObject.name,relief=RAISED,command=lambda filterTypeObject = classObject, index = i : self.filterTypeButtonPressed(filterTypeObject,index))
                b.grid(row=i+1,column=0, sticky=N+S+E+W,padx=2,pady =2)
                self.headButtonList.append(b)

        for i in range(len(jawFiltersList)):
                classObject = jawFiltersList[i]
                b = Button(self,text=classObject.name,relief=RAISED,command=lambda classObject = classObject, i = i  : self.filterTypeButtonPressed(classObject,i))
                b.grid(row=i+1,column=1, sticky=N+S+E+W,padx=2,pady =2)
                self.jawButtonList.append(b)
                
        for i in range(max(len(jawFiltersList)+1,len(headFiltersList)+1)):
            self.rowconfigure(i,weight=1)        

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.wait_window(self)


    def filterTypeButtonPressed(self,filterTypeObject,index):
        
        if filterTypeObject.filterType == "Head":
            
            for i in range(len(self.headButtonList)):
                b = self.headButtonList[i]
                b.config(fg='black')

            b = self.headButtonList[index]
            b.config(fg='red')

            self.selectedHeadFilterType = filterTypeObject
            if self.selectedJawFilterType is not None:
                self.destroy()

        else:

            for i in range(len(self.jawButtonList)):
                b = self.jawButtonList[i]
                b.config(fg='black')

            b = self.jawButtonList[index]
            b.config(fg='red')

            self.selectedJawFilterType = filterTypeObject

            b = self.jawButtonList[index]
            b.config(fg='red')

            if self.selectedHeadFilterType is not None:
                self.destroy()



