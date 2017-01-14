from plot.FigureDrawing import getFigureFrame, getEguanaMachinePlotTileFigure
from plot.NavigationToolbar import EguanaFigureToolBarTkAgg
from random import random
import tkinter

def getSampleFrame_MachinePlotTile(parentFrame):
	#fake data first
	number_of_coils=2
	number_of_channels=3
	sample_rate=2
	
	#three dimentional arrays with index [coil][channel][sample]
	data=[]
	for coilIndex in range(0,number_of_coils):
		data.append([])
		for channelIndex in range(0,number_of_channels):
			data[-1].append([])
			for sampleCount in range(0,30):
				data[-1][-1].append(random())
				
	name_of_channels=['alpha','beta','charlie']
	relevant_channels=[True,False,True]
	
	figureInstance=getEguanaMachinePlotTileFigure(
			number_of_coils,
			number_of_channels,
			sample_rate,
			data,
			name_of_channels,
			relevant_channels
	)
	frameInstance=getFigureFrame(parentFrame,figureInstance,EguanaFigureToolBarTkAgg)
	return frameInstance

root = tkinter.Tk()
root.geometry("550x450+300+300")
sample=getSampleFrame_MachinePlotTile(root)
sample.pack()
root.mainloop()
