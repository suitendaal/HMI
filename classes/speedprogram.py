from udp.datamanager import *
from udp.udpsocket import *
import time
import json
import os


root = os.getcwd()
num = json.load(open(root + '\\values\\num.json'))


class SpeedProgram(object):
    def __init__(self, hmi, level):
        self.repeat = True

        self.hmi = hmi
        self.hmi.show()
        self.gap = None
        self.advisory_speeds = []

        self.level = level

        self.socket = UDPSocket((server_values['ip_address'], server_values['port']))
        self.datamanager = DataManager(self.socket)

    def start(self):
        self.getData()

    def getData(self):
        start_time = int(time.time() * 1000)
        while self.repeat:
            data = self.socket.get_data()

            current_time = int(time.time() * 1000)
            difference_time = current_time - start_time

            self.datamanager.start(data)

            if data is not None:
                if difference_time > 2000:
                    start_time = int(time.time() * 1000)
                    # Plot advisory speed.
                    advisory_speed = self.datamanager.advisory_speed
                    if advisory_speed < 0:
                        advisory_speed = num['udp_data']['advisory_speed_variables']['advisory_speed']
                        self.showInHMI(advisory_speed)
                        self.advisory_speeds = []
                        self.hideMergeCommand()
                    else:
                        self.advisory_speeds.append(advisory_speed)
                        if len(self.advisory_speeds) > 3:
                            self.advisory_speeds.pop(0)
                        self.showInHMI(self.advisorySpeed())

                # Plot gap.
                distances = json.load(open('values/num.json'))['udp_data']['road_data']

                if self.datamanager.gap is not None and distances['xpos_start_merginglane'] < self.datamanager.vehicles[
                    0].position.xpos < distances['xpos_end_merginglane']:

                    # Show error.
                    if self.level == 4:
                        if self.datamanager.error:
                            self.showError()
                        else:
                            self.hideError()

                    if self.datamanager.vehicles is not None and len(self.datamanager.vehicles) > 0 and self.datamanager.gap is not None:
                        main_vehicle = self.datamanager.vehicles[0]
                        gap = self.datamanager.gap
                        gap.rel_distance = gap.xpos() - main_vehicle.position.xpos

                        self.plotGap(gap)

                        gap.speedDifference(main_vehicle.dynamics.velocity)
                        self.checkIfMerge(gap, main_vehicle)

                    else:
                        self.hideGap()

                else:
                    self.hideGap()
                    if self.level == 4:
                        self.hideError()

    def showInHMI(self, advisory_speed):
        self.hmi.setText(str(advisory_speed))

    def mergeCommand(self):
        self.hmi.showMergingCommand()

    def hideMergeCommand(self):
        self.hmi.hideMergingCommand()

    def showError(self):
        self.hmi.showError()

    def hideError(self):
        self.hmi.hideError()

    def hideGap(self):
        self.hmi.hideGap()

    def plotGap(self, gap):
        self.hmi.plotGap(gap.rel_distance)

    def advisorySpeed(self):
        amount = 0
        total = 0
        for i in range(len(self.advisory_speeds)):
            total += (i + 1) * self.advisory_speeds[i]
            amount += i + 1
        return int(float(total) / amount)

    def checkIfMerge(self, gap, vehicle):
        # Show if you are next to gap.
        if self.nextToGap(gap, vehicle):
            self.mergeCommand()
        else:
            self.hideMergeCommand()

    def nextToGap(self, gap, vehicle):
        distance = num['udp_data']['advisory_speed_variables']['distance']
        speed_difference = num['udp_data']['advisory_speed_variables']['speed_difference']
        success = vehicle.front() < gap.front and vehicle.back() > gap.back and gap.speed_difference < speed_difference
        return success
