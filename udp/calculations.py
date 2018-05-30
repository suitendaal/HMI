import numpy as np
from classes.gap import *
import json
import os


root = os.getcwd()


def timeToInter(vehicle, acc):
    temp = np.roots([acc / 2, vehicle.dynamics.velocity, -vehicle.disToInter()])
    temp = temp[~np.iscomplex(temp)]
    if len(temp) > 0:
        return np.max(temp)
    else:
        return -1
    pass


def calculateTimeToIntersection(vehicles):
    # Define main vehicle.
    vehicle = vehicles[0]
    min_speed = vehicle.min_speed
    max_acc = vehicle.max_acc

    # Time with minimal speed on highway.
    t_min = 2 * vehicle.disToInter() / (min_speed + vehicle.dynamics.velocity)

    # Time with maximal acceleration of vehicle.
    t_max = timeToInter(vehicle, max_acc)

    # Time to inter with current speed and acceleration.
    vehicle.time_to_inter = t_max  # timeToInter(vehicle, vehicle.dynamics.acc)

    speed_at_inter = vehicle.dynamics.velocity + vehicle.dynamics.acc * vehicle.time_to_inter
    if speed_at_inter == 0:
        speed_at_inter = -1

    # Time to inter for front and back of the car with constant speed at intersection.
    vehicle.time_to_inter_front = vehicle.time_to_inter - vehicle.type.carlength / speed_at_inter
    vehicle.time_to_inter_back = vehicle.time_to_inter + vehicle.type.carlength / speed_at_inter

    return t_min, t_max


def createGaps(vehicles, t_max):
    gaps = []

    for i in range(1, len(vehicles)):
        gap = Gap(vehicles[i], vehicles[i - 1])
        if vehicles[i].time_to_inter_front > t_max:
            gaps.append(gap)
        elif gap.disToInter() > 0:
            gaps.append(gap)
            break
        else:
            break
    return gaps


def findTargetGap(vehicle, gaps):
    gapspace = json.load(open(root + '\\values\\num.json'))['udp_data']['gapspace']
    factor = gapspace['factor']
    max_time = gapspace['time']

    # Sort gaps on distance from main vehicle.
    # gaps.sort(key=lambda x: abs(x.disToInter() - vehicle.disToInter()))
    gaps = gaps[::-1]

    print(gaps[0].xpos(), end=" ")
    print(vehicle.position.xpos)

    # Find nearest target gap which is at least the vehicle space.
    target_gap = None
    for gap in gaps:
        if gap.size() > factor * vehicle.type.carlength:
            target_gap = gap
            break
        if gap.timeToInter() - vehicle.time_to_inter > max_time:
            break

    # If no target gap is found, find the biggest.
    if target_gap is None:
        for gap in gaps:
            if target_gap is None or gap.size() > target_gap.size():
                target_gap = gap
            if gap.timeToInter() - vehicle.time_to_inter > max_time:
                if target_gap is None:
                    target_gap = gap
                break

    return target_gap


def advisorySpeed(target_gap, main_vehicle):
    if main_vehicle.disToInter() < 0:
        return -1

    advisory_speed = 2 * main_vehicle.disToInter() / target_gap.timeToInter() - main_vehicle.dynamics.velocity

    # Convert to km/h.
    advisory_speed = advisory_speed * 3.6

    # Round to 5.
    # advisory_speed = int(np.round(advisory_speed / 5) * 5)

    return advisory_speed


def whereIsGap(all_vehicles, target_gap, tmax):
    vehicles = all_vehicles[1:]

    # For every vehicle, calculate time to intersection.
    for vehicle in vehicles:
        vehicle.timeToInter()

    # Sort vehicles on time to inter in order from long to short.
    vehicles.sort(key=lambda x: x.time_to_inter, reverse=True)

    # Delete vehicles which are not in the right lane.
    vehicles_sorted = [vehicle for vehicle in vehicles if vehicle.position.lane == 0 and (vehicle.time_to_inter > 0)]
    vehicles = vehicles_sorted

    # create all possible gaps
    gaps = createGaps(vehicles, tmax)

    for gap in gaps:
        if gap.vehicle_back.partnr == target_gap.vehicle_back.partnr and gap.vehicle_front.partnr == target_gap.vehicle_front.partnr:
            return gap

    return None


def calculateAdvisorySpeedToGap(vehicles, target_gap):
    main_vehicle = vehicles[0]
    advisory_speed = advisorySpeed(target_gap, main_vehicle)
    if advisory_speed > main_vehicle.max_speed:
        advisory_speed = -1
        target_gap = None

    return target_gap, advisory_speed


def calculateAdvisorySpeed(all_vehicles, t_max, gaps=None):
    main_vehicle = all_vehicles[0]
    vehicles = all_vehicles[1:]

    # For every vehicle, calculate time to intersection.
    for vehicle in vehicles:
        vehicle.timeToInter()

    # Sort vehicles on time to inter in order from long to short.
    vehicles.sort(key=lambda x: x.time_to_inter, reverse=True)

    # Delete vehicles which are not in the right lane.
    vehicles_sorted = [vehicle for vehicle in vehicles if vehicle.position.lane == 0 and (vehicle.time_to_inter > 0)]
    vehicles = vehicles_sorted

    advisory_speed = -1
    target_gap = None

    if (len(vehicles)) > 1:

        # Create an array of gaps.
        if gaps is None:
            gaps = createGaps(vehicles, t_max)

        # Find target gap.
        target_gap = findTargetGap(main_vehicle, gaps)

        # Calculate advisory speed
        if target_gap is not None:
            advisory_speed = advisorySpeed(target_gap, main_vehicle)

            if advisory_speed > main_vehicle.max_speed:
                gaps.remove(target_gap)
                target_gap, advisory_speed = calculateAdvisorySpeed(all_vehicles, t_max, gaps=gaps)

    elif len(vehicles) > 0:
        target_gap = Gap(vehicles[0])
        factor = json.load(open(root + '\\values\\num.json'))['udp_data']['gapspace']['factor']
        target_gap.time_to_inter = max([main_vehicle.time_to_inter, vehicles[0].time_to_inter_back +
                                        factor * main_vehicle.type.carlength / 2 /
                                        vehicles[0].dynamics.velocity])

    if target_gap is not None:
        target_gap.rel_distance = (main_vehicle.time_to_inter_back - target_gap.timeToInter()) * advisory_speed

    return target_gap, advisory_speed


def checkIfError(old_vehicles, vehicles, old_gap, gap):
    return changedLane(old_vehicles, vehicles) or gapChanged(old_gap, gap)


def changedLane(old_vehicles, vehicles):
    # Check if a vehicle has changed lane.
    if old_vehicles is not None:
        for old_vehicle in old_vehicles:
            # Compare old vehicle with the same vehicle if the lane is changed
            vehicle = [vehicle for vehicle in vehicles if vehicle.partnr == old_vehicle.partnr]
            if len(vehicle) > 0:
                vehicle = vehicle[0]
                if vehicle.position.lane == 0 and old_vehicle.position.lane != 0:
                    return True
    return False


def gapChanged(gap1, gap2):
    # Check if gap has changed.
    if gap1 is not None:
        # If there is no new gap, gap has disappeared.
        if gap2 is None:
            return True
        # If gap is changed.
        elif gap1.vehicle_front.partnr != gap2.vehicle_front.partnr:
            # Old vehicle might be None
            if gap1.vehicle_back != gap2.vehicle_back or (gap1.vehicle_back is not None and gap2.vehicle_back is not
                                                            None and gap1.vehicle_back.partnr !=
                                                            gap2.vehicle_back.partnr):
                return True

    return False
