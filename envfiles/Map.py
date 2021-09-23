import math

from envfiles.Region import Region
from envfiles.Bike import Bike


class Map:

    # Constructor for our bike map
    def __init__(self, size_of_map, bikes_starting_string):

        self.size_of_map = size_of_map
        self.bikes_starting_string = bikes_starting_string
        self.regions = []
        for i in range(size_of_map):
            self.regions.append([Region(None, None)]*size_of_map)

        self.create_regions()

        self.total_bikes = []
        self.moving_bikes = []

        self.reset_bikes()

    # Takes in seed input and turns them into bikes
    def reset_bikes(self):

        self.total_bikes.clear()

        for x in range(self.size_of_map):
            for y in range(self.size_of_map):
                self.regions[x][y].bikes.clear()

        temp = self.bikes_starting_string.split(",")
        for value in range(len(temp)):
            self.total_bikes.append(
                Bike(temp[value].strip().strip('[').strip(']').strip('\'').strip(')').strip('(')))

        self.save_bikes_to_regions()

    # Helper method which sends all bikes to their region
    def save_bikes_to_regions(self):
        for bike in self.total_bikes:
            x = int((bike.x_coord / 10))
            y = int((bike.y_coord / 10))
            self.regions[x][y].bikes.append(bike)


    # Helper method to create, then fill regions with references to eachother
    def create_regions(self):

        for y in range(self.size_of_map):
            for x in range(self.size_of_map):
                self.regions[x][y] = Region(x, y)

        # Gives all the regions references to their surrounding regions for use later
        for i in range(self.size_of_map):
            for j in range(self.size_of_map):
                self.regions[i][j].set_surrounding_regions(self.regions, self.size_of_map)

    # Method called to remove a bike from its region, add it to the intermediate transit list for use later
    def bike_in_transit(self, bike, end_x, end_y):
        self.regions[int(bike.x_coord/10)][int(bike.y_coord/10)].take_bike(bike)

        self.moving_bikes.append([bike, end_x, end_y])

    def end_trips(self):

        for i in range(len(self.moving_bikes)):
            self.moving_bikes[i][0].x_coord = self.moving_bikes[i][1]
            self.moving_bikes[i][0].y_coord = self.moving_bikes[i][2]
            self.regions[int(self.moving_bikes[i][1]/10)][int(self.moving_bikes[i][2]/10)].bikes.append(self.moving_bikes[i][0])
        self.moving_bikes.clear()

    def get_state(self, hour, day_bud):
        obs = [hour]
        for x in range(self.size_of_map):
            for y in range(self.size_of_map):
                obs.append(len(self.regions[x][y].bikes))

        obs.append(day_bud)

        return obs

    @staticmethod
    def closest_bike(trip, list_of_bikes):

        closest = None
        closest_dist = 999999

        for bike in list_of_bikes:

            # This is a stupid work around to the none type problem. should fix this later if i get around to it
            if bike is None:
                dis = 100000
            else:
                dis = Map.calc_distance(bike.x_coord, bike.y_coord, trip.x_start, trip.y_start)
                if dis < closest_dist:
                    closest = bike
                    closest_dist = dis

        return closest

    @staticmethod
    def calc_distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
