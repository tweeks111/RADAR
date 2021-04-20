import tkinter as tk
import view.simulation
from tkinter import ttk


class Window(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.resizable(False, False)
        self.title("Simulation")

        self.map_dim = [0, 0]

        self.left_frame = tk.Frame(self)
        self.map_frame = tk.LabelFrame(self.left_frame, text="Clusters :")
        self.map_frame.pack(side=tk.TOP, expand=False)
        self.canvas = view.simulation.Canvas(self.map_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP)
        self.info_panel = view.simulation.InfoPanel(self.left_frame)
        self.info_panel.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.config_frame = tk.Frame(self.map_frame)
        self.config_frame.pack(side=tk.BOTTOM)
        self.play_btn = tk.Button(self.config_frame, text="\u23F8")  # \u25B6
        self.play_btn.pack(side=tk.LEFT)
        self.time_value = tk.DoubleVar()
        self.time_scale = tk.Scale(self.config_frame, from_=0, to=10, variable=self.time_value, orient=tk.HORIZONTAL,
                                   resolution=0.01, length=300)
        self.time_scale.pack(side=tk.LEFT, fill=tk.X)

        separator = ttk.Separator(self, orient='vertical')
        separator.pack(fill=tk.Y)

        self.right_frame = tk.LabelFrame(self, text="Plots :")
        self.right_frame.pack(side=tk.RIGHT)
        self.rdm_canvas = view.simulation.RDMCanvas(self.right_frame)
        self.rdm_canvas.get_tk_widget().pack(side=tk.LEFT)

    def initSimulation(self, pos_list, color_list, tx_pos, rx_pos, x, y, z, dmap, AoA):
        self.canvas.drawMap()
        self.initRadar(tx_pos, rx_pos)
        self.canvas.initPoints(pos_list, color_list)
        self.rdm_canvas.initRDM(x, y, z, dmap, AoA)

    def updateSimulation(self, pos_list):
        self.canvas.updatePoints(pos_list)

    def closeSimulation(self):
        self.canvas.clearSimulation()
        self.rdm_canvas.clearRDM()

    def initRadar(self, tx_pos, rx_pos):
        self.canvas.initRadar(tx_pos, rx_pos)

    def clearSimulation(self):
        self.canvas.clearSimulation()
        self.rdm_canvas.clearRDM()

    def plotRDM(self, z, dmap, AoA, est, no_leak_est):
        self.rdm_canvas.updateRDM(z, dmap, AoA)
        self.info_panel.setEstNbPoints(est, no_leak_est)

    # -- Set Functions -- #

    def setMapDim(self, map_dim):
        self.map_dim = map_dim
        self.canvas.setMapDim(map_dim)

    def setScaleLength(self, value):
        self.time_scale.configure(from_=0, to=value)

    def setScaleValue(self, value):
        self.time_value.set(value)

    def setNbPoints(self, nb):
        self.info_panel.setNbPoints(nb)

    def setEstNbpoints(self, est):
        self.info_panel.setEstNbPoints(est)