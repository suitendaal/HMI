import json
import os


root = os.getcwd()


class Gap(object):

    def __init__(self, vehicle_front, vehicle_back=None):
        self.vehicle_back = vehicle_back
        self.vehicle_front = vehicle_front
        self.rel_distance = 0
        self.time_to_inter = 0
        self.speed_difference = 0
        self.front = vehicle_front.back()
        if vehicle_back is None:
            self.back = -100
        else:
            self.back = vehicle_back.front()

    def xpos(self):
        return (self.back + self.front) / 2

    def disToInter(self):
        xpos_merginlane = json.load(open(root + '\\values\\num.json'))['udp_data']['road_data']['xpos_end_merginglane']
        return xpos_merginlane - self.xpos()

    def size(self):
        return abs(self.front - self.back)

    def speed(self):
        speed_front = self.vehicle_front.dynamics.velocity
        if self.vehicle_back is None:
            speed_back = speed_front
        else:
            speed_back = self.vehicle_back.dynamics.velocity
        return (speed_back + speed_front) / 2

    def timeToInter(self):
        if self.vehicle_back is not None:
            return self.disToInter() / self.speed()
        else:
            return self.time_to_inter

    def speedDifference(self, speed):
        self.speed_difference = abs(self.speed() - speed)
        return self.speed_difference