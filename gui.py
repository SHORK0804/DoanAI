import tkinter as tk
from tkinter import Label, Entry, Button
import numpy as np
import math
import random

def create_entry_fields(num_items):
    label_weights = Label(root, text="Nhập khối lượng của từng đồ vật:")
    label_weights.pack()

    global entry_weights
    entry_weights = [Entry(root) for _ in range(num_items)]
    for entry in entry_weights:
        entry.pack()

    label_values = Label(root, text="Nhập giá trị của từng đồ vật:")
    label_values.pack()

    global entry_values
    entry_values = [Entry(root) for _ in range(num_items)]
    for entry in entry_values:
        entry.pack()

def knapsack_simulated_annealing(weights, values, max_weight, temperature, cooling_rate, iterations):
    # Rest of the code remains the same
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

def knapsack_solver():
    num_items = int(entry_num_items.get())
    weights = [int(entry_weights[i].get()) for i in range(num_items)]
    values = [int(entry_values[i].get()) for i in range(num_items)]
    max_weight = int(entry_max_weight.get())

    initial_temperature = 1000
    cooling_rate = 0.03
    iterations = 1000

    best_solution, best_weight, best_value = knapsack_simulated_annealing(weights, values, max_weight, initial_temperature, cooling_rate, iterations)

    result_label.config(text="<--Đồ vật được chọn-->\n")
    for i in range(num_items):
        if best_solution[i] == 1:
            result_label.config(text=result_label.cget("text") + f"Đồ vật {i + 1} - Khối lượng: {weights[i]}, Giá trị: {values[i]}\n")

    result_label.config(text=result_label.cget("text") + f"\n-->Tổng khối lượng chứa được là : {best_weight}\n")
    result_label.config(text=result_label.cget("text") + f"-->Giá trị tối đa của đồ vật được bỏ vào túi là : {best_value}")

def on_button_click():
    num_items = int(entry_num_items.get())
    create_entry_fields(num_items)
    button_solve.config(command=knapsack_solver)

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Bài toán cái túi với Simulated Annealing")

# Tạo các widget
label_num_items = Label(root, text="Nhập số lượng đồ vật:")
label_num_items.pack()

entry_num_items = Entry(root)
entry_num_items.pack()

button_create_fields = Button(root, text="Tạo ô nhập thuộc tính", command=on_button_click)
button_create_fields.pack()

label_max_weight = Label(root, text="Nhập tải trọng tối đa của túi:")
label_max_weight.pack()

entry_max_weight = Entry(root)
entry_max_weight.pack()

button_solve = Button(root, text="Giải bài toán")
button_solve.pack()

result_label = Label(root, text="")
result_label.pack()

# Chạy ứng dụng
root.mainloop()