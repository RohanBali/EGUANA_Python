from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy
import tkinter

def getFigureFrame(parent,figure,toolbarType):
	mainFrame=tkinter.Frame(parent)
	figureFrame=tkinter.Frame(mainFrame)
	toolbarFrame=tkinter.Frame(mainFrame)

	canvas=FigureCanvasTkAgg(figure, master=figureFrame)
	canvas.show()
	toolbar=toolbarType(canvas,toolbarFrame)
	toolbar.update()
	canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
		
	toolbarFrame.pack(side=tkinter.BOTTOM, fill=tkinter.X, expand=False)
	figureFrame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
	return mainFrame

def getSiglePlotFigure(dataX,dataY,title=None,xLabel=None,yLabel=None):
	figure=Figure()
	subplot=figure.add_subplot(1,1,1)
	subplot.plot(dataX,dataY)
	if title is not None:
		subplot.set_title(title)
	if xLabel is not None:
		subplot.set_xlabel(xLabel)
	if yLabel is not None:
		subplot.set_ylabel(yLabel)
	return figure

def getEguanaMachinePlotTileFigure(
	number_of_coils,
	number_of_channels,
	sample_rate,
	data,#three dimentional arrays with index [coil][channel][sample]
	name_of_channels,#sequence of strings
	relevant_channels,#sequence of True/False
	**kwargs#drawing related parameters
):
	
	#drawing related parameters
	channelNameTopPadding=kwargs.get('channelNameTopPadding',0.06)
	coilNameLeftPadding=kwargs.get('coilNameLeftPadding',0.06)
	rightPadding=kwargs.get('rightPadding',0.05)
	bottomPadding=kwargs.get('bottomPadding',0)
	plotTopPadding=kwargs.get('plotTopPadding',0)
	plotBottomPadding=kwargs.get('plotBottomPadding',0.15)
	plotLeftPadding=kwargs.get('plotLeftPadding',0.15)
	plotRightPadding=kwargs.get('plotRightPadding',0)

	channelNameParams=kwargs.get('channelNameParams',{
		'horizontalalignment':'center',
		'verticalalignment':'center'
	})
	coilNameParams=kwargs.get('coilNameParams',{
		'horizontalalignment':'center',
		'verticalalignment':'center',
		'rotation':'vertical'
	})
	plotParams=kwargs.get('plotParams',{
	})

	#do plots for different coils but same channel share y axis
	channelShareY=kwargs.get('channelShareY',False)

	#do plots for different channels but same coil share x axis
	#this value will be ignored if all plots share x axis
	coilShareX=kwargs.get('coilShareX',False) 

	#do all plots share x axis
	allPlotsShareX=kwargs.get('allPlotsShareX',False)
	if allPlotsShareX==True:
		coilShareX=True

	numberOfRelatedChannels=0
	nameOfRelatedChannels=[]
	drawingData=[]
	for i in range(0,number_of_coils):
		drawingData.append([])
	for i in range(0,number_of_channels):
		if relevant_channels[i] is True:
			nameOfRelatedChannels.append(name_of_channels[i])
			numberOfRelatedChannels+=1
			for j in range(0,number_of_coils):
				drawingData[j].append(data[j][i])

	#rect=l,b,w,h
	rowHeight=(1-channelNameTopPadding-bottomPadding)/number_of_coils
	colWidth=(1-coilNameLeftPadding-rightPadding)/numberOfRelatedChannels
	plotHeight=rowHeight*(1-plotTopPadding-plotBottomPadding)
	plotWidth=colWidth*(1-plotLeftPadding-plotRightPadding)
	plotLeftOffset=colWidth*plotLeftPadding
	plotBottomOffset=rowHeight*plotBottomPadding

	#start to draw figure
	figure=Figure()
	for channelNum in range(0,numberOfRelatedChannels):
		figure.text(
			coilNameLeftPadding+(channelNum+0.5)*colWidth,
			1-channelNameTopPadding/2,
			nameOfRelatedChannels[channelNum],
			**channelNameParams
		)

	for coilNum in range(0,number_of_coils):
		figure.text(coilNameLeftPadding/2,
			(number_of_coils-0.5-coilNum)*rowHeight+bottomPadding,
			'coil '+str(coilNum+1),
			**coilNameParams
		)

	xdata=numpy.arange(0,len(data[0][0])/sample_rate,1.0/sample_rate)
	firstPlotInCoil=[]
	firstPlotInChannel=[]
	for coilNum in range(0,number_of_coils):
		for channelNum in range(0,numberOfRelatedChannels):
			rect=(coilNameLeftPadding+channelNum*colWidth+plotLeftOffset,
				bottomPadding+(number_of_coils-1-coilNum)*rowHeight+plotBottomOffset,
				plotWidth,
				plotHeight
			)
			curPlot=None
			if coilNum==0:
				if coilShareX==True and channelNum>0:
					curPlot=figure.add_axes(rect,sharex=firstPlotInCoil[coilNum])
				else:
					curPlot=figure.add_axes(rect)
			else:
				if channelShareY==True:
					shY=firstPlotInChannel[channelNum]
				else:
					shY=None
				if allPlotsShareX==True:
					shX=firstPlotInCoil[0]
				elif coilShareX==True and channelNum>0:
					shX=firstPlotInCoil[coilNum]
				else:
					shX=None
				curPlot=figure.add_axes(rect,sharex=shX,sharey=shY)
			curPlot.plot(xdata,drawingData[coilNum][channelNum],**plotParams)
			if coilNum==0:
				firstPlotInChannel.append(curPlot)
			if channelNum==0:
				firstPlotInCoil.append(curPlot)

	return figure

