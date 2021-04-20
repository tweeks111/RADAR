import math
import numpy as np

####################
# Static Functions #
####################

def lineLength(line):
    return math.sqrt((line[1][0] - line[0][0]) ** 2 + (line[1][1] - line[0][1]) ** 2)


def linesIntersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception("No intersection")

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [x, y]


def vectAngle(vect1, vect2):
    # Using cos(angle) = <a,b> / (||a||.||b||)
    # Normalized vectors
    len_vect1 = lineLength([[0, 0], vect1])
    len_vect2 = lineLength([[0, 0], vect2])

    norm_vect1 = (vect1[0]/len_vect1, vect1[1]/len_vect1)
    norm_vect2 = (vect2[0]/len_vect2, vect2[1]/len_vect2)

    dot_product = norm_vect1[0]*norm_vect2[0] + norm_vect1[1]*norm_vect2[1]
    if dot_product > 1:
        dot_product = 1
    elif dot_product < -1:
        dot_product = -1
    return math.acos(dot_product)


def bisectionVector(vect1, vect2):
    return -(vect1[0]+vect2[0]), -(vect1[1]+vect2[1])

#########
# CLASS #
#########

class Point:

    def __init__(self, x, y, speed, direction, wavelength, color):
        # Point(x, y)
        self.x = x
        self.y = y

        self.speed = speed
        self.v = [speed * math.cos(direction), speed * math.sin(direction)]

        self.wavelength = wavelength

        self.color = color

    def computeParameters(self, tx_pos, rx_pos):
        TX_point_line = [[tx_pos[0], tx_pos[1]], [self.x, self.y]]
        RX_point_line = [[rx_pos[0], rx_pos[1]], [self.x, self.y]]
        d_tx = lineLength(TX_point_line)
        d_rx = lineLength(RX_point_line)

        vect_TX_point = (TX_point_line[1][0]-TX_point_line[0][0], TX_point_line[1][1]-TX_point_line[0][1])
        vect_RX_point = (RX_point_line[1][0]-RX_point_line[0][0],  RX_point_line[1][1]-RX_point_line[0][1])
        xi = vectAngle(vect_TX_point, vect_RX_point)

        bisVect = bisectionVector(vect_TX_point, vect_RX_point)
        theta = vectAngle(bisVect, self.v)
        # TODO : maybe change the vectAngle function and use arctan2 instead
        #print(math.cos(theta)*math.cos(xi/2))   # percentage of f_doppler taken into account

        doppler_freq = 2*self.speed*math.cos(theta)*math.cos(xi/2)/self.wavelength
        #DoA = vectAngle(vect_RX_point, [0, 1])
        DoA = np.arctan2(rx_pos[0]-self.x, rx_pos[1]-self.y)
        return np.float32(d_tx), np.float32(d_rx), np.float32(DoA), np.float32(doppler_freq)

    # Get Functions
    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPos(self):
        return [self.x, self.y]

    def getVelocity(self):
        return self.v

    def getSpeed(self):
        return self.speed

    def getColor(self):
        return self.color

    # Set Functions

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    # TODO: corriger les trop nombreux paramètres (direction, vx, velocity, etc.)
    def oppositeVX(self):
        self.v[0] = - self.v[0]

    def oppositeVY(self):
        self.v[1] = - self.v[1]

    def updatePos(self, time):
        self.x = self.x + self.v[0]*time
        self.y = self.y + self.v[1]*time

    def computeNewPos(self, time):
        new_x = self.x + self.v[0]*time
        new_y = self.y + self.v[1]*time
        return [new_x, new_y]