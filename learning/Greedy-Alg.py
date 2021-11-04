from envfiles.RbbsEnv import Region_Based_Bike_Sharing_Env

def greedyTesting(seed, str):

    count = 0


    # File used for testing the environment on a static algorithm
    env = Region_Based_Bike_Sharing_Env(seed, str+"-greedy")
    state = env.map.get_state(env.hour, env.daily_budget)


    # state = [hour, each region .. .. .. , day_budget]
    while (state[0] < 11 and count<250):
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

greedyTesting(2,"2")