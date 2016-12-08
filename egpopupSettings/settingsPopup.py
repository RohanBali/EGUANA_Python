from tkinter import *
from tkinter import Toplevel, RAISED, Button, TOP, X, NORMAL, DISABLED, S, N, E, W, SUNKEN, Label, OptionMenu, BOTH, messagebox
from tkinter.ttk import Notebook

import subprocess
import os.path
import json

from eguanaModel import EguanaModel

from egpopupSettings.addSettingsFrame import AddSettingsFrame
from egpopupSettings.editSettingsFrame import EditSettingsFrame
from egpopupSettings.deleteSettingsFrame import DeleteSettingsFrame

from egpopupSettings.groupDescriptionCheckboxFrame import GroupDescriptionCheckboxFrame

from helpers import jsonHelper

class SettingsPopup(Toplevel):
    
    def __init__(self,parent):
        Toplevel.__init__(self) 
        self.transient(parent)
        self.focus()

        sw = parent.winfo_screenwidth()
        sh = parent.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (sw/2, sh/2, sw/4, sh/4))
        self.grab_set()
        self.title("Settings")

        self.modeNotebook = Notebook(self)
        self.modeNotebook.pack(fill=BOTH, expand=True)

        self.addFrame = AddSettingsFrame(self.modeNotebook, self)
        self.addFrame.pack(fill=BOTH, expand=True)

        self.editFrame = EditSettingsFrame(self.modeNotebook, self)
        self.editFrame.pack(fill=BOTH, expand=True)

        self.deleteFrame = DeleteSettingsFrame(self.modeNotebook, self)
        self.deleteFrame.pack(fill=BOTH, expand=True)

        self.modeNotebook.add(self.addFrame, text='Add')
        self.modeNotebook.add(self.editFrame, text='Edit')
        self.modeNotebook.add(self.deleteFrame, text='Delete')

        self.addFrame.setupFrame()
        self.editFrame.setupFrame()
        
        self.wait_window()