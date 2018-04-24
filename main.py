from classes.hmidrawer import *
from classes.vehicles import *
from classes.position import *
from time import *
import matlab.engine
import sys


def main():

    if len(sys.argv[1:]) > 0:
        arg = int(sys.argv[1:][0])
        if 0 < arg <= 5:
            sys.exit(4)
    else:
        arg = 4
    print("arg: {}".format(arg))

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
    print(eng.functietester())
    print('JEMOEDER')


if __name__ == '__main__':
    main()
