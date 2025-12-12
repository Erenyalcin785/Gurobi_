import pandas as pd
import random
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

df = df.head(30)         #  30 uçuş
n_flights = len(df)
max_planes = 8           #  8 uçak

conflict = {}
for i in range(n_flights):
    for k in range(i + 1, n_flights):
        a_start, a_end = df.loc[i, "dep_min"], df.loc[i, "arr_min"]
        b_start, b_end = df.loc[k, "dep_min"], df.loc[k, "arr_min"]
        if not (a_end <= b_start or b_end <= a_start):
            conflict[(i, k)] = True

# === Geçerli başlangıç çözümü üret ===
def generate_valid_solution():
    assignment = [-1] * n_flights
    for i in range(n_flights):
        for _ in range(100):
            plane = random.randint(0, max_planes - 1)
            if all(assignment[j] != plane or not ((i, j) in conflict or (j, i) in conflict) for j in range(n_flights)):
                assignment[i] = plane
                break
        if assignment[i] == -1:
            return None
    return assignment


def cost(sol):
    return sum(df.loc[i, "price"] for i in range(n_flights) if sol[i] != -1)

# === Komşular üret ===
def get_neighbors(sol):
    neighbors = []
    for i in range(n_flights):
        for plane in range(max_planes):
            if plane != sol[i]:
                new_sol = sol.copy()
                new_sol[i] = plane
                if is_valid(new_sol):
                    neighbors.append(new_sol)
    return neighbors

def is_valid(sol):
    for (i, k) in conflict:
        if sol[i] == sol[k]:
            return False
    return all(s != -1 for s in sol)

# === Tabu Search Algoritması ===
def tabu_search(max_iter=150, tabu_tenure=10):
    current = None
    while current is None:
        current = generate_valid_solution()

    best = current[:]
    best_cost = cost(current)
    tabu_list = []

    for _ in range(max_iter):
        neighbors = get_neighbors(current)
        neighbors = [n for n in neighbors if n not in tabu_list]
        if not neighbors:
            break

        next_sol = min(neighbors, key=cost)
        next_cost = cost(next_sol)

        current = next_sol
        tabu_list.append(current)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)

        if next_cost < best_cost:
            best = next_sol
            best_cost = next_cost

    return best, best_cost

start = time.time()
solution, total_cost = tabu_search()
end = time.time()

print(f"\nTS Toplam Maliyet (USD): {total_cost}\n")

for i in range(n_flights):
    plane = solution[i]
    info = f"{df.loc[i, 'origin']} → {df.loc[i, 'destination']} ({df.loc[i, 'dep_time']} - {df.loc[i, 'arr_time']})"
    print(f"Uçuş {i}: {info} → Uçak {plane}")
print(f"\nÇözüm Süresi: {end - start:.2f} saniye")


