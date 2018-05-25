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
        self.dot_color = colors['blue']

        self.gap_toegewezen = False
        self.error = False

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
                start_merging_lane = num['udp_data']['road_data']['xpos_start_merginglane']
                end_merging_lane = num['udp_data']['road_data']['xpos_end_merginglane']

                if start_analyzing < vehicles[0].position.xpos < end_merging_lane:
                    if self.level == 3:
                        if self.gap is None:
                            advisory_speed, gap = self.datamanager.calculateAdvisorySpeed(vehicles)
                        else:
                            advisory_speed, gap = self.datamanager.calculateAdvisorySpeed3(vehicles, self.gap)
                            if self.gap_toegewezen and gap is None:
                                self.error = True
                    else:
                        advisory_speed, gap = self.datamanager.calculateAdvisorySpeed(vehicles)

                    if (self.gap is None and self.level == 3 and vehicles[0].position.xpos < start_merging_lane)\
                            or self.level == 4:
                        self.gap = gap
                        if self.level == 3:
                            self.gap_toegewezen = True

                    if difference_time > 2000:
                        start_time = current_time

                        if advisory_speed < 0:
                            self.advisory_speeds = []
                            self.showInHMI("")
                        else:
                            self.advisory_speeds.append(advisory_speed)

                            if len(self.advisory_speeds) > 3:
                                self.advisory_speeds.pop(0)
                            self.showInHMI(self.advisorySpeed())

                    if start_merging_lane < vehicles[0].position.xpos < end_merging_lane and\
                            (self.level == 4 or (self.level == 3 and not gapChanged(self.gap, gap))) and gap is not \
                            None and not self.error:
                        gap.rel_distance = gap.xpos() - vehicles[0].position.xpos
                        gap.speedDifference(vehicles[0].dynamics.velocity)

                        if self.level == 4 and (self.datamanager.checkIfError() or
                                                (self.dot_color == colors['green'] and not self.nextToGap(self.gap, vehicles[0]))):
                            self.dot_color = colors['red']
                        elif self.nextToGap(gap, vehicles[0]):
                            self.dot_color = colors['green']
                        self.plotGap(gap, self.dot_color)
                    else:
                        self.hideGap()
                else:
                    self.advisory_speeds = []
                    self.hideGap()
                    self.showInHMI("")

                if self.error:
                    self.advisory_speeds = []
                    self.showInHMI("")
            else:
                self.showInHMI("")
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
    #                     # self.plotGap(gap)
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

    def plotGap(self, gap, color):
        self.hmi.plotGap(gap.rel_distance, color)

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
        speed_difference = 100 * num['udp_data']['advisory_speed_variables']['speed_difference']
        return gap.speed_difference < speed_difference and self.prediction(gap, vehicle)

    def prediction(self, gap, vehicle):
        reaction_time = num['udp_data']['advisory_speed_variables']['reaction_time']
        gap_front = gap.front + reaction_time * gap.speed()
        gap_back = gap.back + reaction_time * gap.speed()

        vehicle_front = vehicle.front() + vehicle.dynamics.velocity * reaction_time + vehicle.dynamics.acc * reaction_time ** 2
        vehicle_back = vehicle.back() + vehicle.dynamics.velocity * reaction_time + vehicle.dynamics.acc * reaction_time ** 2

        print(str(gap_front) + ", " + str(vehicle_front))
        return vehicle_front < gap_front and vehicle_back > gap_back
