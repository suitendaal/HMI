from udp.datamanager import *
from udp.udpsocket import *
import time
import json
import os


root = os.getcwd()
num = json.load(open(root + '\\values\\num.json'))
colors = json.load(open(root + '\\values\\colors.json'))


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
        start_time = int(time.time() * 1000)
        while self.repeat:
            data = self.socket.get_data()
            vehicles, roads, variables = self.datamanager.manageData(data)

            if vehicles is not None and len(vehicles) > 0:
                self.show_speed(vehicles[0].dynamics.velocity)

            if self.level > 2:

                current_time = int(time.time() * 1000)
                difference_time = current_time - start_time

                start_analyzing = num['udp_data']['road_data']['start_analyzing']
                end_merging_lane = num['udp_data']['road_data']['xpos_end_merginglane']

                if start_analyzing < vehicles[0].position.xpos < end_merging_lane:
                    if self.level == 3:
                        advisory_speed, gap = self.datamanager.calculateAdvisorySpeed(self.gap)
                    else:
                        advisory_speed, gap = self.datamanager.calculateAdvisorySpeed()

                    if (self.gap is None and self.level == 3) or self.level == 4:
                        self.gap = gap

                    if difference_time > 2000:
                        start_time = current_time

                        if advisory_speed < 0:
                            self.advisory_speeds = []
                        else:
                            self.advisory_speeds.append(advisory_speed)

                            if len(self.advisory_speeds) > 3:
                                self.advisory_speeds.pop(0)
                                self.showInHMI(advisory_speed)
                else:
                    gap = None
                    self.advisory_speeds = []

                if gap is None:
                    print("gap is None")
                else:
                    print("gap is not None")

                if (self.level == 4 or (self.level == 3 and not gapChanged(self.gap, gap))) and gap is not None:
                    gap.rel_distance = gap.xpos() - vehicles[0].position.xpos
                    gap.speedDifference(vehicles[0].dynamics.velocity)

                    dot_color = colors['blue']
                    if self.level == 4 and self.datamanager.checkIfError():
                        dot_color = colors['red']
                    elif self.nextToGap(gap, vehicles[0]):
                        dot_color = colors['green']
                    self.plotGap(gap, dot_color)
                else:
                    self.hideGap()

            self.hmi.show()

    #     if self.level > 2:
    #         self.getData()
    #     else:
    #         while self.repeat:
    #             self.hmi.show()
    #
    # def getData(self):
    #     start_time = int(time.time() * 1000)
    #     while self.repeat:
    #         data = self.socket.get_data()
    #
    #         current_time = int(time.time() * 1000)
    #         difference_time = current_time - start_time
    #
    #         self.datamanager.start(data)
    #
    #         if data is not None:
    #             if difference_time > 2000:
    #                 start_time = int(time.time() * 1000)
    #                 # Plot advisory speed.
    #                 advisory_speed = self.datamanager.advisory_speed
    #                 if advisory_speed < 0:
    #                     advisory_speed = num['udp_data']['advisory_speed_variables']['advisory_speed']
    #                     self.showInHMI(advisory_speed)
    #                     self.advisory_speeds = []
    #                     self.hideMergeCommand()
    #                 else:
    #                     self.advisory_speeds.append(advisory_speed)
    #                     if len(self.advisory_speeds) > 3:
    #                         self.advisory_speeds.pop(0)
    #                     self.showInHMI(self.advisorySpeed())
    #
    #             # Plot gap.
    #             distances = json.load(open('values/num.json'))['udp_data']['road_data']
    #
    #             if self.datamanager.gap is not None and distances['xpos_start_merginglane'] < self.datamanager.vehicles[
    #                 0].position.xpos < distances['xpos_end_merginglane']:
    #
    #                 # Show error.
    #                 if self.level == 4:
    #                     if self.datamanager.error:
    #                         self.showError()
    #                     else:
    #                         self.hideError()
    #
    #                 if self.datamanager.vehicles is not None and len(self.datamanager.vehicles) > 0 and \
    #                         self.datamanager.gap is not None:
    #                     main_vehicle = self.datamanager.vehicles[0]
    #                     gap = self.datamanager.gap
    #                     gap.rel_distance = gap.xpos() - main_vehicle.position.xpos
    #
    #                     self.plotGap(gap)
    #
    #                     gap.speedDifference(main_vehicle.dynamics.velocity)
    #                     self.checkIfMerge(gap, main_vehicle)
    #
    #                 else:
    #                     self.hideGap()
    #                     self.hideMergeCommand()
    #
    #             else:
    #                 self.hideMergeCommand()
    #                 self.hideGap()
    #                 if self.level == 4:
    #                     self.hideError()

    def show_speed(self, velocity):
        # TODO
        pass

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
        pass

    def plotGap(self, gap, color):
        self.hmi.plotGap(gap.rel_distance, color)
        pass

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
        distance1_front = num['udp_data']['advisory_speed_variables']['distance1_front']
        distance2_front = num['udp_data']['advisory_speed_variables']['distance2_front']
        distance_back = num['udp_data']['advisory_speed_variables']['distance_back']
        speed_difference = num['udp_data']['advisory_speed_variables']['speed_difference']
        if gap.speed_difference < speed_difference / 4:
            success = vehicle.front() < gap.front + distance2_front and vehicle.back() > gap.back and \
                      gap.speed_difference < speed_difference
        else:
            success = vehicle.front() < gap.front + distance1_front and vehicle.back() > gap.back and \
                      gap.speed_difference < speed_difference
        success = success and vehicle.back() > gap.back - distance_back
        return success

    def prediction(self, gap, vehicle):
        reaction_time = num['udp_data']['advisory_speed_variables']['reaction_time']
        #rel_front =