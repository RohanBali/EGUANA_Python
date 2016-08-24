# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:15:51 2016

@author: rohanbali
"""
from tkinter import Menu, DISABLED, NORMAL
from tkinter import BooleanVar
from eguanaModel import EguanaModel
from egpopupSettings.settingsPopup import SettingsPopup

class EguanaMenu(Menu):
    
 def __init__(self, parent,delegate):
        Menu.__init__(self, parent)   
        self.parent = parent
        self.delegate = delegate
        self.initUI()
        self.toggleBooleanButtonStates = []
 def initUI(self):
 
    self.menu_file = Menu(self)
    self.menu_file.add_command(label='Load 3D')
    self.menu_file.add_command(label='Load 2D')
    self.menu_file.add_command(label='Settings', command=self.settingsPressed)

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

                menuObj.add_checkbutton(label=filterTypeObj.name, onvalue=1, offvalue=0, variable=buttonBool, command=lambda i=i, headOrJawString = headOrJawString, ffObj = ffObj : self.menuItemSelected(i,headOrJawString,ffObj))
                

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



 def menuItemSelected(self,i,headOrJawString,ffObj):

    
    for key in self.booleanDictionary:
            if key[0] is not ffObj.name:
                booleanList = self.booleanDictionary[(key)]
                for boolVal in booleanList:
                    boolVal.set(False)

    booleanList = self.booleanDictionary[(ffObj.name,headOrJawString)]

    for idx in range(len(booleanList)):
        booleanList[idx].set(False) 

    booleanList[i].set(True)

    selectedHeadFilterName = None
    selectedJawFilterName = None

    for idx in range(len(self.booleanDictionary[(ffObj.name,"Head")])):
        if self.booleanDictionary[(ffObj.name,"Head")][idx].get() == True:
            print('inside head')
            headFilterTypeList = EguanaModel().getAllowedHeadFilterTypesForFilterFunction(ffObj)
            selectedHeadFilterName = headFilterTypeList[idx].name
            break


    for idx in range(len(self.booleanDictionary[(ffObj.name,"Jaw")])):
        if self.booleanDictionary[(ffObj.name,"Jaw")][idx].get() == True:
            print('inside jaw')
            jawFilterTypeList = EguanaModel().getAllowedJawFilterTypesForFilterFunction(ffObj)
            selectedJawFilterName = jawFilterTypeList[idx].name
            break

    if headOrJawString == "Head":
        headFilterTypeList = EguanaModel().getAllowedHeadFilterTypesForFilterFunction(ffObj)
        EguanaModel().filterTypeHead = headFilterTypeList[i]
    else:
        jawFilterTypeList = EguanaModel().getAllowedJawFilterTypesForFilterFunction(ffObj)
        EguanaModel().filterTypeJaw = jawFilterTypeList[i]

    EguanaModel().filterFunction = ffObj

    self.delegate.updateSelectedFilters(ffObj.name,selectedHeadFilterName,selectedJawFilterName)

 def setSelectedFilters(self,ffFilter,ftHeadFilter,ftJawFilter):
    

    for key in self.booleanDictionary:
        if key[0] is not ffFilter.name:
            booleanList = self.booleanDictionary[(key)]
            for boolVal in booleanList:
                boolVal.set(False)


    booleanList = self.booleanDictionary[(ffFilter.name,"Head")]
    headFilterTypeList = EguanaModel().getAllowedHeadFilterTypesForFilterFunction(ffFilter)

    for boolVar in booleanList:
        boolVar.set(False)

    idx = None

    for i in range(len(headFilterTypeList)):
        if headFilterTypeList[i].name == ftHeadFilter.name:
            idx = i
            break


    booleanList[idx].set(True)


    booleanList = self.booleanDictionary[(ffFilter.name,"Jaw")]
    jawFilterTypeList = EguanaModel().getAllowedJawFilterTypesForFilterFunction(ffFilter)

    for boolVar in booleanList:
        boolVar.set(False)

    idx = None

    for i in range(len(jawFilterTypeList)):
        if jawFilterTypeList[i].name == ftJawFilter.name:
            idx = i
            break

    booleanList[idx].set(True)



 def settingsPressed(self):
    settingsPopup = SettingsPopup(self.parent)





                