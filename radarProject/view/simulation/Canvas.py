from Constants import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt


class Canvas(FigureCanvasTkAgg):
    def __init__(self, parent):
        self.fig = plt.figure(figsize=(3, 3))
        self.ax = plt.axes()
        self.fig.set_facecolor("#f0f0f0")
        self.ax.set_aspect('equal', adjustable='box')
        #plt.gca().invert_yaxis()
        FigureCanvasTkAgg.__init__(self, self.fig, master=parent)

        self.TX = None
        self.RX = None
        self.rect = None
        self.background = None

        self.map_dim    = [0, 0]
        self.points     = []

    def setMapDim(self, map_dim):
        self.map_dim = map_dim
        plt.axis([-1, map_dim[0]+1, -1, map_dim[1]+1])
        plt.grid()

    def drawMap(self):
        self.rect = plt.Rectangle((0, 0), self.map_dim[0], self.map_dim[1], fill=False, color='Red')
        self.ax.add_patch(self.rect)
        self.fig.canvas.draw()

    def initPoints(self, pos, color):
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

        for i in range(len(pos)):
            c = plt.Circle((pos[i][0], pos[i][1]), radius=PERSON_DIAMETER/2, color=color[i])
            self.points.append(c)
            self.ax.add_artist(c)
        self.fig.canvas.draw()

    def initRadar(self, tx_pos, rx_pos):
        self.TX = plt.Circle((tx_pos[0], tx_pos[1]), radius=RADAR_RADIUS, fill=True, color='red')
        self.RX = plt.Circle((rx_pos[0], rx_pos[1]), radius=RADAR_RADIUS, fill=True, color='blue')
        self.ax.add_patch(self.TX)
        self.ax.add_patch(self.RX)
        #plt.show()
        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

    def updatePoints(self, pos):
        self.fig.canvas.restore_region(self.background)
        for i in range(len(pos)):
            self.points[i].set_center(pos[i])
            self.ax.draw_artist(self.points[i])
        self.fig.canvas.blit(self.ax.bbox)

    def clearSimulation(self):
        for point in self.points:
            point.remove()
        self.points.clear()
        self.rect.remove()
        self.RX.remove()
        self.TX.remove()
