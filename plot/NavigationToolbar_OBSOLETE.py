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
		('CursorErase','Clear Data Marker','data_cursor','clear_cursorDataMarker_tool_click'),
		(None, None, None, None),
		('XzoomIn','Zoom in X','zoom_in_x','zoomXIn_toolclick'),
		('XzoomOut','Zoom out X','zoom_out_x','zoomXOut_toolclick'),
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

	#rewrite the default _Button so that toolbar can load our new button images
	def _Button(self, text, file, command, extension='.ppm'):
		try:
			return NavigationToolbar2TkAgg._Button(self,text,file,command,extension)
		except:
			img_file = self._toolbar_image_path + file + extension
			im = tkinter.PhotoImage(master=self, file=img_file)
			b = tkinter.Button(master=self, text=text, padx=2, pady=2, image=im, command=command)
			b._ntimage = im
			b.pack(side=tkinter.LEFT)
			return b

	def __init__(self,canvas,frame):
		NavigationToolbar2TkAgg.__init__(self,canvas,frame)
		self._data_cursor_toggled=False

		#these two will get binded when clicking data cursor toggle button
		self._cid_data_cursor_move=None
		self._cid_data_cursor_press=None

		#enable moving data cursor left and right
		self._cid_data_cursor_keypress=self.canvas.mpl_connect('key_press_event',self._data_cursor_keypress)

		#cursor horizontal and vertical line instance (Line2D)
		self._cursorVerticalLine=None
		self._cursorHorizontalLine=None

		#the following variables describe the Axes the cursor is in
		#they are immediately set to None when cursor moves out that Axes

		#the axes which cursor is in (Axes)
		self._cursorLastAxe=None

		#transform from display coordinate to data coordinate
		#will be refreshed when moving in a plot so that it can work during panning/zooming
		self._cursorLastTransform=None

		#list of x,y values
		self._cursorLastAxeDataX=None
		self._cursorLastAxeDataY=None

		#candidate point is always in cursorLastAxe
		self._cursorApproxMarker=None#list instance, but there should be only one item
		self._cursorApproxLastIndex=None

		#marked point may not be in the Axes where cursor is in
		self._cursorDataMarkerAxe=None
		self._cursorDataMarker=None
		self._cursorDataMarkerIndex=None
		self._cursorDataMarkerAxeDataX=None
		self._cursorDataMarkerAxeDataY=None

	###########################################################################################
	#functionalities for data cursor
	def _clear_cursorApproxMarker(self):
		if self._cursorApproxMarker is not None:
			for l in self._cursorApproxMarker:
				l.remove()
		self._cursorApproxMarker=None
		self._cursorApproxLastIndex=None

	def _clear_cursorDataMarker(self):
		if self._cursorDataMarker is not None:
			for l in self._cursorDataMarker:
				l.remove()
		self._cursorDataMarkerAxe=None
		self._cursorDataMarker=None
		self._cursorDataMarkerIndex=None
		self._cursorDataMarkerAxeDataX=None
		self._cursorDataMarkerAxeDataY=None

	def _set_cursorDataMarker(self,index):
		#function to move data cursor in the same plot
		#switching plot preparation should be done in press event handler
		#(assume that _cursorDataMarkerAxe,_cursorDataMarkerAxeDataX,_cursorDataMarkerAxeDataY are correct)
		#also assume that marker is either None or inside the current axe

		#if index invalid then do nothing
		if index>=len(self._cursorDataMarkerAxeDataX) or index<0:
			return None
		#if we can reuse the old marker then do nothing
		if self._cursorDataMarker is not None:
			if self._cursorDataMarkerIndex==index:
				return None
			else:
				#remove the old marker
				for l in self._cursorDataMarker:
					l.remove()
		#create the new marker
		self._cursorDataMarkerIndex=index
		markDataX=self._cursorDataMarkerAxeDataX[self._cursorDataMarkerIndex]
		markDataY=self._cursorDataMarkerAxeDataY[self._cursorDataMarkerIndex]
		self._cursorDataMarker=self._cursorDataMarkerAxe.plot([markDataX,markDataX],[markDataY,markDataY],**self.data_marker_params)
		markText='x='+str(markDataX)+'\ny='+str(markDataY)
		self._cursorDataMarker.append(self._cursorDataMarkerAxe.text(markDataX,markDataY,markText,bbox=self.data_mark_text_bbox))

	def _find_approx_point(self,dataX,dataY,displayX,displayY):
		#return value: index of closest point

		#find x range first
		#starting from the point with closest x
		#explore to both side, stop when x component of distance greater than tolerated value
		
		#find the point with closest x first
		#assume data in self._cursorLastAxeDataX is of the form a[i]=a[0]+i*step
		#dataX=a[0]+i_wanted*step

		#data used to make sure chosen point is inside the visible area
		#from http://matplotlib.org/devel/transformations.html#matplotlib.transforms.Bbox
		[borderLL,borderUR]=self._cursorLastAxe.get_window_extent().get_points()
		borderMinX,borderMinY=self._cursorLastTransform.transform(borderLL)
		borderMaxX,borderMaxY=self._cursorLastTransform.transform(borderUR)

		step=(self._cursorLastAxeDataX[-1]-self._cursorLastAxeDataX[0])/(len(self._cursorLastAxeDataX)-1)
		index_approx=int(round((dataX-self._cursorLastAxeDataX[0])/step))
		if index_approx<0:
			index_approx=0
		elif index_approx>=len(self._cursorLastAxeDataX):
			index_approx=len(self._cursorLastAxeDataX)-1

		if self._cursorLastAxeDataX[index_approx]<borderMinX or self._cursorLastAxeDataX[index_approx]>borderMaxX:
			#the starting point is not in visible area when considering x only
			#impossible to have better candidates
			return None

		#test starting point
		iBest=None
		curMinSqrDist=self.approx_min_sqr_distance
		
		curDispX,curDispY=self._cursorLastAxe.transData.transform((self._cursorLastAxeDataX[index_approx],self._cursorLastAxeDataY[index_approx]))
		curSqrDistX=(curDispX-displayX)**2
		if curSqrDistX>self.approx_min_sqr_distance:
			#impossible to have better candidates
			return None
		if self._cursorLastAxeDataY[index_approx]>=borderMinY and self._cursorLastAxeDataY[index_approx]<=borderMaxY:
			#starting point in visible area
			curSqrDist=curSqrDistX+(curDispY-displayY)**2
			if curSqrDist<curMinSqrDist:
				iBest=index_approx
				curMinSqrDist=curSqrDist

		#explore to left
		leftIndex=index_approx-1
		while leftIndex>=0 and self._cursorLastAxeDataX[leftIndex]>=borderMinX:
			curDispX,curDispY=self._cursorLastAxe.transData.transform((self._cursorLastAxeDataX[leftIndex],self._cursorLastAxeDataY[leftIndex]))
			curSqrDistX=(curDispX-displayX)**2
			if curSqrDistX>curMinSqrDist:
				break
			if self._cursorLastAxeDataY[leftIndex]>=borderMinY and self._cursorLastAxeDataY[leftIndex]<=borderMaxY:
				curSqrDist=curSqrDistX+(curDispY-displayY)**2
				if curSqrDist<curMinSqrDist:
					iBest=leftIndex
					curMinSqrDist=curSqrDist
			leftIndex-=1

		#explore to right
		rightIndex=index_approx+1
		while rightIndex<len(self._cursorLastAxeDataX) and self._cursorLastAxeDataX[rightIndex]<=borderMaxX:
			curDispX,curDispY=self._cursorLastAxe.transData.transform((self._cursorLastAxeDataX[rightIndex],self._cursorLastAxeDataY[rightIndex]))
			curSqrDistX=(curDispX-displayX)**2
			if curSqrDistX>curMinSqrDist:
				break
			if self._cursorLastAxeDataY[rightIndex]>=borderMinY and self._cursorLastAxeDataY[rightIndex]<=borderMaxY:
				curSqrDist=curSqrDistX+(curDispY-displayY)**2
				if curSqrDist<curMinSqrDist:
					iBest=rightIndex
					curMinSqrDist=curSqrDist
			rightIndex+=1
		return iBest

	def _get_Axe_XY_Data(self):
		self._cursorLastAxeDataX=None
		self._cursorLastAxeDataY=None
		for line in self._cursorLastAxe.get_lines():
			curX=line.get_xdata()
			if self._cursorLastAxeDataX is None or len(curX)>len(self._cursorLastAxeDataX):
				self._cursorLastAxeDataX=curX
				self._cursorLastAxeDataY=line.get_ydata()

	def _data_cursor_move_enter_axe_setting(self,currentAxe,event,isTryingToFindApproxPoint=True):
		self._cursorLastAxe=currentAxe
		self._cursorLastTransform=currentAxe.transData.inverted()
		dataX,dataY=self._cursorLastTransform.transform((event.x,event.y))
		self._cursorVerticalLine=currentAxe.axvline(dataX,**self.data_cursor_style_dict)
		self._cursorHorizontalLine=currentAxe.axhline(dataY,**self.data_cursor_style_dict)
		self._get_Axe_XY_Data()

		if isTryingToFindApproxPoint and self._cursorLastAxeDataX is not None and len(self._cursorLastAxeDataX)>1:
			#try to find a data point close to the mouse
			approxIndex=self._find_approx_point(dataX,dataY,event.x,event.y)
			if approxIndex is not None:
				self._cursorApproxLastIndex=approxIndex
				if (self._cursorLastAxe is not self._cursorDataMarkerAxe) or (self._cursorApproxLastIndex!=self._cursorDataMarkerIndex):
					approxDataX=self._cursorLastAxeDataX[approxIndex]
					approxDataY=self._cursorLastAxeDataY[approxIndex]
					self._cursorApproxMarker=self._cursorLastAxe.plot([approxDataX,approxDataX],[approxDataY,approxDataY],**self.approx_marker_params)
			

	def _data_cursor_move_leave_axe_setting(self):
		self._cursorVerticalLine.remove()
		self._cursorHorizontalLine.remove()
		self._cursorLastAxe=None
		self._cursorLastTransform=None
		self._cursorVerticalLine=None
		self._cursorHorizontalLine=None
		self._cursorLastAxeDataX=None
		self._cursorLastAxeDataY=None
		self._clear_cursorApproxMarker()

	#from http://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.MouseEvent
	#event.button: 1:left 2:mid 3:right
	#event.x,event.y in display coordinates
	def data_cursor_move(self,event):
		#new_code='''
		currentAxe=None
		for i, a in enumerate(self.canvas.figure.get_axes()):
			if (event.x is not None and event.y is not None and a.in_axes(event)):
				currentAxe=a
				break

		if currentAxe is not None:
			if self._cursorLastAxe is None:
				#entering an axe
				#initial state: all related things are None
				self._data_cursor_move_enter_axe_setting(currentAxe,event,True)
				
			else:
				#from an axe to an axe
				if currentAxe is self._cursorLastAxe:
					#moving in the same axe
					#just reset the line coordinates
					self._cursorLastTransform=self._cursorLastAxe.transData.inverted()
					dataX,dataY=self._cursorLastTransform.transform((event.x,event.y))
					self._cursorVerticalLine.set_xdata([dataX,dataX])
					self._cursorHorizontalLine.set_ydata([dataY,dataY])
					approxIndex=self._find_approx_point(dataX,dataY,event.x,event.y)

					if approxIndex is None:
						self._clear_cursorApproxMarker()

					elif self._cursorApproxLastIndex!=approxIndex:
						if self._cursorApproxMarker is not None:
							self._clear_cursorApproxMarker()

						self._cursorApproxLastIndex=approxIndex
						if (self._cursorLastAxe is not self._cursorDataMarkerAxe
							)or(self._cursorApproxLastIndex!=self._cursorDataMarkerIndex):

							approxDataX=self._cursorLastAxeDataX[approxIndex]
							approxDataY=self._cursorLastAxeDataY[approxIndex]
							self._cursorApproxMarker=self._cursorLastAxe.plot(
								[approxDataX,approxDataX],
								[approxDataY,approxDataY],
								**self.approx_marker_params)
				else:
					#moving to another axe
					#clean up the old axe
					self._cursorVerticalLine.remove()
					self._cursorVerticalLine=None
					self._cursorHorizontalLine.remove()
					self._cursorHorizontalLine=None
					self._clear_cursorApproxMarker()
					#same as entering a new axe
					self._data_cursor_move_enter_axe_setting(currentAxe,event,True)
		elif self._cursorLastAxe is not None:
			#exiting an axe
			self._data_cursor_move_leave_axe_setting()
		self.canvas.draw_idle()

	
	def data_cursor_press(self,event):
		if event.button!=1:
			return None
		self._clear_cursorApproxMarker()
		currentAxe=None
		for i, a in enumerate(self.canvas.figure.get_axes()):
			if (event.x is not None and event.y is not None and a.in_axes(event)):
				currentAxe=a
				break
		if currentAxe is not None:
			if self._cursorLastAxe is not currentAxe:
				self._data_cursor_move_leave_axe_setting()
				self._data_cursor_move_enter_axe_setting(currentAxe,event,False)
			dataX,dataY=self._cursorLastTransform.transform((event.x,event.y))
			currentIndex=self._find_approx_point(dataX,dataY,event.x,event.y)
			self._cursorApproxLastIndex=currentIndex
			if currentIndex is not None:
				#start to update mark
				#set correct axe and data first
				if (self._cursorDataMarker is None)or(self._cursorDataMarkerAxe is not currentAxe):
					self._cursorDataMarkerAxe=currentAxe
					self._cursorDataMarkerAxeDataX=self._cursorLastAxeDataX
					self._cursorDataMarkerAxeDataY=self._cursorLastAxeDataY
					if self._cursorDataMarker is not None:
						for l in self._cursorDataMarker:
							l.remove()
						self._cursorDataMarker=None
				#other checks are in this function
				self._set_cursorDataMarker(currentIndex)					
		self.canvas.draw_idle()

	def _data_cursor_keypress(self,event):
		if event.key=='left':
			if self._cursorDataMarker is not None:
				self._set_cursorDataMarker(self._cursorDataMarkerIndex-1)
				self.canvas.draw_idle()
		elif event.key=='right':
			if self._cursorDataMarker is not None:
				self._set_cursorDataMarker(self._cursorDataMarkerIndex+1)
				self.canvas.draw_idle()
	def data_cursor_tool_click(self):
		#called when button is pressed
		#when cursor is previously not toggled:
		#	bind event (move,click(press))
		##	set cursor to crosshair
		#when cursor is already toggled:
		#	unbind event
		##	restore cursor

		#preparation
		self._cursorLastAxe=None
		self._cursorLastTransform=None
		self._cursorLastAxeDataX=None
		self._cursorLastAxeDataY=None
		if self._cursorVerticalLine is not None:
			self._cursorVerticalLine.remove()
			self._cursorVerticalLine=None
		if self._cursorHorizontalLine is not None:
			self._cursorHorizontalLine.remove()
			self._cursorHorizontalLine=None
		self._clear_cursorApproxMarker()

		#main work
		if self._data_cursor_toggled==True:
			self._cid_data_cursor_move=self.canvas.mpl_disconnect(self._cid_data_cursor_move)
			self._cid_data_cursor_press=self.canvas.mpl_disconnect(self._cid_data_cursor_press)
			self._data_cursor_toggled=False
		else:
			self._cid_data_cursor_move=self.canvas.mpl_connect('motion_notify_event',self.data_cursor_move)
			self._cid_data_cursor_press=self.canvas.mpl_connect('button_press_event',self.data_cursor_press)
			self._data_cursor_toggled=True

	def clear_cursorDataMarker_tool_click(self):
		self._clear_cursorDataMarker()
		self.canvas.draw_idle()

	###########################################################################################
	#functions for zooming x
	def zoomX(self,ratio):
		#reference: matplotlib.backend_bases.NavigationToolbar2.release_zoom
		#zoom all plots in x direction
		#will avoid duplicated zooming for plots sharing x axis
		#keep the center the same and change two bounds accordingly
		zoomed_axes=[]
		for i, currentAxe in enumerate(self.canvas.figure.get_axes()):
			if currentAxe.can_zoom():
				twinx=False
				if zoomed_axes:
					for la in zoomed_axes:
						if currentAxe.get_shared_x_axes().joined(currentAxe, la):
							twinx = True
							break
				zoomed_axes.append(currentAxe)
				if twinx==False:
					[left,right]=currentAxe.get_xlim()
					mid=(left+right)/2
					halfspan=(right-mid)*ratio
					currentAxe.set_xlim(mid-halfspan,mid+halfspan)
	def zoomXIn_toolclick(self):
		self.zoomX(self.zoom_in_factor)
		self.canvas.draw_idle()
	def zoomXOut_toolclick(self):
		self.zoomX(1/self.zoom_in_factor)
		self.canvas.draw_idle()
