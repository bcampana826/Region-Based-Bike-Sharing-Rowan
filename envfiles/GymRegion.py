import gym
import numpy as np
from gym.vector.utils import spaces

from envfiles.Region import Region
from envfiles.Bike import Bike
from envfiles.Map import Map
from envfiles.Trip import Trip


class GymRegion(gym.Env):

    def __init__(self, seed_number, model_name):
        '''
        Environment Initializer, needs a seed number to read from and model_name to save results
        :param seed_number: used to pull data into the environment
        :param model_name: What to save the data from the environment in
        '''

        # Pulls in the seed file, saves the data into run_info
        self.seed_file = open(("../RBBS-Seeds/" + str(seed_number) + ".txt"), "r")

        run_info = self.seed_file.readlines()

        # Saving Default Parameters for environment
        self.params = run_info[1].split(",")
        for value in range(len(self.params)):
            self.params[value] = int(self.params[value].strip())

        self.size_of_env = self.params[0]
        self.daily_budget = self.params[1]
        self.bikes_in_circulation = self.params[2]
        self.max_hourly_customers = self.params[3]

        # Set the initial variables for the first day.
        self.hour = 0
        self.temp_day_reward = 0
        self.temp_day_budget = 0
        self.successful_trips = 0
        self.walked = 0
