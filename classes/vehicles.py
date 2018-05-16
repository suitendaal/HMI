import numpy as np
from classes.environment import Environment
import json
import os


root = os.getcwd()
colors = json.load(open(root + '\\values\\colors.json'))


class Vehicle(Environment):

    def __init__(self, position, width, length, color):
        super().__init__(color)
        self.position = position
        self.width = width
        self.length = length

    def drawing(self, canvas):
        center_x = self.position.pos_x
        center_y = self.position.pos_y
        direction = np.radians(self.position.direction)

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

        return super().drawing(canvas, coord)

    def rotatedVector(self, rotationMatrix, point):
        return np.array(np.dot(rotationMatrix, point))



class Car(Vehicle):

    def __init__(self, position):
        width = 20
        length = 50
        color = colors['car']
        super().__init__(position, width, length, color)


class Truck(Vehicle):

    def __init__(self, position):
        width = 60
        length = 200
        color = colors['truck']
        super().__init__(position, width, length, color)
