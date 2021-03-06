from envfiles.RbbsEnv import Region_Based_Bike_Sharing_Env
import os


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

def test_greedies():
    for files in os.listdir('C:\\Users\\Brian\\Desktop\\SURP\\Pycharm\\Region-Based-Sharing\\RBBS-Seeds'):
        if files.count(".txt") > 0:
            seed_file = open(("../RBBS-Seeds/" + files),
                             "r")

            text = seed_file.readlines()
            print(text[1])

            greedyTesting(int(files.split(".")[0]), "TRPO-" + str(float(text[1].split(",")[2]) / 600) + "-" + str(
                float(text[1].split(",")[1]) / 600))


test_greedies()
