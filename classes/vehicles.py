from tkinter import *
import numpy as np


class Vehicle(object):

    def __init__(self, position, width, length, color):
        self.position = position
        self.width = width
        self.length = length
        self.color = color

    def getCanvas(self, canvas):
        center_x = self.position.pos_x
        center_y = self.position.pos_y
        direction = np.radians(self.position.direction)

        # x0 = center_x - self.width / 2 * math.cos(direction) + self.length / 2 * math.sin(direction)
        # y0 = center_y - self.width / 2 * math.sin(direction) - self.length / 2 * math.cos(direction)
        # x1 = center_x + self.width / 2 * math.cos(direction) + self.length / 2 * math.sin(direction)
        # y1 = center_y + self.width / 2 * math.sin(direction) - self.length / 2 * math.cos(direction)
        # x2 = center_x + self.width / 2 * math.cos(direction) - self.length / 2 * math.sin(direction)
        # y2 = center_y + self.width / 2 * math.sin(direction) + self.length / 2 * math.cos(direction)
        # x3 = center_x - self.width / 2 * math.cos(direction) - self.length / 2 * math.sin(direction)
        # y3 = center_y - self.width / 2 * math.sin(direction) + self.length / 2 * math.cos(direction)
        # max_x = max(x0, x1, x2, x3)
        # min_x = min(x0, x1, x2, x3)
        # max_y = max(y0, y1, y2, y3)
        # min_y = min(y0, y1, y2, y3)
        # coord = x0, y0, x1, y1, x2, y2, x3, y3
        # canvas = Canvas(tk, bg=self.color, height=max_y - min_y, width=max_x - min_x)
        # canvas.create_polygon(coord)
        # return canvas

        c, s = np.cos(direction), np.sin(direction)

        rotationMatrix = [
            [c, -s],
            [s, c]
            ]

        pointMatrix = [
            [-1, -1],
            [1, -1],
            [1, 1],
            [-1, 1]
            ]
        points = np.dot(pointMatrix, [[self.width / 2, 0], [0, self.length / 2]])

        coord = []
        for point in points:
            rotatedPoint = self.rotatedVector(rotationMatrix, point)
            rotatedPoint += [center_x, center_y]
            coord.extend(rotatedPoint)

        canvas.create_polygon(coord, fill=self.color)

        return canvas

    def rotatedVector(self, rotationMatrix, point):
        return np.array(np.dot(rotationMatrix, point))



class Car(Vehicle):

    def __init__(self, position):
        width = 20
        length = 50
        color = 'red'
        super().__init__(position, width, length, color)


class Truck(Vehicle):

    def __init__(self, position):
        width = 60
        length = 200
        color = 'green'
        super().__init__(position, width, length, color)
