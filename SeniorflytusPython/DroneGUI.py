import Tkinter as tk
import time, thread
import Ultrasonic
import FlightControl

num = 0

class DiagnosticGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Labels
        self.left_label = tk.Label(self, text="Left Sensor:")
        self.left_label.grid(column=0, row=0, sticky="e")

        self.right_label = tk.Label(self, text="Right Sensor:")
        self.right_label.grid(column=0, row=1, sticky="e")

        self.front_label = tk.Label(self, text="Front Sensor:")
        self.front_label.grid(column=0, row=2, sticky="e")

        self.state_label = tk.Label(self, text="State:")
        self.state_label.grid(column=0, row=4, sticky="e")

        self.grid_columnconfigure(1, minsize=300)

        #Values
        self.left_val = tk.Label(self, text="None")
        self.left_val.grid(column=1, row=0, sticky="w")

        self.right_val = tk.Label(self, text="None")
        self.right_val.grid(column=1, row=1, sticky="w")

        self.front_val = tk.Label(self, text="None")
        self.front_val.grid(column=1, row=2, sticky="w")

        self.state_val = tk.Label(self, text="None")
        self.state_val.grid(column=1, row=4, sticky="w")

        self.update_vals()

    def update_vals(self):
        self.left_val.configure(text=str(Ultrasonic.left_sensor))
        self.right_val.configure(text=str(Ultrasonic.right_sensor))
        self.front_val.configure(text=str(Ultrasonic.front_sensor))
        self.state_val.configure(text=FlightControl.state)

        # signals the update after a delay
        self.after(5, self.update_vals)

def runGUI():
    #if __name__== "__main__":
    app = DiagnosticGUI()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        app.destroy()

# def updateGUI():
#     while 1:
#         global num
#         num = num + 1
#         time.sleep(0.2)

# try:
#     thread.start_new_thread(runGUI, ())
#     thread.start_new_thread(updateGUI, ())
# except:
#    print "Thread Error"

# while 1:
#     pass