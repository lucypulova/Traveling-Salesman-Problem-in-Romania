import random
import math
import numpy as np
import matplotlib.pyplot as plt
from itertools import islice

# Дефиниране на разстоянието между две точки

def calculate_distance(city1, city2):
    return math.hypot(city1[0] - city2[0], city1[1] - city2[1])

# Дефиниране на локациите на селищата
romania_locations = {
    "Arad": (91, 492), "Bucharest": (400, 327), "Craiova": (253, 288),
    "Drobeta": (165, 299), "Eforie": (562, 293), "Fagaras": (305, 449),
    "Giurgiu": (375, 270), "Hirsova": (534, 350), "Iasi": (473, 506),
    "Lugoj": (165, 379), "Mehadia": (168, 339), "Neamt": (406, 537),
    "Oradea": (131, 571), "Pitesti": (320, 368), "Rimnicu": (233, 410),
    "Sibiu": (207, 457), "Timisoara": (94, 410), "Urziceni": (456, 350),
    "Vaslui": (509, 444), "Zerind": (108, 531)
}

cities = list(romania_locations.keys())

# Функция за изчисляване на общото разстояние на даден маршрут

def route_distance(route):
    return sum(
        calculate_distance(romania_locations[route[i]], romania_locations[route[i + 1]])
        for i in range(len(route) - 1)
    ) + calculate_distance(romania_locations[route[-1]], romania_locations[route[0]])

# Създаване на начална популация

def initial_population(pop_size, cities):
    return [random.sample(cities, len(cities)) for _ in range(pop_size)]

# Оценка на популацията

def evaluate_population(population):
    return [route_distance(individual) for individual in population]

# Селекция на родителите с турнирна селекция

def select_parents(population, fitness, num_parents):
    selected_parents = []
    for _ in range(num_parents):
        tournament = random.sample(list(zip(population, fitness)), k=5)
        selected_parents.append(min(tournament, key=lambda x: x[1])[0])
    return selected_parents

# Кросоувър оператор

def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child_p1 = parent1[start:end]
    child_p2 = [city for city in parent2 if city not in child_p1]
    return child_p1 + child_p2

# Мутация на дете

def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]

# Генетичен алгоритъм с елитизъм за решаване на проблема на търговския пътник

def genetic_algorithm(cities, pop_size, generations, mutation_rate):
    population = initial_population(pop_size, cities)
    for generation in range(generations):
        fitness = evaluate_population(population)

        # Запазване на най-добрия индивид (елитизъм)
        best_individual = min(population, key=route_distance)

        parents = select_parents(population, fitness, pop_size // 2)
        next_population = parents[:]

        while len(next_population) < pop_size - 1:
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)
            mutate(child, mutation_rate)
            next_population.append(child)

        # Добавяне на най-доброто решение в популацията
        next_population.append(best_individual)

        population = next_population

    best_route = min(population, key=route_distance)
    return best_route, route_distance(best_route)

# Параметри на генетичния алгоритъм
population_size = 100
generations = 300
mutation_rate = 0.015

# Изпълнение на алгоритъма
best_route, best_distance = genetic_algorithm(cities, population_size, generations, mutation_rate)

# Отпечатване на резултатите
print("Най-добър маршрут:", " -> ".join(best_route))
print(f"Дължина на маршрута: {best_distance:.2f}")

# Визуализация на маршрута
def plot_route(route):
    x = [romania_locations[city][0] for city in route + [route[0]]]
    y = [romania_locations[city][1] for city in route + [route[0]]]
    plt.plot(x, [-y for y in y], 'ro-')  # Промяна на знака на y координатите, за да се обърнат горе-долу
    for city in route:
        plt.text(romania_locations[city][0], -romania_locations[city][1], city, fontsize=9)
    plt.xlabel('X координата')
    plt.ylabel('Y координата')
    plt.title('Най-добрият маршрут на търговския пътник')
    plt.grid(True)
    plt.gcf().canvas.manager.set_window_title('Домашно 1')
    plt.show()

plot_route(best_route)










