import Tkinter as tk
import time, thread

num = 0

class DiagnosticGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Labels
        self.left_label = tk.Label(self, text="Left Sensor:")
        self.left_label.grid(column=0, row=0)

        self.right_label = tk.Label(self, text="Right Sensor:")
        self.right_label.grid(column=0, row=1)

        self.front_label = tk.Label(self, text="Front Sensor:")
        self.front_label.grid(column=0, row=2)

        #Values
        self.left_val = tk.Label(self, text="None")
        self.left_val.grid(column=1, row=0)

        self.right_val = tk.Label(self, text="None")
        self.right_val.grid(column=1, row=1)

        self.front_val = tk.Label(self, text="None")
        self.front_val.grid(column=1, row=2)

        self.update_vals()

    def update_vals(self):
        global num
        left_str = str(num)
        right_str = str(num+1)
        front_str = str(num+2)
        self.left_val.configure(text=left_str)
        self.right_val.configure(text=right_str)
        self.front_val.configure(text=front_str)

        # signals the update after a delay
        self.after(5, self.update_vals)

def runGUI():
    if __name__== "__main__":
        app = DiagnosticGUI()
        app.mainloop()

def updateGUI():
    while 1:
        global num
        num = num + 1
        time.sleep(0.2)

try:
    thread.start_new_thread(runGUI, ())
    thread.start_new_thread(updateGUI, ())
except:
   print "Thread Error"

while 1:
    pass