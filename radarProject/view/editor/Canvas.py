import tkinter as tk
from Constants import *
import math


class Canvas(tk.Canvas):
    def __init__(self, root):
        tk.Canvas.__init__(self, root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#f0f0f0")
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.map_dim = [0, 0]
        self.PIXEL_PER_METER = 0
        self.pixel_map_dim = [0, 0]
        self.pad = [0, 0]

        #self.colors = ["deep sky blue", "gold", "turquoise", "salmon", "cyan", "tomato", "aquamarine", "maroon", "sea green", "dark violet", "spring green", "olive drab", "khaki",
        #               'goldenrod', "peach puff", "MediumPurple1", "LemonChiffon2", "lavender"]
        self.clusters_colors = []
        self.clusters_list = []
        self.arrows_list = []

        self.TX = None
        self.TX_label = None
        self.RX = None
        self.RX_label = None

    def computePixelRatio(self):
        min_canvas_size = min(CANVAS_WIDTH-100, CANVAS_HEIGHT-100)
        max_map_size = max(self.map_dim[0], self.map_dim[1])
        return min_canvas_size / max_map_size

    def computePixelMapDim(self):
        return [self.PIXEL_PER_METER * self.map_dim[0], self.PIXEL_PER_METER * self.map_dim[1]]

    def computePad(self):
        return [(CANVAS_WIDTH - self.pixel_map_dim[0]) / 2, (CANVAS_HEIGHT - self.pixel_map_dim[1]) / 2]

    def drawMap(self):
        self.create_rectangle(self.pad[0], self.pad[1], self.pad[0]+self.pixel_map_dim[0], self.pad[1]+self.pixel_map_dim[1], fill="white")

        # Legend
        self.create_line(self.pad[0], self.pad[1] - 10, self.pad[0] + self.pixel_map_dim[0], self.pad[1] - 10, fill="gray", arrow=tk.BOTH)
        self.create_line(self.pad[0] - 10, self.pad[1], self.pad[0] - 10, self.pad[1] + self.pixel_map_dim[1], fill="gray", arrow=tk.BOTH)
        width_label = self.create_text(CANVAS_WIDTH / 2, self.pad[1]-20)
        self.itemconfig(width_label, text=str(self.map_dim[0])+" m")
        height_label = self.create_text(self.pad[0] - 30, CANVAS_HEIGHT / 2)
        self.itemconfig(height_label, text=str(self.map_dim[1]) + " m")
        self.update_idletasks()

    def initRadar(self, tx_pos, rx_pos):
        self.TX = self.create_oval(self.pad[0] + tx_pos[0] * self.PIXEL_PER_METER - RADAR_RADIUS_PX,
                                   self.pad[1] + tx_pos[1] * self.PIXEL_PER_METER - RADAR_RADIUS_PX,
                                   self.pad[0] + tx_pos[0] * self.PIXEL_PER_METER + RADAR_RADIUS_PX,
                                   self.pad[1] + tx_pos[1] * self.PIXEL_PER_METER + RADAR_RADIUS_PX,
                                   fill="red")
        self.TX_label = self.create_text(self.pad[0] + (tx_pos[0]) * self.PIXEL_PER_METER,
                                         self.pad[1] + (tx_pos[1]) * self.PIXEL_PER_METER,
                                         text="TX", fill="white")
        self.RX = self.create_oval(self.pad[0] + rx_pos[0] * self.PIXEL_PER_METER - RADAR_RADIUS_PX,
                                   self.pad[1] + rx_pos[1] * self.PIXEL_PER_METER - RADAR_RADIUS_PX,
                                   self.pad[0] + rx_pos[0] * self.PIXEL_PER_METER + RADAR_RADIUS_PX,
                                   self.pad[1] + rx_pos[1] * self.PIXEL_PER_METER + RADAR_RADIUS_PX,
                                   fill="blue")
        self.RX_label = self.create_text(self.pad[0] + (rx_pos[0]) * self.PIXEL_PER_METER,
                                         self.pad[1] + (rx_pos[1]) * self.PIXEL_PER_METER,
                                         text="RX", fill="white")

    def addCluster(self, r, x, y, v, theta, color):

        self.clusters_colors.append(color)
        self.clusters_list.append(self.create_oval(self.pad[0] + (x - r) * self.PIXEL_PER_METER,
                                                   self.pad[1] + (y - r) * self.PIXEL_PER_METER,
                                                   self.pad[0] + (x + r) * self.PIXEL_PER_METER,
                                                   self.pad[1] + (y + r) * self.PIXEL_PER_METER,
                                                   width=2,
                                                   outline=color))
        vx = v*math.cos(theta*math.pi/180) / 3.6
        vy = v*math.sin(theta*math.pi/180) / 3.6
        self.arrows_list.append(self.create_line(self.pad[0] + x * self.PIXEL_PER_METER,
                                                 self.pad[1] + y * self.PIXEL_PER_METER,
                                                 self.pad[0] + (x + vx) * self.PIXEL_PER_METER,
                                                 self.pad[1] + (y + vy) * self.PIXEL_PER_METER,
                                                 width=2,
                                                 fill=color,
                                                 arrow=tk.LAST))

    def removeCluster(self, index):
        self.delete(self.clusters_list[index])
        self.delete(self.arrows_list[index])
        del self.clusters_list[index]
        del self.arrows_list[index]
        del self.clusters_colors[index]
        self.update_idletasks()

    def selectCluster(self, index):
        for item in self.clusters_list:
            self.itemconfig(item, outline=self.clusters_colors[self.clusters_list.index(item)])
            self.itemconfig(item, width=2)
        for item in self.arrows_list:
            self.itemconfig(item, fill=self.clusters_colors[self.arrows_list.index(item)])
        self.itemconfig(self.clusters_list[index], outline="red")
        self.itemconfig(self.clusters_list[index], width=3)
        self.itemconfig(self.arrows_list[index], fill="red")

    def updateClusterSettings(self, r, x, y, v, theta, index):
        self.coords(self.clusters_list[index],
                    self.pad[0] + (x - r) * self.PIXEL_PER_METER,
                    self.pad[1] + (y - r) * self.PIXEL_PER_METER,
                    self.pad[0] + (x + r) * self.PIXEL_PER_METER,
                    self.pad[1] + (y + r) * self.PIXEL_PER_METER)

        vx = v*math.cos(theta*math.pi/180) / 3.6
        vy = v*math.sin(theta*math.pi/180) / 3.6

        self.coords(self.arrows_list[index],
                    self.pad[0] + x * self.PIXEL_PER_METER,
                    self.pad[1] + y * self.PIXEL_PER_METER,
                    self.pad[0] + (x + vx) * self.PIXEL_PER_METER,
                    self.pad[1] + (y + vy) * self.PIXEL_PER_METER)

    def updateRadarSettings(self, tx_x, tx_y, rx_x, rx_y):
        self.coords(self.TX,
                    self.pad[0] + tx_x*self.PIXEL_PER_METER - RADAR_RADIUS_PX,
                    self.pad[1] + tx_y*self.PIXEL_PER_METER - RADAR_RADIUS_PX,
                    self.pad[0] + tx_x*self.PIXEL_PER_METER + RADAR_RADIUS_PX,
                    self.pad[1] + tx_y*self.PIXEL_PER_METER + RADAR_RADIUS_PX)
        self.coords(self.RX,
                    self.pad[0] + rx_x * self.PIXEL_PER_METER - RADAR_RADIUS_PX,
                    self.pad[1] + rx_y * self.PIXEL_PER_METER - RADAR_RADIUS_PX,
                    self.pad[0] + rx_x * self.PIXEL_PER_METER + RADAR_RADIUS_PX,
                    self.pad[1] + rx_y * self.PIXEL_PER_METER + RADAR_RADIUS_PX)
        self.coords(self.TX_label,
                    self.pad[0] + tx_x * self.PIXEL_PER_METER,
                    self.pad[1] + tx_y * self.PIXEL_PER_METER)
        self.coords(self.RX_label,
                    self.pad[0] + rx_x * self.PIXEL_PER_METER,
                    self.pad[1] + rx_y * self.PIXEL_PER_METER)

    def setMapDim(self, map_dim):
        self.map_dim = map_dim

        self.PIXEL_PER_METER = self.computePixelRatio()
        self.pixel_map_dim = self.computePixelMapDim()
        self.pad = self.computePad()

        self.drawMap()
