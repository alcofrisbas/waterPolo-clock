import threading
import time
from Tkinter import *
import ttk

class TimeOut:
	def __init__(self, master, type, used, unused):
		self.master = master
		self.used = used
		self.unused = unused
		self.type = type
		self.status = False
		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()
		
		self.B = ttk.Button(self.mainFrame, text = "")
		self.B.grid(row = 0, column = 0)
		

class Clock:
	def __init__(self, master, initialTime, style):
		self.master = master
	
    	
		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()
		self.initialTime = initialTime
		self.currentTime = initialTime
		
		self.theTime = StringVar()
		self.theTime.set(self.HMS())
		
		self.display = ttk.Label(self.mainFrame, textvariable = self.theTime,  style = style, width = 6)
		self.display.grid(column = 0, row = 0, columnspan = 3)
		self.display.grid_propagate(0)

		
		self.running = False
		self.initialized = False
				
		self.ppB = ttk.Button(self.mainFrame, text = "Pause Play", command = self.playPause)
		self.ppB.grid(row = 1, column = 0)
		
		self.rB = ttk.Button(self.mainFrame, text = "Reset", command = self.reset)
		self.rB.grid(row = 1, column = 1)
		
	def HMS(self):
		m,s = divmod(self.currentTime,60)
		h,m = divmod(m, 60)
		return "%d:%02d:%02d" % (h, m, s)
		
	
	def clockWorker(self):
		while self.initialized:
			if self.running:
				self.currentTime-=1
				self.theTime.set(self.HMS())
				#self.master.update_idletasks()
				time.sleep(1)
				if self.currentTime > 0:
					self.clockWorker()
				else:
					break
		self.reset()
	
	def initializeClock(self):
		self.currentTime = self.initialTime
		
		self.initialized = True
		self.running = True
		
		self.t = threading.Thread(target = self.clockWorker)
		self.t.start()
		
	def playPause(self):
		if not self.initialized:
			self.initializeClock()
		else:
			self.running = not self.running
		
		
		
	def reset(self):
		self.initialized = False
		self.running = False
		
		self.currentTime = self.initialTime
		self.theTime.set(self.HMS())
		#self.master.update_idletasks()
		#self.t.join()
	
	def setClock(self, newTime):
		self.initialTime = newTime
		self.reset()
		
class MainGui:
	def __init__(self, master):
		self.master = master
		#self.master.minsize(width=666, height=666)
    	#self.master.maxsize(width=666, height=666)
		
		self.s = ttk.Style()
		self.s.theme_use('default')
		self.s.configure('Time.TLabel', font = ('TkDefaultFont',75))
		
		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()
		
		self.upperFrame = ttk.Frame(self.mainFrame)
		self.upperFrame.grid(row = 0, column = 0)
		
		self.lowerFrame = ttk.Frame(self.mainFrame)
		self.lowerFrame.grid(row = 1, column = 0, sticky = W)
		
		self.quarterFrame = ttk.LabelFrame(self.upperFrame, text = "Quarter", width = 250)
		self.quarterFrame.grid(row = 0, column = 0, padx = 2)
		
		self.shotFrame = ttk.LabelFrame(self.upperFrame, text = "Shot Clock", width = 250)
		self.shotFrame.grid(row = 0, column = 1, padx = 2)
		
		self.variousFrame = ttk.LabelFrame(self.lowerFrame, text = "Various")
		self.variousFrame.grid(row = 0, column = 0, sticky = W)
		
		self.varClockF = ttk.Frame(self.variousFrame)
		self.varClockF.grid(row = 0, column = 0, sticky = W)
		
		self.varClockBF = ttk.Frame(self.variousFrame)
		self.varClockBF.grid(row = 1, column = 0, sticky = W+E, padx = 15, pady = 5)
		
		self.TOFullB = ttk.Button(self.varClockBF, text = "Full TO", command = self.fullTO)
		self.TOFullB.grid(row = 0, column = 0)
		
		self.TOHB = ttk.Button(self.varClockBF, text = "Half TO", command = self.halfTO)
		self.TOHB.grid(row = 0, column = 1, sticky = E, padx = (20,0))
		
		self.HTB = ttk.Button(self.varClockBF, text = "Half Time", command = self.halfTime)
		self.HTB.grid(row = 1, column = 0)
		
		self.QTB = ttk.Button(self.varClockBF, text = "Quarter", command = self.quarterTime)
		self.QTB.grid(row = 1, column = 1, sticky = E)
		
		self.ExB = ttk.Button(self.varClockBF, text = "Exclusion", command = self.exclusion)
		self.ExB.grid(row = 2, column = 0)
		
		self.TOFrame = ttk.LabelFrame(self.lowerFrame, text = "Time outs")
		self.TOFrame.grid(row = 0, column = 1)
		
		self.white1 = TimeOut(self.TOFrame, "long", "TButton", "TButton")
		

		
		self.quarterClock = Clock(self.quarterFrame, 420, "Time.TLabel")
		
		self.shotClock = Clock(self.shotFrame, 35, "Time.TLabel")
		
		self.variousClock = Clock(self.varClockF, 120, "Time.TLabel")
		



		
	def __update_layout(self):
		self.master.update_idletasks()
		self.after(100, self.__update_layout)
		
	def fullTO(self):
		self.variousClock.setClock(120)
		
	def halfTO(self):
		self.variousClock.setClock(30)
	
	def halfTime(self):
		self.variousClock.setClock(300)
	
	def quarterTime(self):
		self.variousClock.setClock(180)
		
	def exclusion(self):
		self.variousClock.setClock(20)
		
		

def main():
	root = Tk()
	gui = MainGui(root)
	root.mainloop()
	
if __name__ == "__main__":
	main()