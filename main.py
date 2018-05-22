from classes.hmidrawer import *
from classes.speedprogram import *
import sys
import time


def main():
    level = 3
    if len(sys.argv) == 2 and int(sys.argv[1]) in [1, 2, 3, 4]:
        level = int(sys.argv[1])

    window = HMIDrawer(level)
    program = SpeedProgram(window, level)

    program.start()

    
if __name__ == '__main__':
    main()
    time.sleep(1)
