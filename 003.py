import random
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def monty_hall_simulation(num_simulations):
    switch_wins = 0
    stay_wins = 0

    for _ in range(num_simulations):
        doors = [0, 0, 1]
        random.shuffle(doors)
        initial_choice = random.randint(0, 2)

        # 主持人打开一扇有山羊的门
        open_door = next(j for j in range(3) if j != initial_choice and doors[j] == 0)

        # 换门策略
        switch_choice = next(j for j in range(3) if j != initial_choice and j != open_door)
        if doors[switch_choice] == 1:
            switch_wins += 1

        # 坚持策略
        if doors[initial_choice] == 1:
            stay_wins += 1

    switch_prob = switch_wins / num_simulations
    stay_prob = stay_wins / num_simulations

    return switch_prob, stay_prob


# 多次实验
num_experiments = 1000
num_simulations_per_experiment = 1000
switch_probs = []
stay_probs = []

for _ in range(num_experiments):
    switch_prob, stay_prob = monty_hall_simulation(num_simulations_per_experiment)
    switch_probs.append(switch_prob)
    stay_probs.append(stay_prob)

# 计算平均概率
average_switch_prob = sum(switch_probs) / num_experiments
average_stay_prob = sum(stay_probs) / num_experiments

# 打印结果
print(f"多次实验后，换门赢的平均概率: {average_switch_prob:.4f}")
print(f"多次实验后，坚持赢的平均概率: {average_stay_prob:.4f}")

# 绘制可视化结果
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.hist(switch_probs, bins=20, color='lightgreen', edgecolor='black')
plt.axvline(x=2 / 3, color='red', linestyle='--', label='贝叶斯理论概率 (2/3)')
plt.xlabel('换门赢的概率')
plt.ylabel('实验次数')
plt.title('换门赢的概率分布')
plt.legend()

plt.subplot(1, 2, 2)
plt.hist(stay_probs, bins=20, color='lightblue', edgecolor='black')
plt.axvline(x=1 / 3, color='red', linestyle='--', label='贝叶斯理论概率 (1/3)')
plt.xlabel('坚持赢的概率')
plt.ylabel('实验次数')
plt.title('坚持赢的概率分布')
plt.legend()

plt.tight_layout()
plt.show()
