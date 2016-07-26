# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 23:24:40 2016

@author: rohanbali
"""

from tkinter import Tk,simpledialog, Label, Entry, messagebox

class MyDialog(simpledialog.Dialog):

    def body(self, master):
        
        self.results = []
        
        Label(master, text="td:").grid(row=0)
        Label(master, text="tb:").grid(row=1)
        Label(master, text="tt:").grid(row=2)
        Label(master, text="head:").grid(row=3)
        Label(master, text="nose:").grid(row=4)
        Label(master, text="ul:").grid(row=5)
        Label(master, text="ll:").grid(row=6)
        Label(master, text="jaw:").grid(row=7)
        Label(master, text="lc:").grid(row=8)
        Label(master, text="rc:").grid(row=9)
        Label(master, text="l ear:").grid(row=10)
        Label(master, text="r ear:").grid(row=11)


        vcmd = (self.master.register(self.validateEntry),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')


        for i in range(0,12):
            a = Entry(master)
            setattr(self, "e"+str(i),a)
            a.insert(0,i+1)
            a.config(validate='key',validatecommand=vcmd)
            a.grid(row=i,column=1)
        
        return self.e1 # initial focus
    
    def validate(self):

        for i in range(0,12):
            ent = getattr(self,"e"+str(i))
            text = ent.get()
            try:
                if int(text) > 12 or int(text) < 1:
                    messagebox.showerror(
                    "Index out of range!",
                    "Please enter a number between 1 and 12"
                    )  
                    return False
            except ValueError:
                messagebox.showerror(
                    "Value Error",
                    "One of your coils is not a number"
                    )  
                return False
            
        return True

    def validateEntry(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
                           
        if len(value_if_allowed)==0 : 
            return True
        
        if text in '0123456789.-+':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
    
    def apply(self):
        ar = []
        for i in range(0,12):
            ent = getattr(self,"e"+str(i))
            text = ent.get()
            ar.append(text)
        self.results = ar
        
    def isSet(self):
        if len(self.results) == 0:
            return 0
        else:
            return 1
        
    def getValues(self):
        return self.results