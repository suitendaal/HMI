from classes.hmidrawer import *
from classes.speedprogram import *
from classes.gap import *
from udp.calculations import *
import sys


def main():
    level = 3
    if len(sys.argv) == 2 and int(sys.argv[1]) in [3, 4]:
        level = int(sys.argv[1])

    window = HMIDrawer()
    program = SpeedProgram(window, level)

    # Tijdelijk voor plotten en troubleshooting
    main_vehicle = MainVehicle()
    print("Mainvehicle: " + str(main_vehicle.type.carlength) + "  " + str(main_vehicle.time_to_inter()) + "  " + str(main_vehicle.position.xpos()))

    program.start()
    #while True:
     #   window.show()


if __name__ == '__main__':
    main()
