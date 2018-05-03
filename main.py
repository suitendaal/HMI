from classes.hmidrawer import *
from classes.vehicles import *
from classes.position import *
from time import *
import matlab.engine
import sys
import socket
from udp.udpsocket import UDPSocket
from udp.datamanager import DataManager
from classes.speedprogram import *


def main():
    window = HMIDrawer()
    program = SpeedProgram(window)
    program.start()
    #while True:
     #   window.show()


if __name__ == '__main__':
    main()
