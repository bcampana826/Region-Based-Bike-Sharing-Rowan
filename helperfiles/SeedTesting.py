# Used for tetsing the different parameters

# for a 7 by 7, starting with a 245 bikes
# Testing the bugdet and number of users
from stable_baselines import TRPO
from stable_baselines.common.evaluation import evaluate_policy

from envfiles.RbbsEnv import Region_Based_Bike_Sharing_Env
from helperfiles import SeedGeneration

max_users = [225, 250, 275, 300, 325]
budgets = [1, 2, 3, 4, 5]


for i in range(len(max_users)):
    for j in range(len(budgets)):
        text = "TRPO-"+str(max_users[i])+"-"+str(budgets[j])
        seed = SeedGeneration.generate_seed(7, budgets[j]*max_users[i], 245, max_users[i])
        env = Region_Based_Bike_Sharing_Env(seed, text)

        # Instantiate the agent
        model = TRPO('MlpPolicy', env, verbose=1)

        # Train the agent
        timesteps = int(2e5)
        model.learn(total_timesteps=timesteps)

