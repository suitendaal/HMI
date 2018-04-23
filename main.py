from classes.hmidrawer import *
from classes.vehicles import *
from classes.position import *
from time import *
import matlab.engine


def main():
    # hmi = HMIDrawer()

    # position1 = Position(100, 100, 45)
    # car1 = Car(position1)
    # car1.drawing(hmi.canvas)
    # hmi.update_idletasks()
    # sleep(2)
    #
    # position2 = Position(80, 60, 80)
    # car2 = Car(position2)
    # car2.drawing(hmi.canvas)
    # hmi.update_idletasks()
    # sleep(2)
    #
    # position3 = Position(0, 120, -30)
    # truck = Truck(position3)
    # truck.drawing(hmi.canvas)
    # hmi.update_idletasks()
    # sleep(2)

    eng = matlab.engine.start_matlab()
    eng.addpath(r'matlab', nargout=0)
    print(eng.kwadraat(2))
    print('JEMOEDER')
    print(eng.kwadraat(3))

if __name__ == '__main__':
    main()
