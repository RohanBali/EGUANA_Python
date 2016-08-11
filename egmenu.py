# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:15:51 2016

@author: rohanbali
"""
from tkinter import Menu, DISABLED, NORMAL
from tkinter import BooleanVar
from eguanaModel import EguanaModel

class EguanaMenu(Menu):
    
 def __init__(self, parent,delegate):
        Menu.__init__(self, parent)   
        
        self.delegate = delegate
        self.initUI()
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
        
        
 def inputSelected(self):
    filterFunctionObjects = EguanaModel().getAllowedFilterFunctions()

    menu_Filter = Menu(self)

    filterFunctionMenuObjectsList = []

    self.booleanDictionary = {} 


    for filterFun in filterFunctionObjects:
        mObj = Menu(self)
        filterFunctionMenuObjectsList.append(mObj)
        menu_Filter.add_cascade(menu=mObj,label=filterFun.name)


    for i in range(len(filterFunctionMenuObjectsList)):


        mObj = filterFunctionMenuObjectsList[i]
        ffObj= filterFunctionObjects[i]

        headMenu = Menu(self)
        jawMenu = Menu(self)

        menuList = [headMenu,jawMenu]

        for menuObj in menuList:
            filterTypeList = []
            if menuObj == headMenu:
                filterTypeList = EguanaModel().getAllowedHeadFilterTypesForFilterFunction(ffObj)
            else:
                filterTypeList = EguanaModel().getAllowedJawFilterTypesForFilterFunction(ffObj)

            boolArray = []

            for i in range(len(filterTypeList)):
                filterTypeObj = filterTypeList[i]
                buttonBool = BooleanVar()
                boolArray.append(buttonBool)

                headOrJawString = []

                if menuObj == headMenu:
                    headOrJawString = "Head"
                else:
                    headOrJawString = "Jaw"

                menuObj.add_checkbutton(label=filterTypeObj.name, onvalue=1, offvalue=0, variable=buttonBool, command=lambda i=i, headOrJawString = headOrJawString, ffName = ffObj.name : self.menuItemSelected(i,headOrJawString,ffName))
                

            if menuObj == headMenu:  
                self.booleanDictionary[(ffObj.name,"Head")] = boolArray
            else:
                self.booleanDictionary[(ffObj.name,"Jaw")] = boolArray

        mObj.add_cascade(label="Head",menu=headMenu)
        mObj.add_cascade(label="Jaw",menu=jawMenu)


    # for i in range(len(filterFunctionObjects)):
    #     classObject = filterFunctionObjects[i]        
    #     buttonBool = BooleanVar()
    #     self.toggleBooleanButtonStates.append(buttonBool)

    self.add_cascade(menu=menu_Filter, label='Filter')



 def menuItemSelected(self,i,headOrJawString,ffName):
    booleanList = self.booleanDictionary[(ffName,headOrJawString)]

    for idx in range(len(booleanList)):
        booleanList[idx].set(False) 

    booleanList[i].set(True)





                