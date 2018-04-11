from classes.hmidrawer import *
from classes.vehicles import *
from classes.position import *
import matlab.engine


hmi = HMIDrawer()
width_canvas = 621
heigth_canvas = 361
canvas = Canvas(hmi.baseFrame, bg='white', highlightthickness=0, width=width_canvas, height=heigth_canvas)

position1 = Position(100, 100, 45)
car1 = Car(position1)
car1.getCanvas(canvas)

position2 = Position(80, 60, 80)
car2 = Car(position2)
car2.getCanvas(canvas)

position3 = Position(0, 120, -30)
truck = Truck(position3)
truck.getCanvas(canvas)

# Verplaats canvas naar rechts en naar beneden
canvas.place(x=132, y=108)
hmi.show()

