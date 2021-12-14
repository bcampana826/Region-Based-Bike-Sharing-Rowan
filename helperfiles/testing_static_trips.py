# testing static trips with 600 max customers per hour
from stable_baselines import TRPO

from envfiles.RbbsEnv import Region_Based_Bike_Sharing_Env
from helperfiles import SeedGeneration


def greedyTesting(seed, str):
    count = 0

    # File used for testing the environment on a static algorithm
    env = Region_Based_Bike_Sharing_Env(seed, str + "-greedy")
    state = env.map.get_state(env.hour, env.daily_budget)

    # state = [hour, each region .. .. .. , day_budget]
    while (state[0] < 11 and count < 250):
        state = env.map.get_state(env.hour, env.daily_budget)
        action = []

        for i in range(len(state)):
            # if i is not the hour nor the budget
            if i is not 0 and i is not len(state) - 1:
                if state[i] / (env.bikes_in_circulation / env.size_of_env ** 2) > 1:
                    # too many
                    action.append(10)
                else:
                    action.append(5)

        returned = env.step(action)
        if returned[2] is True:
            env.reset()
            count += 1
            state = env.map.get_state(env.hour, env.daily_budget)

    env.env_data.close()

def noIncentive(seed, str):
    count = 0

    # File used for testing the environment on a static algorithm
    env = Region_Based_Bike_Sharing_Env(seed, str + "-noINCEN")
    state = env.map.get_state(env.hour, env.daily_budget)

    # state = [hour, each region .. .. .. , day_budget]
    while (state[0] < 11 and count < 25):
        state = env.map.get_state(env.hour, env.daily_budget)
        action = []

        for i in range(len(state)):
            # if i is not the hour nor the budget
            if i is not 0 and i is not len(state) - 1:
                if state[i] / (env.bikes_in_circulation / env.size_of_env ** 2) > 1:
                    # too many
                    action.append(0)
                else:
                    action.append(0)

        returned = env.step(action)
        if returned[2] is True:
            env.reset()
            count += 1
            state = env.map.get_state(env.hour, env.daily_budget)

    env.env_data.close()

bikes = [.5, .75, 1, 1.25, 1.5, 2]
budgets = [1, 2, 5, 10, 15]

# Data Saving Setup
data_file = open(("../RBBS-Data/" + "StaticTestInfo.txt"), "w")

for i in range(len(bikes)):
    for j in range(len(budgets)):
        text = "TRPO-"+str(bikes[i])+"-"+str(budgets[j])
        '''
        seed = SeedGeneration.generate_static_trips(7, budgets[j]*600, int(bikes[i]*600))
        env = Region_Based_Bike_Sharing_Env(seed, text)

        # Instantiate the agent
        model = TRPO('MlpPolicy', env, verbose=1)

        # Train the agent
        timesteps = int(2e5)
        model.learn(total_timesteps=timesteps)
        env.env_data.close()

        # Greedy
        greedyTesting(seed, text)

        # no incentive testing
        noIncentive(seed, text)
        '''
        trained = open(("../RBBS-Data/"+text+".txt"), "r")
        trained_data = [float(n) for n in trained]
        trained_start = trained_data[5]
        trained_end = trained_data[16679]
        trained_learn = trained_end - trained_start

        greedy = open(("../RBBS-Data/"+text+"-greedy"+".txt"), "r")
        greedy_data = [float(n) for n in greedy]
        greedy_value = greedy_data[50]

        noIncen = open(("../RBBS-Data/"+text+"-noINCEN"+".txt"),"r")
        noIncen_data = [float(n) for n in noIncen]
        noIncen_value = noIncen_data[10]

        data_file.write(text+"\n")
        data_file.write("\tTrained Start: "+str(trained_start)+"\n")
        data_file.write("\tTrained End: " + str(trained_end) + "\n")
        data_file.write("\tTrained learn: " + str(trained_learn) + "\n")
        data_file.write("\tGreedy: " + str(greedy_value) + "\n")
        data_file.write("\tNo Incentive: " + str(noIncen_value) + "\n")

