from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes

import os
import tkinter

class EguanaFigureToolBarTkAgg(NavigationToolbar2TkAgg):
	_toolbar_image_path='plot/toolbarImages/'

	toolitems = (
		('Home', 'Reset original view', 'home', 'home'),
		('Back', 'Back to  previous view', 'back', 'back'),
		('Forward', 'Forward to next view', 'forward', 'forward'),
		(None, None, None, None),
		('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
		('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
		(None, None, None, None),
		('Cursor','Toggle Data Cursor','data_cursor','data_cursor_tool_click'),
		(None, None, None, None),
		#functionality removed since default figure tile do not share axis any more
		#('XzoomIn','Zoom in X','zoom_in_x','zoomXIn_toolclick'),
		#('XzoomOut','Zoom out X','zoom_out_x','zoomXOut_toolclick'),
		(None, None, None, None),
		('Save', 'Save the figure', 'filesave', 'save_figure'),
	)

	data_cursor_style_dict={
		#'animated':True,
		'color':'k',#black
		'linestyle':'dashed'
	}

	approx_min_sqr_distance=400 #in display coordinates
	approx_marker_params={'color':'k','marker':'o','markeredgecolor':'k','markerfacecolor':'None'}
	data_marker_params={'color':'k','marker':'s','markeredgecolor':'k','markerfacecolor':'k'}

	#see http://matplotlib.org/api/patches_api.html#matplotlib.patches.Rectangle
	#see http://matplotlib.org/api/axes_api.html for text(...)
	data_mark_text_bbox={'edgecolor':'k','facecolor':'w'}

	#this value should be less than 1
	zoom_in_factor=0.8

	#class that groups plot data and add-ons
	class plotInfo():
		def __init__(self,axe):
			self.axeHandle=axe
			self.xData=None
			self.yData=None
			for line in axe.get_lines():
				curX=line.get_xdata()
				if self.xData is None or len(curX)>len(self.xData):
					self.xData=curX
					self.yData=line.get_ydata()

			#list of markerInfo
			self.dataMarkerList=[]

			#instance of current data marker (the one responds to moving left/right) in self.dataMarker
			self.curDataMarker=None

	#class that groups data marker data
	class markerInfo():
		def __init__(self,plot,dataIndex):
			self.index=dataIndex
			markDataX=plot.xData[self.index]
			markDataY=plot.yData[self.index]
			self.mark=plot.axeHandle.plot([markDataX,markDataX],[markDataY,markDataY],**EguanaFigureToolBarTkAgg.data_marker_params)
			self.text=None

		def remove(self):
			if self.mark is not None:
				for l in self.mark:
					l.remove()
				self.mark=None
			if self.text is not None:
				self.text.remove()
				self.text=None

	#rewrite the default _Button so that toolbar can load our new button images
	#go to our image folders first
	def _Button(self, text, file, command, extension='.ppm'):
		try:
			img_file = self._toolbar_image_path + file + extension
			im = tkinter.PhotoImage(master=self, file=img_file)
			b = tkinter.Button(master=self, text=text, padx=2, pady=2, image=im, command=command)
			b._ntimage = im
			b.pack(side=tkinter.LEFT)
			return b
		except:
			return NavigationToolbar2TkAgg._Button(self,text,file,command,extension)

	def __init__(self,canvas,frame):
		NavigationToolbar2TkAgg.__init__(self,canvas,frame)

		#data of all plots
		#data of data markers are saved to plots so that their positions get updated more easily during panning/zooming
		self.plotList=[]
		for i, a in enumerate(self.canvas.figure.get_axes()):
			if a.can_pan() and a.can_zoom():
				curplot=EguanaFigureToolBarTkAgg.plotInfo(a)
				if len(curplot.yData)>0:
					self.plotList.append(curplot)

		#set to true when user toggles data marker
		self._data_cursor_toggled=False

		#will get binded when clicking data cursor toggle button
		self._cid_data_cursor_move=None

		#enable moving data cursor left and right
		self._cid_data_cursor_keypress=self.canvas.mpl_connect('key_press_event',self._data_cursor_keypress)
		
		#mouse button click handler for data cursor part
		self._cid_data_cursor_press=self.canvas.mpl_connect('button_press_event',self._data_cursor_buttonpress)

		#cursor horizontal and vertical line instance (Line2D)
		#lines will not show if self._cursorLineEnable is False
		self._cursorLineEnable=False
		self._cursorVerticalLine=None
		self._cursorHorizontalLine=None

		#the following variables describe the Axes the cursor is in
		#they are immediately set to None when cursor moves out that Axes

		#the plot which cursor is in (plotInfo)
		self._currentPlot=None

		#the plot which current data marker is in (plotInfo)
		self._currentMarkerPlot=None

		#candidate point is always in cursorLastAxe
		self._approxMarker=None#list instance, but there should be only one item
		self._approxLastIndex=None
	
	def _clearApproxMarker(self):
		if self._approxMarker is not None:
			for l in self._approxMarker:
				l.remove()
		self._approxMarker=None
		self._approxLastIndex=None
		
	
	def _updateDataMarkerPosition(self,plot,markers):
		#check position of a data marker
		#if changes needed, update it without refresh
		#markers should be a list of markerInfo in the plot

		#for each marker:
		#the dot is always left unmodified (marker constructor is responsible for this)
		#if text is not put then it is created f
		#the text will be placed in the following manner:
			#if the textbox can set data point as lower left point, do this
			#if not enough space on top,

		if markers is None:
			return None

		[borderLL,borderUR]=plot.axeHandle.get_window_extent().get_points()
		display2dataTransform=plot.axeHandle.transData.inverted()
		borderMinX,borderMinY=display2dataTransform.transform(borderLL)
		borderMaxX,borderMaxY=display2dataTransform.transform(borderUR)

		for currentMarker in markers:
			curMarkerDataX=plot.xData[currentMarker.index]
			curMarkerDataY=plot.yData[currentMarker.index]
			if ((curMarkerDataX<=borderMinX)or(curMarkerDataX>=borderMaxX)
					or(curMarkerDataY<=borderMinY)or(curMarkerDataY>=borderMaxY)):
				#the marker is not in visible area
				#if there is a text, delete it
				if currentMarker.text is not None:
					currentMarker.text.remove()
					currentMarker.text=None
			else:
				#draw text first, correct later
				if currentMarker.text is None:
					currentMarker.text=plot.axeHandle.text(
						curMarkerDataX,curMarkerDataY,
						'x=%.2f\ny=%.2f'%(curMarkerDataX,curMarkerDataY),
						#'x='+str(curMarkerDataX)+'\ny='+str(curMarkerDataY),
						bbox=self.data_mark_text_bbox)

				#get position of text and start to correct
				[textLL,textUR]=currentMarker.text.get_window_extent(renderer=self.canvas.renderer).get_points()
				textMinX,textMinY=display2dataTransform.transform(textLL)
				textMaxX,textMaxY=display2dataTransform.transform(textUR)

				#put at top right by default
				xRate=0.1
				yRate=0.2
				#textNewX=(textMaxX-textMinX)/2+curMarkerDataX
				textNewX=(textMaxX-textMinX)*xRate+curMarkerDataX
				textNewY=(textMaxY-textMinY)*yRate+curMarkerDataY
				
				if textMaxX-textMinX+textNewX>=borderMaxX:
					textNewX-=(textMaxX-textMinX)*(1+xRate*2)

				if (textMaxY-textMinY)/2+textNewY>=borderMaxY:
					textNewY-=(textMaxY-textMinY)*(1+yRate*2)

				newCoord=(textNewX,textNewY)
				if newCoord!=currentMarker.text.get_position():
					currentMarker.text.set_position(newCoord)


	def _find_approx_point(self,targetPlot,dataX,dataY,displayX,displayY):
		#return value: index of closest point

		#find x range first
		#starting from the point with closest x
		#explore to both side, stop when x component of distance greater than tolerated value
		
		#find the point with closest x first
		#assume data in self._cursorLastAxeDataX is of the form a[i]=a[0]+i*step
		#dataX=a[0]+i_wanted*step

		#data used to make sure chosen point is inside the visible area
		#from http://matplotlib.org/devel/transformations.html#matplotlib.transforms.Bbox
		[borderLL,borderUR]=targetPlot.axeHandle.get_window_extent().get_points()
		display2dataTransform=targetPlot.axeHandle.transData.inverted()
		borderMinX,borderMinY=display2dataTransform.transform(borderLL)
		borderMaxX,borderMaxY=display2dataTransform.transform(borderUR)

		step=(targetPlot.xData[-1]-targetPlot.xData[0])/(len(targetPlot.xData)-1)
		index_approx=int(round((dataX-targetPlot.xData[0])/step))
		if index_approx<0:
			index_approx=0
		elif index_approx>=len(targetPlot.xData):
			index_approx=len(targetPlot.xData)-1

		if targetPlot.xData[index_approx]<borderMinX or targetPlot.xData[index_approx]>borderMaxX:
			#the starting point is not in visible area when considering x only
			#impossible to have better candidates
			return None

		#test starting point
		iBest=None
		curMinSqrDist=self.approx_min_sqr_distance
		
		curDispX,curDispY=targetPlot.axeHandle.transData.transform(
				(targetPlot.xData[index_approx],
				targetPlot.yData[index_approx])
		)
		curSqrDistX=(curDispX-displayX)**2
		if curSqrDistX>self.approx_min_sqr_distance:
			#impossible to have better candidates
			return None
		if targetPlot.yData[index_approx]>=borderMinY and targetPlot.yData[index_approx]<=borderMaxY:
			#starting point in visible area
			curSqrDist=curSqrDistX+(curDispY-displayY)**2
			if curSqrDist<curMinSqrDist:
				iBest=index_approx
				curMinSqrDist=curSqrDist

		#explore to left
		leftIndex=index_approx-1
		while leftIndex>=0 and targetPlot.xData[leftIndex]>=borderMinX:
			curDispX,curDispY=targetPlot.axeHandle.transData.transform(
					(targetPlot.xData[leftIndex],
					targetPlot.yData[leftIndex])
			)
			curSqrDistX=(curDispX-displayX)**2
			if curSqrDistX>curMinSqrDist:
				break
			if targetPlot.yData[leftIndex]>=borderMinY and targetPlot.yData[leftIndex]<=borderMaxY:
				curSqrDist=curSqrDistX+(curDispY-displayY)**2
				if curSqrDist<curMinSqrDist:
					iBest=leftIndex
					curMinSqrDist=curSqrDist
			leftIndex-=1

		#explore to right
		rightIndex=index_approx+1
		while rightIndex<len(targetPlot.xData) and targetPlot.xData[rightIndex]<=borderMaxX:
			curDispX,curDispY=targetPlot.axeHandle.transData.transform(
					(targetPlot.xData[rightIndex],
					targetPlot.yData[rightIndex])
			)
			curSqrDistX=(curDispX-displayX)**2
			if curSqrDistX>curMinSqrDist:
				break
			if targetPlot.yData[rightIndex]>=borderMinY and targetPlot.yData[rightIndex]<=borderMaxY:
				curSqrDist=curSqrDistX+(curDispY-displayY)**2
				if curSqrDist<curMinSqrDist:
					iBest=rightIndex
					curMinSqrDist=curSqrDist
			rightIndex+=1
		return iBest

	def drag_pan(self, event):
		#overwrite handler in backend_bases.NavigationToolbar2.drag_pan
		#since now panning also need to consider data marker visibility & position
		#currently this is the original code (unmodified)
		for a, ind in self._xypress:
			a.drag_pan(self._button_pressed, event.key, event.x, event.y)
		for plot in self.plotList:
			self._updateDataMarkerPosition(plot,plot.dataMarkerList)
		self.dynamic_update()
	
	#from http://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.MouseEvent
	#event.button: 1:left 2:mid 3:right
	#event.x,event.y in display coordinates
	def _mouse_move_helper(self,event,wantFindApprox=True,tryCursorLine=True):
		currentPlot=None
		for plot in self.plotList:
			if plot.axeHandle.in_axes(event):
				currentPlot=plot
				break
		
		if currentPlot is not None:
			if self._currentPlot is None:
				#entering an axe
				#initial state: all related things are None
				self._currentPlot=currentPlot
				dataX,dataY=self._currentPlot.axeHandle.transData.inverted().transform((event.x,event.y))
				if tryCursorLine and self._cursorLineEnable is True:
					self._cursorVerticalLine=self._currentPlot.axeHandle.axvline(dataX,**self.data_cursor_style_dict)
					self._cursorHorizontalLine=self._currentPlot.axeHandle.axhline(dataY,**self.data_cursor_style_dict)
				if wantFindApprox is True:
					approxIndex=self._find_approx_point(self._currentPlot,dataX,dataY,event.x,event.y)
					if approxIndex is not None:
						self._approxLastIndex=approxIndex
						approxDataX=self._currentPlot.xData[approxIndex]
						approxDataY=self._currentPlot.yData[approxIndex]
						self._approxMarker=self._currentPlot.axeHandle.plot([approxDataX,approxDataX],[approxDataY,approxDataY],**self.approx_marker_params)
				
			else:
				#from an axe to an axe
				if currentPlot is self._currentPlot:
					#moving in the same axe
					#just reset the line coordinates
					display2dataTransform=self._currentPlot.axeHandle.transData.inverted()
					dataX,dataY=display2dataTransform.transform((event.x,event.y))
					if tryCursorLine and self._cursorLineEnable is True:
						if self._cursorHorizontalLine is None:
							self._cursorHorizontalLine=self._currentPlot.axeHandle.axhline(dataY,**self.data_cursor_style_dict)
						else:
							self._cursorHorizontalLine.set_ydata([dataY,dataY])
						
						if self._cursorVerticalLine is None:
							self._cursorVerticalLine=self._currentPlot.axeHandle.axvline(dataX,**self.data_cursor_style_dict)
						else:
							self._cursorVerticalLine.set_xdata([dataX,dataX])
					
					if wantFindApprox is True:
						approxIndex=self._find_approx_point(self._currentPlot,dataX,dataY,event.x,event.y)
						if approxIndex is None:
							self._clearApproxMarker()
						elif self._approxMarker is not None and self._approxLastIndex!=approxIndex:
							self._clearApproxMarker()
							self._approxLastIndex=approxIndex
							approxDataX=self._currentPlot.xData[approxIndex]
							approxDataY=self._currentPlot.yData[approxIndex]
							self._approxMarker=self._currentPlot.axeHandle.plot(
									[approxDataX,approxDataX],
									[approxDataY,approxDataY],
									**self.approx_marker_params)
				else:
					#moving to another axe
					#clean up the old axe
					if self._cursorVerticalLine is not None:
						self._cursorVerticalLine.remove()
						self._cursorVerticalLine=None
					if self._cursorHorizontalLine is not None:
						self._cursorHorizontalLine.remove()
						self._cursorHorizontalLine=None
					self._clearApproxMarker()
					
					#now same as entering a new axe
					self._currentPlot=currentPlot
					dataX,dataY=self._currentPlot.axeHandle.transData.inverted().transform((event.x,event.y))
					if tryCursorLine and self._cursorLineEnable is True:
						self._cursorVerticalLine=self._currentPlot.axeHandle.axvline(dataX,**self.data_cursor_style_dict)
						self._cursorHorizontalLine=self._currentPlot.axeHandle.axhline(dataY,**self.data_cursor_style_dict)
					if wantFindApprox is True:
						approxIndex=self._find_approx_point(self._currentPlot,dataX,dataY,event.x,event.y)
						if approxIndex is not None:
							self._approxLastIndex=approxIndex
							approxDataX=self._currentPlot.xData[approxIndex]
							approxDataY=self._currentPlot.yData[approxIndex]
							self._approxMarker=self._currentPlot.axeHandle.plot([approxDataX,approxDataX],[approxDataY,approxDataY],**self.approx_marker_params)
						
		elif self._currentPlot is not None:
			#exiting an axe
			self._currentPlot=None
			if self._cursorVerticalLine is not None:
				self._cursorVerticalLine.remove()
				self._cursorVerticalLine=None
			if self._cursorHorizontalLine is not None:
				self._cursorHorizontalLine.remove()
				self._cursorHorizontalLine=None
			self._clearApproxMarker()
	
	def data_cursor_move(self,event):
		if event.x is None or event.y is None:
			return None
		self._mouse_move_helper(event,wantFindApprox=True,tryCursorLine=True)
		self.canvas.draw_idle()
	
	def _data_cursor_keypress(self,event):
		#this event is always bound
		if (self._currentMarkerPlot is not None) and (self._currentMarkerPlot.curDataMarker is not None):
			oldIndex=self._currentMarkerPlot.curDataMarker.index
			targetIndex=oldIndex
			if event.key=='left':
				if oldIndex>0:
					targetIndex=oldIndex-1
			elif event.key=='right':
				if oldIndex<len(self._currentMarkerPlot.xData)-1:
					targetIndex=oldIndex+1
			if targetIndex!=oldIndex:
				oldIndex=self._currentMarkerPlot.dataMarkerList.index(self._currentMarkerPlot.curDataMarker)
				self._currentMarkerPlot.curDataMarker.remove()
				self._currentMarkerPlot.curDataMarker=EguanaFigureToolBarTkAgg.markerInfo(self._currentMarkerPlot,targetIndex)
				self._currentMarkerPlot.dataMarkerList[oldIndex]=self._currentMarkerPlot.curDataMarker
				self._updateDataMarkerPosition(self._currentMarkerPlot,[self._currentMarkerPlot.curDataMarker])
				self.canvas.draw_idle()
	
	def _data_cursor_buttonpress(self,event):
		isLeftButtonPress=False
		isRightButtonPress=False
		if event.button==1:
			isLeftButtonPress=True
		elif event.button==3:
			isRightButtonPress=True

		#this event is always bound
		if (isLeftButtonPress or isRightButtonPress) and self._data_cursor_toggled:
			#left mouse press
			self._clearApproxMarker()
			self._mouse_move_helper(event,wantFindApprox=False,tryCursorLine=False)
			dataX,dataY=self._currentPlot.axeHandle.transData.inverted().transform((event.x,event.y))
			approxIndex=self._find_approx_point(self._currentPlot,dataX,dataY,event.x,event.y)
			if approxIndex is not None:
				#left click on a data point without any mark: create a new mark
				#right click on an existing mark: delete this mark
				self._currentMarkerPlot=self._currentPlot
				
				for marker in self._currentMarkerPlot.dataMarkerList:
					if marker.index==approxIndex and isRightButtonPress:
						#make sure it is not "current" mark first
						if self._currentMarkerPlot.curDataMarker is marker:
							#try to find the one closest to this mark and it is the next "current" mark
							if len(self._currentMarkerPlot.dataMarkerList)>1:
								diffX=len(self._currentMarkerPlot.xData)
								for candidate in self._currentMarkerPlot.dataMarkerList:
									if candidate is not marker:
										curDiffX=abs(marker.index-candidate.index)
										if curDiffX<=diffX:
											self._currentMarkerPlot.curDataMarker=candidate
											diffX=curDiffX
							else:
								self._currentMarkerPlot.curDataMarker=None
						marker.remove()
						self._currentMarkerPlot.dataMarkerList.remove(marker)
						approxIndex=None
						break
				
				if approxIndex is not None and isLeftButtonPress:
					self._currentMarkerPlot.dataMarkerList.append(EguanaFigureToolBarTkAgg.markerInfo(self._currentMarkerPlot,approxIndex))
					self._currentMarkerPlot.curDataMarker=self._currentMarkerPlot.dataMarkerList[-1]
					self._updateDataMarkerPosition(self._currentMarkerPlot,[self._currentMarkerPlot.curDataMarker])
			self.canvas.draw_idle()
	
	def data_cursor_tool_click(self):
		if self._cursorVerticalLine is not None:
			self._cursorVerticalLine.remove()
			self._cursorVerticalLine=None
		if self._cursorHorizontalLine is not None:
			self._cursorHorizontalLine.remove()
			self._cursorHorizontalLine=None
		self._clearApproxMarker()

		if self._data_cursor_toggled==True:
			self._cid_data_cursor_move=self.canvas.mpl_disconnect(self._cid_data_cursor_move)
			self._data_cursor_toggled=False
		else:
			self._cid_data_cursor_move=self.canvas.mpl_connect('motion_notify_event',self.data_cursor_move)
			self._data_cursor_toggled=True
