import numpy as np
import math
import random

def knapsack_simulated_annealing(weights, values, max_weight, temperature, cooling_rate, iterations):
    num_items = len(weights)
    current_solution = [0] * num_items
    best_solution = current_solution.copy()
    current_weight = 0
    best_weight = 0
    current_value = 0
    best_value = 0

    def evaluate_solution(solution):
        total_weight = np.dot(solution, weights)
        total_value = np.dot(solution, values)
        return total_weight, total_value

    def acceptance_probability(old_weight, new_weight, temperature):
        if new_weight <= max_weight:
            return 1.0
        return math.exp((old_weight - new_weight) / temperature)

    for iteration in range(iterations):
        temperature *= 1 - cooling_rate
        neighbor_solution = current_solution.copy()

        # Flip a random bit
        random_item = random.randint(0, num_items - 1)
        neighbor_solution[random_item] = 1 - neighbor_solution[random_item]

        neighbor_weight, neighbor_value = evaluate_solution(neighbor_solution)
        current_weight, current_value = evaluate_solution(current_solution)

        if acceptance_probability(current_weight, neighbor_weight, temperature) > random.random():
            current_solution = neighbor_solution.copy()
            current_weight = neighbor_weight
            current_value = neighbor_value

        if current_weight <= max_weight and current_value > best_value:
            best_solution = current_solution.copy()
            best_weight = current_weight
            best_value = current_value

    return best_solution, best_weight, best_value

# Nhập số lượng đồ vật, khối lượng đồ vật và tải trọng tối đa của túi từ người dùng
num_items = int(input("Nhập số lượng đồ vật: "))
weights = [int(input(f"Nhập khối lượng của đồ vật {i + 1}: ")) for i in range(num_items)]
values = [int(input(f"Nhập giá trị của đồ vật {i + 1}: ")) for i in range(num_items)]
max_weight = int(input("Nhập tải trọng tối đa của túi: "))

# Thiết lập tham số cho giải thuật Simulated Annealing
initial_temperature = 1000
cooling_rate = 0.03
iterations = 1000

# Gọi hàm giải bài toán cái túi
best_solution, best_weight, best_value = knapsack_simulated_annealing(weights, values, max_weight, initial_temperature, cooling_rate, iterations)

# In kết quả
print("<--Đồ vật được chọn-->")
for i in range(num_items):
    if best_solution[i] == 1:
        print(f"Đồ vật {i + 1} - Khối lượng: {weights[i]}, Giá trị: {values[i]}")

print(f"-->Tổng khối lượng chứa được là : {best_weight}")
print(f"-->Giá trị tối đa của đồ vật được bỏ vào túi là : {best_value}")
