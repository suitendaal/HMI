from classes.hmidrawer import *
from classes.vehicles import *
from classes.position import *


hmi = HMIDrawer()

position = Position(0, 0, 30)
car = Car(position)
canvas = car.getCanvas(hmi)
canvas.pack()

hmi.show()