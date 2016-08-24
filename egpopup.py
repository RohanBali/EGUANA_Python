# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 15:34:22 2016

@author: rohanbali
"""

from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu
from tkinter.ttk import Notebook
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

# class SettingsPopup(Toplevel):

#     def __init__(self,parent):
    
#         Toplevel.__init__(self) 
#         self.transient(parent)
#         self.focus()

#         sw = parent.winfo_screenwidth()
#         sh = parent.winfo_screenheight()
#         self.geometry('%dx%d+%d+%d' % (sw/4, sh/4, sw/2-sw/8, sh/2-sh/8))
#         self.grab_set()
#         self.title("Settings")

#         self.modeNotebook = Notebook(self)
#         self.modeNotebook.pack(fill=BOTH, expand=True)

#         self.addFrame = Frame(self.modeNotebook)
#         self.addFrame.pack(fill=BOTH, expand=True)

#         self.editFrame = Frame(self.modeNotebook)
#         self.editFrame.pack(fill=BOTH, expand=True)

#         self.modeNotebook.add(self.addFrame, text='Add')
#         self.modeNotebook.add(self.editFrame, text='Edit')
         
                
#         dropList = ['Machine', 'Filter Function', 'Filter Type']
#         dropTitle = StringVar()
#         dropTitle.set('Select Type')
#         drop = OptionMenu(self.addFrame,dropTitle,*dropList, command=self.selectTypeCallback)
#         drop.grid(row=1, column=0, columnspan=4, sticky='ew')
        

#         self.addFrame.rowconfigure(0,weight=1)
#         self.addFrame.rowconfigure(1,weight=1)
#         self.addFrame.rowconfigure(2,weight=1)
#         self.addFrame.rowconfigure(3,weight=1)
#         self.addFrame.columnconfigure(0,weight=1)
#         self.addFrame.columnconfigure(1,weight=1)
#         self.addFrame.columnconfigure(2,weight=1)
#         self.addFrame.columnconfigure(3,weight=1)
#         self.addFrame.wait_window(self)

#     def selectTypeCallback(self, value):

#         if value == 'Machine':
#             loadButton = Button(self.addFrame, text='Load config file', relief=RAISED, command= lambda : self.machineLoadButtonPressed(loadButton))
#             loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)


#         elif value == 'Filter Function':
#             loadButton = Button(self, text='Load config file', relief=RAISED, command=self.loadButtonPressed)
#             loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)


#         else: #'Filter Type'
#             loadButton = Button(self, text='Load config file', relief=RAISED, command=self.loadButtonPressed)
#             loadButton.grid(row=2, column=0, columnspan=4, sticky=E+W)



#     def machineLoadButtonPressed(self, loadButton):
#         print(loadButton.cget('text'))

#         filePath = filedialog.askopenfilename()
        
#         if filePath != '':
            
#             loadButton.config(text=filePath)

#             filterFunctionNotebook = Notebook(self.addFrame)
#             filterFunctionNotebook.grid(row=3, column=0,columnspan=4, sticky=E+W)
            
#             dropList = EguanaModel().getAllFilterFunctions()

#             for i in range(len(dropList)):

#                 filterFunctionFrame = Frame(filterFunctionNotebook)
#                 filterFunctionFrame.pack(fill=BOTH, expand=True)
#                 filterFunctionNotebook.add(filterFunctionFrame, text=EguanaModel().getFilterObjectFromFunctionName(dropList[i]).name)
#                 self.generateFilterTypesCheckboxesForFilterFunction(filterFunctionFrame)
              

#     def generateFilterTypesCheckboxesForFilterFunction(self, frame):
        
#         checkBoxVar1 = IntVar()
#         Checkbutton(frame, text='Enabled', variable=checkBoxVar1).grid(row=0, column=0, columnspan=2, sticky=N+E)

#         headList = EguanaModel().getAllHeadFilterTypes()
#         modifiedHeadList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(headList,'Head')

#         jawList = EguanaModel().getAllJawFilterTypes()
#         modifiedJawList = EguanaModel().getFilterTypeObjectsFromTypeNameArray(jawList,'Jaw')
        
#         for h in range(len(headList)):
#             checkBoxVar2 = IntVar()
#             Checkbutton(frame, text=modifiedHeadList[h].name, variable=checkBoxVar2).grid(row=1+h, column=0, sticky=W,)

#         for j in range(len(jawList)):
#             checkBoxVar3 = IntVar()
#             Checkbutton(frame, text=modifiedJawList[j].name, variable=checkBoxVar3).grid(row=1+j, column=1, sticky=W)

