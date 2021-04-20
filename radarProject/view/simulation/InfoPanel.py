import tkinter as tk
from tkinter import ttk


class InfoPanel(tk.LabelFrame):
    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text="Informations :")
        self.nbpoints = tk.IntVar(value=0)
        self.estnbpoints = tk.IntVar(value=0)
        self.no_leak_est = tk.IntVar(value=0)
        self.totalEst   = tk.IntVar(value=0)
        self.noLeakTotalEst = tk.IntVar(value=0)

        tk.Label(self, text="Number of points : ").grid(row=0, column=0, sticky=tk.W)
        tk.Label(self, textvariable=self.nbpoints).grid(row=0, column=1)

        tk.Label(self, text="No Leak Est. Nb of points: ").grid(row=1, column=0, sticky=tk.W)
        tk.Label(self, textvariable=self.no_leak_est).grid(row=1, column=1)

        tk.Label(self, text="No Leak Total. Est : ").grid(row=1, column=3, sticky=tk.W)
        tk.Label(self, textvariable=self.noLeakTotalEst).grid(row=1, column=4)

        tk.Label(self, text="Estimate nb of points : ").grid(row=2, column=0, sticky=tk.W)
        tk.Label(self, textvariable=self.estnbpoints).grid(row=2, column=1)

        tk.Label(self, text="Total estimation : ").grid(row=2, column=3, sticky=tk.W)
        tk.Label(self, textvariable=self.totalEst).grid(row=2, column=4)

        ttk.Separator(self, orient=tk.VERTICAL).grid(row=0, column=2, rowspan=8)

    def setNbPoints(self, nb):
        self.nbpoints.set(nb)

    def setEstNbPoints(self, est, no_leak_est):
        self.estnbpoints.set(est)
        self.no_leak_est.set(no_leak_est)
