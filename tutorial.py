
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
from tkinter import filedialog, FLAT, PhotoImage, Menu, CENTER, S, NW,NE, SW,W,SE, E, Toplevel
from tkinter import Tk, RIGHT, RAISED, ttk, Frame, Button, Label, Text, TOP,RIDGE, BOTH,BOTTOM, Y,X,W, N, LEFT

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

            dirStr = 'Path : '+dirStr
            
            self.directoryLabel = Label(self.frame, text="No Project Currently Selected",relief=FLAT)
            self.directoryLabel.pack(side=TOP,anchor=N,fill=X,padx=2, pady=2)
            self.directoryLabel.config(text=dirStr)
            
            self.filterButton = Button(self.frame,text="No Filter Selected. Click to select a filter",relief=RAISED,fg='red')
            self.filterButton.pack(side=TOP,anchor=N,fill=X,padx=2, pady=2)
           
            self.showPlotTools()

    def showPlotTools(self):        
        f2= Frame(self.frame, relief=FLAT,bg='#FADC46')
        f2.pack(side=TOP,expand=1,fill=BOTH,padx=10,pady=10)     
        
        b1 = Button(f2,text='3D K',relief=RAISED)
        b1.grid(row=0, column=0,sticky=N+S+E+W,padx=5,pady =5)
        
        b2 = Button(f2,text='3D Dist',relief=RAISED)
        b2.grid(row=0, column=1,sticky=N+S+E+W,padx=5,pady =5)
        
        b3 = Button(f2,text='3D DP',relief=RAISED)
        b3.grid(row=0, column=2,sticky=N+S+E+W,padx=5,pady =5)
        
        b4 = Button(f2,text='2D K',relief=RAISED)
        b4.grid(row=1, column=0,sticky=N+S+E+W,padx=5,pady =5)

        b5 = Button(f2,text='2D Dist',relief=RAISED)
        b5.grid(row=1, column=1,sticky=N+S+E+W,padx=5,pady =5)

        b6 = Button(f2,text='2D DP',relief=RAISED)
        b6.grid(row=1, column=2,sticky=N+S+E+W,padx=5,pady =5)
        
        f2.columnconfigure(0, weight=1)
        f2.columnconfigure(1, weight=1)
        f2.columnconfigure(2, weight=1)

        f2.rowconfigure(0, weight=1)
        f2.rowconfigure(1, weight=1)
        
        self.grab_set()
        
        top = Toplevel()
        top.title("About this application...")

        t = Button(f2,text='2D DP',relief=RAISED)
        t.pack()

        button = Button(top, text="Dismiss", command=top.destroy)
        button.pack()
        

        
    def speech3DButton(self):
        self.filterLabel = Label(self.frame, text="Filter : speech3D ",relief=FLAT)
        self.filterLabel.pack(side=TOP,anchor=N,fill=X,padx=2, pady=2)
        
    def speech2DButton(self):
        self.filterLabel = Label(self.frame, text="Filter : speech2D ",relief=FLAT)
        self.filterLabel.pack(side=TOP,anchor=N,fill=X,padx=2, pady=2)

    def swallow3DButton(self):
        self.filterLabel = Label(self.frame, text="Filter : swallow3D ",relief=FLAT)
        self.filterLabel.pack(side=TOP,anchor=N,fill=X,padx=2, pady=2)

    def swallow2DButton(self):
        self.filterLabel = Label(self.frame, text="Filter : swallow2D ",relief=FLAT)
        self.filterLabel.pack(side=BOTTOM,anchor=N,fill=X,padx=2, pady=2)
    
def main():
  
    root = Tk()
    
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    
    root.geometry('%dx%d+%d+%d' % (sw, sh, 0, 0))

    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()  