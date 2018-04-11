from classes.hmidrawer import *
from classes.vehicles import *
from classes.position import *
import matlab.engine


hmi = HMIDrawer()

position = Position(0, 0, 30)
car = Car(position)
car.getCanvas(hmi)
# canvas.pack()

# hmi.show()

