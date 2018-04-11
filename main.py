from classes.hmidrawer import *
from classes.vehicles import *
from classes.position import *
import matlab.engine


hmi = HMIDrawer()

position = Position(10, 10, 45)
car = Car(position)
canvas = car.getCanvas(hmi.label)
canvas.pack()

hmi.show()

