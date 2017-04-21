from Tkinter import *
import thread, threading
import time
Tk()
left_str = StringVar()
right_str = StringVar()
front_str = StringVar()
left_str.set('Test')

num = 0

class Application(Frame):
    def print_state(self):
        print "hi there, everyone!"

    def createWidgets(self):
        self.LEFT = Label(self, textvariable = left_str)
        self.LEFT["text"] = "Left Sensor: "
        #self.LEFT.pack({"side": "left"})
        self.LEFT.grid(column=0, row=0)

        self.RIGHT = Label(self, textvariable = right_str)
        self.RIGHT["text"] = "Right Sensor: "
        self.RIGHT.grid(column=0, row=1)

        self.FRONT = Label(self, textvariable = front_str)
        self.FRONT["text"] = "Front Sensor: "
        self.FRONT.grid(column=0, row=2)

        self.PRINT = Button(self)
        self.PRINT["text"] = "Hello",
        self.PRINT["command"] = self.print_state
        self.PRINT.grid(column=0, row=5)

        #self.PRINT.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

def runGUI():
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()

def updateGUI():
    num = 0
    while 1:
        left_str.set(str(num+1))
        right_str = str(num+2)
        front_str = str(num+3)
        num = num + 1
        time.sleep(0.05)

#Test Threading
try:
    thread.start_new_thread(runGUI, ())
    thread.start_new_thread(updateGUI, ())
except:
   print "Thread Error"

while 1:
    pass