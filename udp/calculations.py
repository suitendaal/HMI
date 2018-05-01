import numpy as np
from classes.gap import *


def calculateTimeToIntersection(vehicles):
    # Define main vehicle.
    vehicle = vehicles[0]
    min_speed = vehicle.min_speed
    max_acc = vehicle.max_acc

    # Time with minimal speed on highway.
    t_min = 2 * vehicle.dynamics.dis_to_inter / (min_speed + vehicle.dynamics.velocity)

    # Time with maximal acceleration of vehicle.
    temp = np.roots([max_acc / 2, vehicle.dynamics.velocity, -vehicle.dynamics.dis_to_inter])
    t_max = np.max(temp[~np.iscomplex(temp)])

    # Time to inter with current speed and acceleration.
    temp = np.roots([vehicle.dynamics.acc / 2, vehicle.dynamics.velocity, -vehicle.dynamics.dis_to_inter])
    vehicle.time_to_inter = np.max(temp[~np.iscomplex(temp)])
    speed_at_inter = vehicle.dynamics.velocity + vehicle.dynamics.acc * vehicle.time_to_inter

    # Time to inter for front and back of the car with constant speed at intersection.
    vehicle.time_to_inter_front = vehicle.time_to_inter - vehicle.type.carlength / speed_at_inter
    vehicle.time_to_inter_back = vehicle.time_to_inter + vehicle.type.carlength / speed_at_inter

    return t_min, t_max


def createGaps(vehicles, t_max):
    gaps = []

    # Define first no_gap.
    no_gap = Gap(vehicles[0].time_to_inter_back, vehicles[0].time_to_inter_front, False)
    gaps.append(no_gap)

    # Define other gaps.
    for i in range(1, len(vehicles)):
        gap = Gap(vehicles(i - 1).time_to_inter_front, vehicles(i).time_to_inter_back, True)
        no_gap = Gap(vehicles(i).time_to_inter_back, vehicles(i).time_to_inter_front, False)
        gaps.extend([gap, no_gap])

    if vehicles(-1).time_to_inter_front > t_max:
        gap = Gap(vehicles(-1).time_to_inter_front, t_max, True)
        gaps.append(gap)

    return gaps


def find_target_gap(vehicles, gaps):
    vehicle = vehicles[0]
    time_to_inter = vehicle.time_to_inter
    gaps = gaps.sortGaps(time_to_inter)
    for i in gaps:
        if gaps{i}.isgap AND gaps{i}.getDuration > abs(vehicle.time_to_inter_front - vehicle.time_to_inter_back)
            target_gap = gaps{i}
        break
    break

    # TODO: Sort gaps on time from predicted time. Find target gap
    return None


def calculateAdvisorySpeed(vehicles, t_max):
    main_vehicle = vehicles[0]
    vehicles = vehicles[1:]

    # For every vehicle, calculate time to intersection.
    for vehicle in vehicles:
        vehicle.timeToInter()

    # Sort vehicles on time to inter in order from long to short.
    vehicles.sort(key=lambda x: x.time_to_inter, reverse=True)

    # Delete vehicles which are not in the right lane.
    vehicles_sorted = [vehicle for vehicle in vehicles if vehicle.dynamics.lane == 0]
    vehicles = vehicles_sorted

    # Create an array of gaps.
    gaps = createGaps(vehicles, t_max)

    # Find target gap.
    target_gap = find_target_gap(gaps)

    # Calculate advisory speed
    advisory_speed = 2 * main_vehicle.dynamics.dis_to_inter / target_gap.GetTimeToInter() + \
                     main_vehicle.dynamics.velocity

    advisory_speed = advisory_speed * 3.6

    # Round to 5
    advisory_speed = np.round(advisory_speed / 5) * 5

    return advisory_speed
