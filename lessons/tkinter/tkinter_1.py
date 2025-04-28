import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.name_var=tk.StringVar()
        self.entry = tk.Entry(self, textvariable = self.name_var).grid(row=0,column=0)
        self.quitbutton = tk.Button(self, text="Quit", command=quit).grid(row=1, column=0)
        self.pack()

# create the application
myapp = App()

#
# here are method calls to the window manager class
#
myapp.master.title("My Do-Nothing Application")
myapp.master.maxsize(1000, 400)

# start the program
myapp.mainloop()