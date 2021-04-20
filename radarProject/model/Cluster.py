import math


class Cluster:
    def __init__(self, r, x, y, v, theta, lambda0, color, is_point):
        self.is_point = is_point
        self.r = r
        self.x = x
        self.y = y
        self.v = v / 3.6
        self.theta = theta * math.pi/180
        self.area = self.computeArea()
        self.color = color
        self.lambda0 = lambda0

    def updateClusterSettings(self, r, x, y, v, theta, lambda0):
        self.r = r
        self.x = x
        self.y = y
        self.v = v / 3.6
        self.theta = theta * math.pi/180
        self.area = self.computeArea()
        self.lambda0 = lambda0

    def setIsPoint(self, is_point):
        self.is_point = is_point

    def computeArea(self):
        return math.pi * self.r ** 2

    def getRadius(self):
        return self.r

    def getArea(self):
        return self.area

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getAngle(self):
        return self.theta

    def getSpeed(self):
        return self.v

    def getLambda0(self):
        return self.lambda0

    def getClusterSettings(self):
        return [self.r, self.x, self.y, self.v * 3.6, self.theta * 180/math.pi, self.lambda0]

    def getColor(self):
        return self.color
