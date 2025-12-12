import random
import pandas as pd
import time

def to_minutes(t):
    h, m = map(int, t.strip().split(":"))
    return h * 60 + m

data = []
with open("C:/Users/MONSTER/Desktop/flights.txt", "r") as file:
    for line in file:
        origin, dest, dep_time, arr_time, price = line.strip().split(",")
        data.append({
            "origin": origin,
            "destination": dest,
            "dep_time": dep_time,
            "arr_time": arr_time,
            "dep_min": to_minutes(dep_time),
            "arr_min": to_minutes(arr_time),
            "price": int(price)
        })

df = pd.DataFrame(data)
df = df.head(30)  

n_flights = len(df)
max_planes = 8

conflict = {}
for i in range(n_flights):
    for k in range(i + 1, n_flights):
        a_start, a_end = df.loc[i, "dep_min"], df.loc[i, "arr_min"]
        b_start, b_end = df.loc[k, "dep_min"], df.loc[k, "arr_min"]
        if not (a_end <= b_start or b_end <= a_start):
            conflict[(i, k)] = True

population_size = 60
generations = 150
mutation_rate = 0.2

# === Fitness Function: Total cost + penalty for conflicts ===
def fitness(assignment):
    total_cost = sum(df.loc[i, "price"] for i in range(n_flights))
    penalty = 0
    for (i, k) in conflict:
        if assignment[i] == assignment[k]:
            penalty += 5000  # conflict penalty
    return total_cost + penalty

def create_population():
    population = []
    for _ in range(population_size):
        individual = [random.randint(0, max_planes - 1) for _ in range(n_flights)]
        population.append(individual)
    return population

# === Selection: Top 2 fittest individuals ===
def select_parents(population):
    population.sort(key=fitness)
    return population[:2]

# === Crossover Function ===
def crossover(p1, p2):
    point = random.randint(1, n_flights - 2)
    return p1[:point] + p2[point:]

# === Mutation Function ===
def mutate(individual):
    for i in range(n_flights):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, max_planes - 1)
    return individual

start_time = time.time()

population = create_population()
best_solution = None
best_cost = float('inf')

for generation in range(generations):
    new_population = []
    parents = select_parents(population)
    for _ in range(population_size):
        child = crossover(*parents)
        child = mutate(child)
        new_population.append(child)

    population = new_population
    current_best = min(population, key=fitness)
    current_cost = fitness(current_best)

    if current_cost < best_cost:
        best_cost = current_cost
        best_solution = current_best

end_time = time.time()
duration = end_time - start_time

print(f"\nGA Total Cost (USD): {best_cost:.1f}\n")
for i in range(n_flights):
    f = df.loc[i]
    print(f"Uçuş {i}: {f['origin']} → {f['destination']} ({f['dep_time']} - {f['arr_time']}) → Uçak {best_solution[i]}")

print(f"\nÇözüm Süresi: {duration:.2f} seconds")



