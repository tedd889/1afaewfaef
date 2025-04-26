import random


def monty_hall_bayesian_verification(num_simulations):
    switch_wins = 0
    initial_correct_count = 0  # 记录初始选对的次数

    for _ in range(num_simulations):
        doors = [0, 0, 1]
        random.shuffle(doors)
        initial_choice = random.randint(0, 2)

        # 标记初始是否选对
        initial_correct = doors[initial_choice] == 1
        if initial_correct:
            initial_correct_count += 1

        # 主持人开门（非初始选择且非汽车门）
        open_door = next(i for i in range(3) if i != initial_choice and doors[i] == 0)

        # 换门策略：选择唯一未选且未开的门
        switch_choice = next(i for i in range(3) if i != initial_choice and i != open_door)
        if doors[switch_choice] == 1:
            switch_wins += 1

    # 计算贝叶斯理论值与模拟值
    theoretical_switch_win = (num_simulations - initial_correct_count) / num_simulations  # 初始错误时换门必赢
    simulated_switch_win = switch_wins / num_simulations
    initial_correct_rate = initial_correct_count / num_simulations  # 应接近1/3

    return (theoretical_switch_win, simulated_switch_win, initial_correct_rate)


# 模拟100万次
theo_win, sim_win, initial_correct = monty_hall_bayesian_verification(1000000)
print(f"初始选对概率（理论值1/3）: {initial_correct:.4%}")
print(f"换门胜率（贝叶斯推导）: {theo_win:.4%}")
print(f"换门胜率（模拟结果）: {sim_win:.4%}")