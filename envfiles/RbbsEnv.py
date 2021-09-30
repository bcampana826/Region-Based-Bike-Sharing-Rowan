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

        reform_act = [[0]*self.size_of_env]*self.size_of_env
        count = 0
        for x in range(self.size_of_env):
            for y in range(self.size_of_env):
                reform_act[x][y] = action[0]
                count += 1

        trips = self.trips[self.hour]

        failed_transactions = 0

        for trip in trips:

            success = self.complete_trip(reform_act, trip)

            if not success:
                failed_transactions += 1
            else:
                self.successful_trips += 1

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
        obs = self.map.get_state(self.hour,self.temp_day_budget)

        return np.array(obs), hourly_success, done, {"info": str(self.hour)}

    def complete(self, action, trip):
        # couple things have to happen
        # first -   check the persons starting region to see if any bikes are in there
        #           if so, take a bike and end
        starting_region = self.map.regions[int(trip.x_start/10)][int(trip.y_start/10)]
        if len(starting_region.bikes) > 0:


            # Has bikes in region, take from there, no incentive needed
            closest_bike_in_region = self.map.closest_bike(trip, starting_region.bikes)

            self.map.bike_in_transit(closest_bike_in_region, trip.x_end, trip.y_end)
            return True

        # Now, we need to go through all of our regions adjacent regions and check them with out incentive
        nearby = starting_region.surrounding_regions
        best_deal = None
        best_deal_cost = -1
        for reg in nearby:
            # WC =  dist*.5 ? this could change
            # deal = action - wc

            # if this region has a higher payout, look here for bikes instead
            if best_deal is not None and action[reg.x_coord][reg.y_coord] > action[int(best_deal.x_coord / 10)][int(best_deal.y_coord / 10)]:

                for bike in reg[0].bikes:

                    cost = int((self.map.calc_distance(bike.x_coord, bike.y_coord, trip.x_start, trip.y_start) * .5))
                    if action[reg[0].x_coord][reg[0].y_coord] <= self.temp_day_budget and best_deal_cost < action[reg[0].x_coord][reg[0].y_coord] - cost < 0:
                        best_deal_cost = cost
                        best_deal = bike

            elif best_deal is None:

                for bike in reg[0].bikes:

                    cost = int((self.map.calc_distance(bike.x_coord, bike.y_coord, trip.x_start, trip.y_start) * .5))
                    if action[reg[0].x_coord][reg[0].y_coord] <= self.temp_day_budget and best_deal_cost < action[reg[0].x_coord][reg[0].y_coord] - cost < 0:
                        best_deal_cost = cost
                        best_deal = bike

        if best_deal is not None:
            # now with found bike, remove it from the region its in and add it to moving bikes in map
            self.map.bike_in_transit(best_deal, trip.x_end, trip.y_end)
            self.temp_day_budget -= action[int(best_deal.x_coord/10)][int(best_deal.y_coord/10)]
            return True
        else:

            return False


    def complete_trip(self, action, trip):

        # First - Find the starting region, check for bikes here, complete trip if so
        starting_reg = self.map.regions[int(trip.x_start/10)][int(trip.y_start/10)]
        if len(starting_reg.bikes) > 0:
            # Bikes are in the region, take from the closest and complete.
            closest = Map.closest_bike(trip, starting_reg.bikes)

            # Move that bike into transit, complete.
            self.map.bike_in_transit(closest, trip.x_end, trip.y_end)

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
        for reg in nearby_reg:
            # First check if the incentive for this region is over budget and that the region has bikes
            if len(reg.bikes) > 0 and action[reg.x_coord][reg.y_coord] <= self.temp_day_budget:
                # Checked the two gate keeping params, now iterate through bikes.
                for bike in reg.bikes:
                    tempWC = int(.5 * Map.calc_distance(trip.x_start, trip.y_start, bike.x_coord, bike.y_coord))
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
            return False
        else:
            # Trip successful
            self.map.bike_in_transit(highestUW_bike, trip.x_end, trip.y_end)
            self.temp_day_budget -= action[highestUW_reg.x_coord][highestUW_reg.y_coord]
            return True


    def reset(self):

        data = float(self.successful_trips) / float(self.numb_of_trips)
        print(self.successful_trips)
        print(self.numb_of_trips)
        print(data)
        self.env_data.write((str(data) + "\n"))
        self.temp_day_reward = 0
        self.temp_day_budget = self.daily_budget

        self.successful_trips = 0
        self.hour = 0

        self.map.reset_bikes()

        return np.array(self.map.get_state(self.hour, self.temp_day_budget))
