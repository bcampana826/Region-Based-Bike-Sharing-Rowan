from envfiles.RbbsEnv import Region_Based_Bike_Sharing_Env

# File used for testing the environment on a static algorithm
env = Region_Based_Bike_Sharing_Env(1, "GREEDY")

state = env.map.get_state(env.hour,env.daily_budget)
# state = [hour, each region .. .. .. , day_budget]
while(state[0] < 11):
    state = env.map.get_state(env.hour, env.daily_budget)
    action = []

    for i in range(len(state)):
        # if i is not the hour nor the budget
        if i is not 0 and i is not len(state)-1:
            action.append(int(50*state[i]/env.bikes_in_circulation))

    print(action)
    returned = env.step(action)
    if returned[2] is True:
        env.reset()
        state = env.map.get_state(env.hour, env.daily_budget)

