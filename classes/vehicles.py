from tkinter import *


class Vehicle(object):

    def __init__(self, position, width, length, color):
        self.position = position
        self.width = width
        self.length = length
        self.color = color

    def getDrawing(self):
        print()
        # TODO


class Car(Vehicle):

    def __init__(self, position):
        width = 50
        length = 100
        color = 'red'
        super().__init__(position, width, length, color)


class Truck(Vehicle):

    def __init__(self, position):
        width = 60
        length = 200
        color = 'green'
        super().__init__(position, width, length, color)