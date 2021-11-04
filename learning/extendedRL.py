from stable_baselines import A2C, PPO2, TRPO, PPO1, ACKTR
from stable_baselines.common.evaluation import evaluate_policy
from envfiles.RbbsEnv import Region_Based_Bike_Sharing_Env
from helperfiles.SeedGeneration import generate_seed_working

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

budgets = [1, 2, 5, 10, 15]
bikes = [.5, .75, 1, 1.25, 1.5, 2]
people = [300, 600, 900]

for i in range(len(budgets)):
    for j in range(len(bikes)):
        for k in range(len(people)):



            string = str(people[k])+"-"+str(bikes[j])+"-"+str(budgets[i])
            seednum = generate_seed_working(7, int(budgets[i]*people[k]), int(bikes[j]*people[k]), people[k])

            env = Region_Based_Bike_Sharing_Env(seednum, string)
            greedyTesting(seednum, string)

            model = PPO2('MlpPolicy', env, verbose=1)

            mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

            timesteps = int(2e5)
            model.learn(total_timesteps=timesteps)

            mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

