from stable_baselines import A2C, PPO2, TRPO, PPO1, ACKTR
from stable_baselines.common.evaluation import evaluate_policy
from envfiles.RbbsEnv import Region_Based_Bike_Sharing_Env


# Create environment
print("env")
env = Region_Based_Bike_Sharing_Env(2, "PPO2")

# Instantiate the agent
print("model")
model = PPO2('MlpPolicy', env, verbose=1)

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