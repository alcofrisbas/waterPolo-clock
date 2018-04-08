import threading
import time, sys
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
		self.isUsed = False
		
		self.B = ttk.Button(self.mainFrame, text = "", command = self.toggle)
		self.B.grid(row = 1, column = 0)
		if self.type == "long":
			height = 10
		else:
			height = 5
		self.Box = Text(self.mainFrame, background = self.unused, width = 5, height = height,
					highlightthickness = 0)
		self.Box.grid(row = 0, column = 0, padx = 3)
		
	def toggle(self):
		self.isUsed = not self.isUsed
		if self.isUsed:
			self.Box.config(background = self.used) 
		else:
			self.Box.config(background = self.unused)
		

class Score:
	def __init__(self, master, style):
		self.master = master
		self.style = style
		self.score = 0

		self.theScore = StringVar()
		self.theScore.set(str(self.score))

		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()


		self.s = ttk.Label(self.mainFrame, textvariable=self.theScore, style = self.style)
		self.s.grid(row = 0, column = 0)

		self.buttonFrame = ttk.Frame(self.mainFrame)
		self.buttonFrame.grid(row = 1, column = 0)

		self.plus = ttk.Button(self.buttonFrame, text = "+", command = self.add1)
		self.plus.grid(row = 0, column = 1)

		self.minus = ttk.Button(self.buttonFrame, text = "-", command = self.sub1)
		self.minus.grid(row = 0, column = 0)

	def add1(self):
		self.score += 1
		self.theScore.set(str(self.score))

	def sub1(self):
		self.score -= 1
		self.theScore.set(str(self.score))


class Clock:
	def __init__(self, master, initialTime, style, opts=True):
		self.master = master
	
    	
		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid(sticky=E)
		self.initialTime = initialTime
		self.currentTime = initialTime
		
		self.theTime = StringVar()
		self.theTime.set(self.HMS())
		
		self.display = ttk.Label(self.mainFrame, textvariable = self.theTime,  style = style, width = 6)
		self.display.grid(column = 0, row = 0, columnspan = 1, sticky = E)
		self.display.grid_propagate(0)

		
		self.running = False
		self.initialized = False

		self.lowFrame = ttk.Frame(self.mainFrame)
		self.lowFrame.grid(row = 1, column = 0, sticky=W)

		self.botFrame = ttk.Frame(self.mainFrame)
		self.botFrame.grid(row = 2, column = 0, sticky=W)
				
		self.ppB = ttk.Button(self.lowFrame, text = "Pause Play", command = self.playPause)
		self.ppB.grid(row = 1, column = 0)
		
		self.rB = ttk.Button(self.lowFrame, text = "Reset", command = self.reset)
		self.rB.grid(row = 1, column = 1)

		if opts:
			self.p1B = ttk.Button(self.lowFrame, text = "Plus 1", command = self.add1)
			self.p1B.grid(row = 1, column = 2)

			self.p5B = ttk.Button(self.lowFrame, text = "Plus 5", command = self.add5)
			self.p5B.grid(row = 1, column = 3)

			self.manualB = ttk.Button(self.botFrame, text = "Manually Reconfigure", command = self.reconfigure)
			self.manualB.grid(row = 0, column = 0)

			self.reFrame = ttk.Frame(self.botFrame)
			self.reFrame.grid(row = 0, column = 1)
			
			self.reMin = ttk.Entry(self.reFrame, width=3)
			self.reMin.grid(row = 0, column = 0)

			self.reCO = ttk.Label(self.reFrame, text=":")
			self.reCO.grid(row = 0, column = 1)

			self.reSec = ttk.Entry(self.reFrame, width=3)
			self.reSec.grid(row = 0, column = 2)

		
	def HMS(self):
		m,s = divmod(self.currentTime,60)
		h,m = divmod(m, 60)
		return "%d:%02d" % (m, s)
		
	
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

	def add1(self):
		self.currentTime += 1
		self.theTime.set(self.HMS())

	def add5(self):
		self.currentTime += 5
		self.theTime.set(self.HMS())

	def reconfigure(self):
		timeToSet = 60*int(self.reMin.get()) + int(self.reSec.get())
		self.setClock(timeToSet)
		
		
class MainGui:
	def __init__(self, master):
		self.master = master
		#self.master.minsize(width=666, height=666)
    	#self.master.maxsize(width=666, height=666)
		self.master.title("Water Polo Clock")
		self.s = ttk.Style()
		#self.s.theme_use('default')
		self.s.configure('BigTime.TLabel', background = "black", font = ('TkDefaultFont',150), )
		self.s.configure('Time.TLabel', background = "black", font = ('TkDefaultFont',75), )
		x = self.s.lookup('Time.TLabel', "background")
		print x
		self.s.configure('TOused.TButton', background = "blue")
		self.s.configure('TOunused.TButton', background = "white")
		
		self.mensSeason = True

		self.mainFrame = ttk.Frame(self.master)
		self.mainFrame.grid()
		
		self.upperFrame = ttk.Frame(self.mainFrame)
		self.upperFrame.grid(row = 0, column = 0)
		
		self.lowerFrame = ttk.Frame(self.mainFrame)
		self.lowerFrame.grid(row = 1, column = 0, sticky = W)

		self.bottomFrame = ttk.Frame(self.mainFrame)
		self.bottomFrame.grid(row = 2)
		
		self.quarterFrame = ttk.LabelFrame(self.upperFrame, text = "Quarter")#, width = 250)
		self.quarterFrame.grid(row = 0, column = 0, padx = 2)
		
		self.shotFrame = ttk.LabelFrame(self.upperFrame, text = "Shot Clock")#, width = 250)
		self.shotFrame.grid(row = 0, column = 2, padx = 2)
		
		self.masterFrame = ttk.LabelFrame(self.upperFrame, text = "Master Controls")
		self.masterFrame.grid(row = 0, column = 1, sticky = N)

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
		
		self.masterPP = ttk.Button(self.masterFrame, text = "Play Pause", command = self.masterPlayPause)
		self.masterPP.grid(row = 0)

		self.masterReset = ttk.Button(self.masterFrame, text = "Reset", command = self.masterReset)
		self.masterReset.grid(row = 5)

		self.menWomen = ttk.Button(self.masterFrame, text = "Men", command = self.toggleShotClock)
		self.menWomen.grid(row = 2)

		self.masterAdd1 = ttk.Button(self.masterFrame, text = "Plus 1", command = self.masterAdd1S)
		self.masterAdd1.grid(row = 3)

		self.masterAdd1 = ttk.Button(self.masterFrame, text = "Plus 5", command = self.masterAdd5S)
		self.masterAdd1.grid(row = 4)

		self.masterSPACER = ttk.Label(self.masterFrame, text = "")
		self.masterSPACER.grid(row = 1, column = 0)


		if len(sys.argv) == 3:
			#self.teamFrame = ttk.Frame(self.TOFrame)
			#self.teamFrame.grid(row = 1, column = 0, columnspan = 8)
			
			self.team1 = ttk.Label(self.TOFrame, text = sys.argv[1], style = "Time.TLabel")
			self.team1.grid(row = 1, column = 0, columnspan = 4)
			
			self.team2 = ttk.Label(self.TOFrame, text = sys.argv[2], style = "Time.TLabel")
			self.team2.grid(row = 1, column = 4, columnspan = 4)

			self.score1Frame = ttk.Frame(self.TOFrame)
			self.score1Frame.grid(row = 2, column = 0, columnspan = 4)
			
			self.score1 = Score(self.score1Frame,style="Time.TLabel")

			self.score2Frame = ttk.Frame(self.TOFrame)
			self.score2Frame.grid(row = 2, column = 4, columnspan = 4)
			
			self.score2 = Score(self.score2Frame,style="Time.TLabel")
			#self.score1.grid(row = 2, column = 0)




		TOList = []
		
		for i in range(3):
			f = ttk.Frame(self.TOFrame)
			f.grid(row = 0, column = i)
			TOList.append(TimeOut(f, "long", "blue", "white"))
			
		
		f = ttk.Frame(self.TOFrame)
		f.grid(row = 0, column = 3, sticky = S, padx = (0,20))
		TOList.append(TimeOut(f, "short", "blue", "white"))
		
		f = ttk.Frame(self.TOFrame)
		f.grid(row = 0, column = 4, sticky = S, padx = (20,0))
		TOList.append(TimeOut(f, "short", "blue", "white"))
		
		for i in range(3):
			f = ttk.Frame(self.TOFrame)
			f.grid(row = 0, column = i+5)
			TOList.append(TimeOut(f, "long", "blue", "white"))
		
		self.quarterClock = Clock(self.quarterFrame, 420, "BigTime.TLabel")
		
		self.shotClock = Clock(self.shotFrame, 30, "BigTime.TLabel", opts=True)
		
		self.variousClock = Clock(self.varClockF, 120, "Time.TLabel", opts=False)



		self.quarterClock.reset()
		self.shotClock.reset()

		self.master.bind("g", self.goal)
		#self.master.bind("t", self.turnover)


	
	def masterAdd1S(self):
		self.quarterClock.add1()
		self.shotClock.add1()

	def masterAdd5S(self):
		self.quarterClock.add5()
		self.shotClock.add5()

	def toggleShotClock(self):
		self.mensSeason = not self.mensSeason
		if self.mensSeason:
			self.shotClock.setClock(30)
			self.menWomen.config(text='Men')
		else:
			self.menWomen.config(text='Women')
			self.shotClock.setClock(35)

	def masterPlayPause(self):
		self.quarterClock.playPause()
		self.shotClock.playPause()

	def masterReset(self):
		self.quarterClock.reset()
		self.shotClock.reset()
		
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

	def goal(self, event):
		self.quarterClock.playPause()
		self.shotClock.reset()
	# Faulty Code... Can't get out of this bug...
	# don't use this method
	def turnover(self, event):
		self.shotClock.reset()
		time.sleep(1.01)
		self.replay()
		self.shotClock.playPause()
		
		

def main():
	root = Tk()
	gui = MainGui(root)
	root.mainloop()
	
if __name__ == "__main__":
	main()
