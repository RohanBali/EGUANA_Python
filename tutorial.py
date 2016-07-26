
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we use the pack manager
to position two buttons in the
bottom-right corner of the window. 

Author: Jan Bodnar
Last modified: November 2015
Website: www.zetcode.com
"""

from tkinter import filedialog, FLAT, PhotoImage, Menu, CENTER, S, NW,NE, SW,W,SE, E, Toplevel, Entry, messagebox, simpledialog
from tkinter import Tk, RIGHT, RAISED, ttk, Frame, Button, Label, Text, TOP,RIDGE, BOTH,BOTTOM, Y,X,W, N, LEFT

from customDialogs import MyDialog

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()

        
    def initUI(self):
      
        self.parent.title("EGUANA")
        self.style = ttk.Style()        
        self.style.theme_use("alt")        
                
        self.frame = Frame(self, relief=FLAT, borderwidth=10,bg='#FADC46')
        
        self.frame.pack(fill=BOTH, expand=True)        
        self.pack(fill=BOTH, expand=True)
        
        
        self.setupMenuBar()
        self.setupTopBar()  
        
    def setupMenuBar(self):
        self.menubar = Menu(self.parent)
        self.menu_file = Menu(self.menubar)
        self.menu_file.add_command(label='Load 3D',command=self.askDirectory)
        self.menu_file.add_command(label='Load 2D',command=self.askDirectory)
        self.menu_file.add_command(label='Exit',command=self.parent.quit)
        self.menubar.add_cascade(menu=self.menu_file, label='File')

       
        self.menu_Filter = Menu(self.menubar)
        self.menu_Filter.add_command(label='Speech 3D',command=self.speech3DButton)
        self.menu_Filter.add_command(label='Speech 2D',command=self.speech2DButton)
        self.menu_Filter.add_command(label='Swallow 3D',command=self.swallow3DButton)
        self.menu_Filter.add_command(label='Swallow 2D',command=self.swallow2DButton)

        self.menubar.add_cascade(menu=self.menu_Filter, label='Filter')
        
        self.menubar.entryconfigure('Filter', state = 'disabled')

        self.parent.config(menu=self.menubar)
        

    def setupTopBar(self):
        
        self.openButton3D = Button(self.frame,text="Select Directory for 3D EMA",relief=RAISED,command=self.askDirectory)
        self.openButton3D.pack(side=LEFT,anchor=N,fill=BOTH, expand=True,padx=2, pady=2)
        self.openButton2D = Button(self.frame,text="Select Directory for 2D EMA",relief=RAISED,command=self.askDirectory);
        self.openButton2D.pack(side=RIGHT,anchor=N,fill=BOTH, expand=True,padx=2, pady=2)
        
        self.photo = PhotoImage(file="eguana.gif")
        self.photo = self.photo.subsample(2);
        self.photo_label = Label(self.frame,image=self.photo,borderwidth=0,highlightthickness=0)
        self.photo_label.configure(bg='#FADC46')

        self.photo_label.pack(side=BOTTOM,anchor=S,padx=10,pady=10,fill=BOTH, expand=True)        
        self.photo_label.image = self.photo


    def askDirectory(self):

        dirStr = filedialog.askdirectory()
        
        if len(dirStr):
            self.openButton3D.destroy()
            self.openButton2D.destroy()
            self.menubar.entryconfigure('Filter', state = 'active')
            self.photo_label.destroy()

            dirStr = 'Input Path : '+dirStr
            
            self.infoFrame = Frame(self.frame, relief=FLAT, bg='#FADC46')
            self.infoFrame.pack(side=TOP,anchor=N,fill=X,padx=0, pady=0)
            
            self.directoryLabel = Label(self.infoFrame, text="No project currently selected",relief=FLAT)
            self.directoryLabel.grid(row=0,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
            self.directoryLabel.config(text=dirStr)
            
        
            self.outputDirButton = Button(self.infoFrame,text="No output directory selected. Click to select an output directory ",relief=RAISED,fg='red',command=self.askOutputDirectory)
            self.outputDirButton.grid(row=1,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
            
            
            self.filterButton = Button(self.infoFrame,text="No filter selected. Click to select a filter",relief=RAISED,fg='red',command=self.selectFilter)
            self.filterButton.grid(row=2,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
           
           
            self.trialLabel = Label(self.infoFrame,text="Trial Number",relief=FLAT,justify=RIGHT,anchor=E)
            self.trialLabel.grid(row=3,column=0, sticky=N+S+E+W,padx=2,pady =2)



            vcmd = (self.master.register(self.validate),'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
            self.trialEntry = Entry(self.infoFrame,validate = 'key', validatecommand = vcmd)
            self.trialEntry.grid(row=3,column=1, sticky=N+S+E+W,padx=2,pady =2)

            self.infoFrame.columnconfigure(0, weight=1)
            self.infoFrame.columnconfigure(1, weight=1)
            self.infoFrame.rowconfigure(0, weight=1)
            self.infoFrame.rowconfigure(1, weight=1)
            self.infoFrame.rowconfigure(2, weight=1)
            self.infoFrame.rowconfigure(3, weight=1)

            self.showPlotTools()

    def validate(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
                           
        if len(value_if_allowed)==0 : 
            return True
        
        if text in '0123456789.-+ ':
            try:
                float(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return False
            
    def askOutputDirectory(self):
        dirStr = filedialog.askdirectory()
        if len(dirStr):
            dirStr = 'Output Path : '+dirStr
            self.outputDirButton.destroy()
            self.outputDirLabel = Label(self.infoFrame, relief=FLAT)
            self.outputDirLabel.grid(row=1,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
            self.outputDirLabel.config(text=dirStr)

            

    def showPlotTools(self):        
        
        f2= Frame(self.frame, relief=FLAT,bg='#FADC46')
        f2.pack(side=TOP,expand=1,fill=BOTH,padx=10,pady=10)     
        
        b1 = Button(f2,text='3D K',relief=RAISED,command= lambda:self.plotButtonPressed(1))
        b1.grid(row=0, column=0,sticky=N+S+E+W,padx=5,pady =5)
        
        b2 = Button(f2,text='3D Dist',relief=RAISED,command=lambda:self.plotButtonPressed(2))
        b2.grid(row=0, column=1,sticky=N+S+E+W,padx=5,pady =5)
        
        b3 = Button(f2,text='3D DP',relief=RAISED,command=lambda:self.plotButtonPressed(3))
        b3.grid(row=0, column=2,sticky=N+S+E+W,padx=5,pady =5)
        
        b4 = Button(f2,text='2D K',relief=RAISED,command=lambda:self.plotButtonPressed(4))
        b4.grid(row=1, column=0,sticky=N+S+E+W,padx=5,pady =5)

        b5 = Button(f2,text='2D Dist',relief=RAISED,command=lambda:self.plotButtonPressed(5))
        b5.grid(row=1, column=1,sticky=N+S+E+W,padx=5,pady =5)

        b6 = Button(f2,text='2D DP',relief=RAISED,command=lambda:self.plotButtonPressed(6))
        b6.grid(row=1, column=2,sticky=N+S+E+W,padx=5,pady =5)
        
        f2.columnconfigure(0, weight=1)
        f2.columnconfigure(1, weight=1)
        f2.columnconfigure(2, weight=1)

        f2.rowconfigure(0, weight=1)
        f2.rowconfigure(1, weight=1)
       
       
    def plotButtonPressed(self,number):
        trialNum = self.trialEntry.get()
        
        try:
            trialNum = float(trialNum)
            
            
            if trialNum < 16 and trialNum > 0:
                self.plotFigure(number)
                return True             
            else:
                messagebox.showerror(
                    "Trial Number Error",
                    "The trial number is out of range"
                    )     
                return False
        except ValueError:
            messagebox.showerror(
                "Trial Number Error",
                "Error with the trial number"
            )  
            return False
            
    def plotFigure(self,number):
        m =  MyDialog(self.frame)
        if m.isSet():
            print(m.getValues())
        
    def selectFilter(self):
        
        self.top = Toplevel()
        self.top.transient(self)
        self.top.focus()
        
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
    
        self.top.geometry('%dx%d+%d+%d' % (sw/4, sh/4, sw/2-sw/8, sh/2-sh/8))

        self.top.grab_set()

        self.top.title("Select Filter")

        first = Button(self.top,text='Speech 3D',relief=RAISED,command=self.speech3DButton)
        first.pack(side=TOP,expand=1,fill = X,padx=2,pady =2)

        second = Button(self.top,text='Speech 2D',relief=RAISED,command=self.speech2DButton)
        second.pack(side=TOP,expand=1,fill = X,padx=2,pady =2)
        
        third = Button(self.top,text='Sawllow 3D',relief=RAISED,command=self.swallow3DButton)
        third.pack(side=TOP,expand=1,fill = X,padx=2,pady =2)
        
        fourth = Button(self.top,text='Swallow 2D',relief=RAISED,command=self.swallow2DButton)
        fourth.pack(side=TOP,expand=1,fill = X,padx=2,pady =2)
        

    def speech3DButton(self):
        self.top.destroy()
        if hasattr(self, 'filterLabel'):
            self.filterLabel.config(text="Filter : speech3D")
        else:
            self.filterLabel = Label(self.infoFrame, text="Filter : speech3D",relief=FLAT)
            self.filterLabel.grid(row=2,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
            self.filterButton.destroy()
    
    def speech2DButton(self):
        self.top.destroy()
        if hasattr(self, 'filterLabel'):
            self.filterLabel.config(text="Filter : speech2D")
        else:
            self.filterLabel = Label(self.infoFrame, text="Filter : speech2D ",relief=FLAT)
            self.filterLabel.grid(row=2,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
            self.filterButton.destroy()
    
    def swallow3DButton(self):
        self.top.destroy()
        if hasattr(self, 'filterLabel'):
            self.filterLabel.config(text="Filter : swallow3D")
        else:
            self.filterLabel = Label(self.infoFrame, text="Filter : swallow3D ",relief=FLAT)
            self.filterLabel.grid(row=2,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
            self.filterButton.destroy()
    
    def swallow2DButton(self):
        self.top.destroy()
        if hasattr(self, 'filterLabel'):
            self.filterLabel.config(text="Filter : swallow2D")
        else:
            self.filterLabel = Label(self.infoFrame, text="Filter : swallow2D ",relief=FLAT)
            self.filterLabel.grid(row=2,column=0,columnspan=2, sticky=N+S+E+W,padx=2,pady =2)
            self.filterButton.destroy()

def main():
  
    root = Tk()
    
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    
    root.geometry('%dx%d+%d+%d' % (sw, sh, 0, 0))

    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()  