import tkinter as tk


class SizeDialog(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=300, height=150)
        self.grid_propagate(0)
        self.grid_columnconfigure(1, weight=1)
        self.map_width      = tk.IntVar()
        self.map_width.set(20)
        self.map_height     = tk.IntVar()
        self.map_height.set(20)

        text_label = tk.Label(self, text="Enter the dimension of the room\nyou want to run simulation on")
        text_label.grid(row=0, column=0, columnspan=2, sticky='nsew')
        width_label         = tk.Label(self, text="Width [m] :")
        self.width_scale    = tk.Scale(self, from_=10, to=30, orient=tk.HORIZONTAL, variable=self.map_width)
        height_label        = tk.Label(self, text="Height [m] :")
        self.height_scale   = tk.Scale(self, from_=10, to=30, orient=tk.HORIZONTAL, variable=self.map_height)

        self.ok_button      = tk.Button(self, text="Run Radar Measurement Simulator")
        width_label.grid(row=1, column=0, sticky='w')
        self.width_scale.grid(row=1, column=1, sticky='we')
        height_label.grid(row=2, column=0, sticky='w')
        self.height_scale.grid(row=2, column=1, sticky='we')
        self.ok_button.grid(row=3, column=0, columnspan=2, sticky='nsew')

    def getValues(self):
        return [self.width_scale.get(), self.height_scale.get()]
