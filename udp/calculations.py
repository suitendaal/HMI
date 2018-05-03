import numpy as np
from classes.gap import *
import json


def calculateTimeToIntersection(vehicles):
    # Define main vehicle.
    vehicle = vehicles[0]
    min_speed = vehicle.min_speed
    max_acc = vehicle.max_acc

    # Time with minimal speed on highway.
    t_min = 2 * vehicle.disToInter() / (min_speed + vehicle.dynamics.velocity)

    # Time with maximal acceleration of vehicle.
    temp = np.roots([max_acc / 2, vehicle.dynamics.velocity, -vehicle.disToInter()])
    t_max = np.max(temp[~np.iscomplex(temp)])

    # Time to inter with current speed and acceleration.
    if vehicle.dynamics.acc != 0:
        temp = np.roots([vehicle.dynamics.acc / 2, vehicle.dynamics.velocity, -vehicle.disToInter()])
        vehicle.time_to_inter = np.max(temp[~np.iscomplex(temp)])
        speed_at_inter = vehicle.dynamics.velocity + vehicle.dynamics.acc * vehicle.time_to_inter
    else:
        vehicle.time_to_inter = -1
        speed_at_inter = -1

    # Time to inter for front and back of the car with constant speed at intersection.
    vehicle.time_to_inter_front = vehicle.time_to_inter - vehicle.type.carlength / speed_at_inter
    vehicle.time_to_inter_back = vehicle.time_to_inter + vehicle.type.carlength / speed_at_inter

    return t_min, t_max


def createGaps(vehicles, t_max):
    gaps = []

    for i in range(1, len(vehicles)):
        gap = Gap(vehicles[i-1], vehicles[i])
        if vehicles[i].time_to_inter_front > t_max:
            gaps.append(gap)
        elif gap.disToInter() > 0:
            gaps.append(gap)
            break
        else:
            break

    return gaps


def findTargetGap(vehicles, gaps):
    vehicle = vehicles[0]
    factor = json.load(open('values/num.json'))['factor']

    # Sort gaps on distance from main vehicle.
    gaps.sort(key=lambda x: abs(x.disToInter() - vehicle.disToInter()))

    # Find nearest target gap which is at least the vehicle space.
    target_gap = None
    for gap in gaps:
        if gap.size() > factor * vehicle.type.carlength():
            target_gap = gap
            break

    # If no target gap is found, find the biggest.
    if target_gap is None:
        for gap in gaps:
            if target_gap is None or gap.size() > target_gap.size():
                target_gap = gap
    return target_gap


def advisorySpeed(target_gap, main_vehicle):
    advisory_speed = 2 * main_vehicle.disToInter() / target_gap.timeToInter() + main_vehicle.dynamics.velocity

    # Convert to km/h.
    advisory_speed = advisory_speed * 3.6

    # Round to 5.
    advisory_speed = int(np.round(advisory_speed / 5) * 5)

    return advisory_speed


def calculateAdvisorySpeed(vehicles, t_max):
    main_vehicle = vehicles[0]
    vehicles = vehicles[1:]

    # For every vehicle, calculate time to intersection.
    for vehicle in vehicles:
        vehicle.timeToInter()

    # Sort vehicles on time to inter in order from long to short.
    vehicles.sort(key=lambda x: x.time_to_inter, reverse=True)

    # Delete vehicles which are not in the right lane.
    vehicles_sorted = [vehicle for vehicle in vehicles if vehicle.position.lane == 0 and (vehicle.position.segment in
                                                                                          [0, 1, 3])]
    vehicles = vehicles_sorted

    advisory_speed = -1
    target_gap = None

    if (len(vehicles)) > 0:

        # Create an array of gaps.
        gaps = createGaps(vehicles, t_max)

        # Find target gap.
        target_gap = findTargetGap(vehicles, gaps)

        # Calculate advisory speed
        advisory_speed = advisorySpeed(target_gap, main_vehicle)

    return target_gap, advisory_speed


def checkIfError(old_vehicles, vehicles, old_gap, gap):

    # Check if a vehicle has changed lane.
    if old_vehicles is not None:
        for old_vehicle in old_vehicles:
            # Compare old vehicle with the same vehicle if the lane is changed
            vehicle = [vehicle for vehicle in vehicles if vehicle.partnr == old_vehicle.partnr][0]
            if vehicle.position.lane == 0 and old_vehicle.position.lane != 0:
                return True

    # Check if gap has changed.
    if old_gap is not None:
        # If there is no new gap, gap has disappeared.
        if gap is None:
            return True
        # If gap is changed.
        elif old_gap.vehicle_back.partnr != gap.vehicle_back.partnr or old_gap.vehicle_front.partnr != gap.vehicle_front.partnr:
            return True

    return False
