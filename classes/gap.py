import json


class Gap(object):

    def __init__(self, vehicle_front, vehicle_back=None):
        self.vehicle_back = vehicle_back
        self.vehicle_front = vehicle_front
        self.rel_distance = 0
        self.time_to_inter = 0
        self.speed_difference = 0

    def xpos(self):
        xpos_back = self.vehicle_back.position.xpos + self.vehicle_back.type.carlength / 2
        xpos_front = self.vehicle_front.position.xpos - self.vehicle_front.type.carlength / 2
        return (xpos_back + xpos_front) / 2

    def disToInter(self):
        xpos_merginlane = json.load(open('values/num.json'))['udp_data']['road_data']['xpos_end_merginglane']
        return xpos_merginlane - self.xpos()

    def size(self):
        xpos_back = self.vehicle_back.position.xpos  # + self.vehicle_back.type.carlength / 2
        xpos_front = self.vehicle_front.position.xpos - 2 * self.vehicle_front.type.carlength / 2
        return abs(xpos_front - xpos_back)

    def speed(self):
        speed_back = self.vehicle_back.dynamics.velocity
        speed_front = self.vehicle_front.dynamics.velocity
        return (speed_back + speed_front) / 2

    def timeToInter(self):
        if self.vehicle_back is not None:
            return self.disToInter() / self.speed()
        else:
            return self.time_to_inter

    def speedDifference(self, speed):
        self.speed_difference = abs(self.speed() - speed)
        return self.speed_difference