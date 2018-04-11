from classes.hmidrawer import *
from classes.vehicles import *
from classes.position import *
import matlab.engine


hmi = HMIDrawer()
canvas = Canvas(hmi.baseFrame, bg='white', width=625)
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)

position1 = Position(100, 100, 45)
car1 = Car(position1)
car1.getCanvas(canvas)

position2 = Position(80, 60, 80)
car2 = Car(position2)
car2.getCanvas(canvas)

position3 = Position(0, 120, -30)
truck = Truck(position3)
truck.getCanvas(canvas)

canvas.pack()
hmi.show()

