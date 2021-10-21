import gym
import numpy as np
from gym.vector.utils import spaces

from envfiles.Region import Region
from envfiles.Bike import Bike
from envfiles.Map import Map
from envfiles.Trip import Trip


class Region_Based_Bike_Sharing_Env(gym.Env):

    # Environment Initializer, needs a seed number to read from and model_name to save results
    def __init__(self, seed_number, model_name):

        if seed_number is -1:
            self.seed_file = open(("../RBBS-Seeds/" + str(Region_Based_Bike_Sharing_Env.generate_seed()) + ".txt"), "r")
        else:
            self.seed_file = open(("../RBBS-Seeds/" + str(seed_number) + ".txt"), "r")
        #C:\Users\Brian\Desktop\SURP\Pycharm\Region-Based-Sharing\RBBS-Seeds\12.txt
        run_info = self.seed_file.readlines()

        # Saving Params
        self.params = run_info[1].split(",")
        for value in range(len(self.params)):
            self.params[value] = int(self.params[value].strip())

        self.size_of_env = self.params[0]
        self.daily_budget = self.params[1]
        self.bikes_in_circulation = self.params[2]
        self.max_hourly_customers = self.params[3]

        self.hour = 0
        self.temp_day_reward = 0
        self.temp_day_budget = 0
        self.successful_trips = 0
        self.walked = 0

        # Create Environment Map
        self.map = Map(self.size_of_env, run_info[2])

        # Saving Trips
        self.trips = []
        self.numb_of_trips = 0
        for hours in range(12):
            people = run_info[hours+3][run_info[hours+3].rindex(":")+1:].split("-")
            hour_trip = []
            for i in people:
                hour_trip.append(Trip(i))
                self.numb_of_trips += 1
            self.trips.append(hour_trip)


        self.action_space = spaces.MultiDiscrete([15]*self.size_of_env**2)
        self.observation_space = spaces.Box(np.array([0] * (self.size_of_env**2 + 2)),
                                            np.array(([11]+[self.bikes_in_circulation] * self.size_of_env**2) + [self.daily_budget]))

        # Now with all the seed data, setup env.
        self.model_name = model_name
        self.env_data = open(("../RBBS-Data/" + model_name + ".txt"), "w")

    def step(self, action):

        reform_act = []
        count = 0
        for x in range(self.size_of_env):
            reform_act.append([0]*self.size_of_env)
            for y in range(self.size_of_env):
                reform_act[x][y] = action[count]
                count += 1

        trips = self.trips[self.hour]

        failed_transactions = 0

        for trip in trips:

            success = self.complete_trip(reform_act, trip)

            if success == -1:
                failed_transactions += 1
            elif success == 0:
                self.successful_trips += 1
            elif success == 1:
                self.successful_trips += 1
                self.walked += 1

        hourly_success = (len(trips) - failed_transactions) / (len(trips))

        self.temp_day_reward += hourly_success

        # resend bikes out
        self.map.end_trips()

        if self.hour >= 11:
            done = True
        else:
            done = False
            self.hour += 1

        # Get oberservation
        obs = self.map.get_state(self.hour, self.temp_day_budget)

        return np.array(obs), hourly_success, done, {"info": str(self.hour)}

    def complete_trip(self, action, trip):

        # First - Find the starting region, check for bikes here, complete trip if so
        starting_reg = self.map.regions[int(trip.x_start/10)][int(trip.y_start/10)]
        if len(starting_reg.bikes) > 0:
            # Bikes are in the region, take from the closest and complete.
            closest = Map.closest_bike(trip, starting_reg.bikes)

            # Move that bike into transit, complete.
            self.map.bike_in_transit(closest, trip.x_end, trip.y_end)
            return 0

        # Now - We need to iterate through all the surrounding regions and get their bikes
        #
        # For this Iteration, the user will always pick the bike with the highest "user-worth'
        # user-worth = Incentive - Walking Cost IFF Incentive <= Remaining Budget
        # Walking Cost = 1/2 Distance to Bike

        nearby_reg = starting_reg.surrounding_regions

        highestUW = -1
        highestUW_bike = None
        highestUW_reg = None

        # For each region nearby the starting reg, grab their bikes, get the UW, save if highest
        for x in nearby_reg:
            reg = self.map.regions[x[0]][x[1]]
            # First check if the incentive for this region is over budget and that the region has bikes
            if len(reg.bikes) > 0 and action[reg.x_coord][reg.y_coord] <= self.temp_day_budget:
                # Checked the two gate keeping params, now iterate through bikes.
                for bike in reg.bikes:
                    tempWC = int(Map.calc_distance(trip.x_start, trip.y_start, bike.x_coord, bike.y_coord))
                    tempUW = action[reg.x_coord][reg.y_coord] - tempWC

                    # Check temp UW on highest
                    if tempUW > highestUW:
                        highestUW_bike = bike
                        highestUW = tempUW
                        highestUW_reg = reg

        # Clean up - if after the dust settles highestUW_bike is still None, no bike is sold
        # If not, take the bike saved at highestUW_bike
        if highestUW_bike is None:
            # Trip failed.
            '''
            for x in nearby_reg:
                reg = self.map.regions[x[0]][x[1]]
                for bike in reg.bikes:
                    print("Bike - "+ str(bike.x_coord)+", "+str(bike.y_coord)+"- REG("+str(reg.x_coord)+","+str(reg.y_coord)+") -- Trip - "+str(trip.x_start)+", "+str(trip.y_start))
                    print("Bike wc - " + str(int(Map.calc_distance(trip.x_start, trip.y_start, bike.x_coord, bike.y_coord))) + ", Reg Ac - " + str(action[reg.x_coord][reg.y_coord]))
            '''

            return -1
        else:
            # Trip successful
            self.map.bike_in_transit(highestUW_bike, trip.x_end, trip.y_end)
            self.temp_day_budget -= action[highestUW_reg.x_coord][highestUW_reg.y_coord]
            return 1


    def reset(self):

        data = float(self.successful_trips) / float(self.numb_of_trips)
        self.env_data.write((str(data) + "\n"))

        print("Day Data - out of " + str(self.numb_of_trips) + ", " + str(
            self.successful_trips) + " were sold with " + str(self.walked) + " walkers")
        print("Budget remaining for the day is - " + str(self.temp_day_budget))

        self.temp_day_reward = 0
        self.temp_day_budget = self.daily_budget



        self.successful_trips = 0
        self.walked = 0
        self.hour = 0

        self.map.reset_bikes()

        return np.array(self.map.get_state(self.hour, self.temp_day_budget))
