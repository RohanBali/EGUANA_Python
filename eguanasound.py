import pyaudio
import wave
import threading

#pyaudio Blocking mode from https://people.csail.mit.edu/hubert/pyaudio/docs/

class EguanaPlayer():
	'''EguanaPlayer class: class for audio play
need to bind an EguanaFixedPlayableData Instance first
if you want to change audio source, bind a new one
(the old one will be paused and unbinded)
data will be unbinded when desctucting
'''
	chunkSize=4096
	def __init__(self):
		self.p = pyaudio.PyAudio()
		self.stream=None
		self.soundData=None
		self.frameWidth=0
		self.frameIndex=0
		self.frameRate=0
		self.frameCount=0
		self.frameNumPerStep=0
		self.isPaused=False
		self.isRepeat=False
		self.playingThread=None

	def __play(self):
		isEndOfPlay=False
		dataStartIndex=self.frameIndex*self.frameWidth
		while self.isPaused==False and isEndOfPlay==False:
			dataEndIndex=dataStartIndex+self.chunkSize
			if dataEndIndex<len(self.soundData):
				self.stream.write(self.soundData[dataStartIndex:dataEndIndex])
				self.frameIndex+=self.frameNumPerStep
				dataStartIndex=dataEndIndex
			else:
				self.stream.write(self.soundData[dataStartIndex:])
				self.frameIndex=0
				dataStartIndex=0
				if self.isRepeat==False:
					isEndOfPlay=True

	def __pause(self):
		self.isPaused=True
		if self.playingThread is not None:
			self.playingThread.join()
			self.stream.stop_stream()
			self.playingThread=None

	def __start(self):
		self.__pause()
		self.isPaused=False
		if self.playingThread is None or self.playingThread.is_alive==False:
			self.playingThread=threading.Thread(target=self.__play)
			self.stream.start_stream()
			self.playingThread.start()

	def unbind(self):
		if self.stream is not None:
			if self.playingThread is not None:
				self.pause()
			self.stream.close()
			self.stream=None
			self.soundData=None

	#def __exit__(self, exc_type, exc_val, exc_tb):
	def __del__(self):
		if self.stream is not None:
			self.unbind()

		self.p.terminate()

	def bind(self,EguanaFixedPlayableDataInstance):
		if self.stream is not None:
			self.unbind()

		self.soundData=EguanaFixedPlayableDataInstance.data
		self.stream=self.p.open(format=self.p.get_format_from_width(EguanaFixedPlayableDataInstance.sampWidth),
			channels=EguanaFixedPlayableDataInstance.channelCount,
			rate=EguanaFixedPlayableDataInstance.frameRate,
			output=True,
			start=False)
		self.frameWidth=EguanaFixedPlayableDataInstance.sampWidth*EguanaFixedPlayableDataInstance.channelCount
		self.frameNumPerStep=self.chunkSize//self.frameWidth
		self.frameRate=EguanaFixedPlayableDataInstance.frameRate
		self.frameCount=EguanaFixedPlayableDataInstance.frameCount

	def getFrameNumberFromTime(self,time):
		return max(0,int(time*self.frameRate))

	def setPositionToFrame(self,frameNumber):
		if frameNumber>=self.frameCount or frameNumber<0:
			self.frameIndex=0
		else:
			self.frameIndex=frameNumber

	def playFromStart(self):
		if self.stream is not None:
			self.setPositionToFrame(0)
			self.__start()
	
	def playFromTime(self,time):
		if self.stream is not None:
			self.setPositionToFrame(self.getFrameNumberFromTime(time))
			self.__start()

	def resume(self):
		if self.stream is not None:
			self.__start()

	def stop(self):
		if self.stream is not None:
			self.__pause()
			self.setPositionToFrame(0)

	def pause(self):
		if self.stream is not None:
			self.__pause()

class EguanaFixedPlayableData():
	channelCount=None
	sampWidth=None
	frameRate=None
	frameCount=None
	data=None

	#chunkSize=4096
	def loadWAV(self,path):
		wf=wave.open(path,'rb')

		#info of wav file
		self.channelCount=wf.getnchannels()
		self.sampWidth=wf.getsampwidth()
		self.frameRate=wf.getframerate()
		self.frameCount=wf.getnframes()
		self.data=wf.readframes(-1) #read all frames
		wf.close()

class EguanaRecorder():
	chunkSize=4096

	#all formats supported by pyaudio
	#(width in bytes, pyaudio type constant)
	erFloat32=(4, pyaudio.paFloat32)
	erInt32=(4, pyaudio.paInt32)
	erInt24=(3,pyaudio.paInt24)
	erInt16=(2,pyaudio.paInt16)
	erInt8=(1,pyaudio.paInt8)
	erUInt8=(1,pyaudio.paUInt8)

	def __init__(self):
		self.p = pyaudio.PyAudio()
		self.stream=None
		self.soundData=None
		self.samplingRate=48000
		self.samplingFormat=self.erInt16
		self.channelCount=2
		self.framesPerChunk=self.chunkSize//int(self.samplingFormat[0]*self.channelCount)
		self.isStopped=False
		self.frameCount=0

	def __record_callback(self,in_data,frame_count,time_info,status_flag):
		self.soundData+=in_data
		self.frameCount+=frame_count
		if self.isStopped==False:
			flag=pyaudio.paContinue
		else:
			flag=pyaudio.paComplete
		return (None,flag)

	def startRecording(self, sampRate=48000,sampFormat=(2,pyaudio.paInt16),channelNumber=2):
		if self.stream is None:
			self.samplingRate=sampRate
			self.samplingFormat=sampFormat
			self.channelCount=channelNumber
			self.isStopped=False
			self.frameCount=0
			self.stream=self.p.open(format=self.samplingFormat[1],
				channels=self.channelCount,
				rate=self.samplingRate,
				frames_per_buffer=self.framesPerChunk,
				input=True,
				stream_callback=self.__record_callback,
				start=True)
			self.soundData=b''

	def endRecording(self):
		if self.stream is None:
			return None
		self.isStopped=True
		self.stream.stop_stream()
		self.stream.close()
		self.stream=None

		returnData=EguanaFixedPlayableData()
		returnData.channelCount=self.channelCount
		returnData.sampWidth=self.samplingFormat[0]
		returnData.frameRate=self.samplingRate
		returnData.frameCount=self.frameCount
		returnData.data=self.soundData

		self.soundData=None
		return returnData

def writeWAV(filePath,EguanaFixedPlayableDataInstance):
	wf=wave.open(filePath,'wb')
	wf.setnchannels(EguanaFixedPlayableDataInstance.channelCount)
	wf.setsampwidth(EguanaFixedPlayableDataInstance.sampWidth)
	wf.setframerate(EguanaFixedPlayableDataInstance.frameRate)
	wf.writeframes(EguanaFixedPlayableDataInstance.data)
	wf.close()
