import sys
import math


def distanceEuclidean(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def distance(x1, y1, x2, y2):
    return distanceEuclidean(x1, y1, x2, y2)


class Zone:
    zone_id = -1
    x = -1
    y = -1
    owner = -1

class Drone:
    player_id = -1
    drone_id = -1
    x = -1
    y = -1
    closest_zone_id = -1
    move_x = 0
    move_y = 0


zones = []
drones = []


# Retrieve ininial information 
number_of_players, my_id, number_of_drones, number_of_zones = [ int(i) for i in input().split() ]

# Retrieve zones' location
for zone_id in range(number_of_zones):
    zone = Zone()
    zones.append(zone)

    zone.zone_id = zone_id
    zone.x, zone.y = [ int(i) for i in input().split() ]
    zone.owner = -1

# Create drones' data structure
for player_id in range(number_of_players):
    drones.append([])
    for drone_id in range(number_of_drones):
        drone = Drone()
        drones[player_id].append(drone)

        drone.player_id = player_id  
        drone.drone_id = drone_id
        drone.x = -1
        drone.y = -1
        drone.zone_closest = float('inf')
        drone.move_x = 0
        drone.move_y = 0 


# Game Loop
while True:
    # Retrieve information about zones' ownership
    for zone in zones:
        zone.owner = int(input())

    # Retrieve information about drones' location
    for player_id in range(number_of_players):
        for drone_id in range(number_of_drones):
            drone = drones[player_id][drone_id]
            drone.x, drone.y = [ int(i) for i in input().split() ]
            drone.zone_closest = float('inf')

            # Calculate distance from zones to drones
            for zone in zones:
                from_zone = distance(drone.x, drone.y, zone.x, zone.y)
                if from_zone < drone.zone_closest:
                    drone.zone_closest = from_zone
                    drone.move_x = zone.x
                    drone.move_y = zone.y


    # Move the drones
    for drone_id in range(number_of_drones):
        print(drones[my_id][drone_id].move_x, drones[my_id][drone_id].move_y)
