import pandas as pd
import random
import math
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

df = df.head(30)        #  30 uçuş
max_planes = 8          #  8 uçak
n_flights = len(df)

conflict = {}
for i in range(n_flights):
    for k in range(i + 1, n_flights):
        a_start, a_end = df.loc[i, "dep_min"], df.loc[i, "arr_min"]
        b_start, b_end = df.loc[k, "dep_min"], df.loc[k, "arr_min"]
        if not (a_end <= b_start or b_end <= a_start):
            conflict[(i, k)] = True

# === Geçerli bir çözüm üret ===
def generate_valid_solution():
    assignment = [-1] * n_flights
    for i in range(n_flights):
        for _ in range(100):  # Rastgele deneyerek uygun uçak bul
            plane = random.randint(0, max_planes - 1)
            conflict_free = True
            for j in range(n_flights):
                if assignment[j] == plane and ((i, j) in conflict or (j, i) in conflict):
                    conflict_free = False
                    break
            if conflict_free:
                assignment[i] = plane
                break
        if assignment[i] == -1:
            return None  # Geçerli atama bulunamadı
    return assignment

def cost(solution):
    return sum(df.loc[i, "price"] for i in range(n_flights) if solution[i] != -1)

# === Komşu çözüm üret ===
def neighbor(solution):
    new = solution.copy()
    i = random.randint(0, n_flights - 1)
    new[i] = random.randint(0, max_planes - 1)
    return new

def is_valid(solution):
    for (i, k) in conflict:
        if solution[i] == solution[k]:
            return False
    return all(p != -1 for p in solution)

# === Simulated Annealing Algoritması ===
def simulated_annealing():
    T = 1000
    T_min = 1
    alpha = 0.95
    current = generate_valid_solution()
    while current is None:
        current = generate_valid_solution()
    best = current
    best_cost = cost(current)

    while T > T_min:
        for _ in range(100):
            next_sol = neighbor(current)
            if not is_valid(next_sol):
                continue
            delta = cost(next_sol) - cost(current)
            if delta < 0 or random.random() < math.exp(-delta / T):
                current = next_sol
                if cost(current) < best_cost:
                    best = current
                    best_cost = cost(current)
        T *= alpha
    return best, best_cost

start = time.time()
solution, total_cost = simulated_annealing()
end = time.time()

print(f"\nSA Toplam Maliyet (USD): {total_cost}\n")

for i in range(n_flights):
    plane = solution[i]
    info = f"{df.loc[i, 'origin']} → {df.loc[i, 'destination']} ({df.loc[i, 'dep_time']} - {df.loc[i, 'arr_time']})"
    print(f"Uçuş {i}: {info} → Uçak {plane}")

print(f"\nÇözüm Süresi: {end - start:.2f} saniye")


