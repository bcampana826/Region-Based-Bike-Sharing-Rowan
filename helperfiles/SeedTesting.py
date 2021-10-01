# Used for tetsing the different parameters

# for a 7 by 7, starting with a 245 bikes
# Testing the bugdet and number of users

max_users = [150, 175, 200, 225, 250, 275, 300, 325, 350, 375]
budgets = [1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 7.5, 10]


for i in range(len(max_users)):
    for j in range(len(budgets)):
        text = "TRPO-"+str(max_users[i])+"-"+str(budgets[j])
        seed = generate_seed(7, budgets[j], 245, max_users[i])
        env = Region_Based_Bike_Sharing_Env(seed, text)

        # Instantiate the agent
        print("model")
        model = TRPO('MlpPolicy', env, verbose=1)

        mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
        print(mean_reward)
        print(std_reward)
        # Train the agent
        print("learn")
        timesteps = int(2e5)
        model.learn(total_timesteps=timesteps)

        mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)
        print(mean_reward)
        print(std_reward)
