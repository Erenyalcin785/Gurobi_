from gurobipy import Model, GRB
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

df = df.head(30)      # İlk 30 uçuş
n_flights = len(df)
max_planes = 8         # En fazla 8 uçak kullanılabilir

conflict = {}
for i in range(n_flights):
    for k in range(i + 1, n_flights):
        a_start, a_end = df.loc[i, "dep_min"], df.loc[i, "arr_min"]
        b_start, b_end = df.loc[k, "dep_min"], df.loc[k, "arr_min"]
        if not (a_end <= b_start or b_end <= a_start):
            conflict[(i, k)] = True

# === E. Gurobi Modeli Kur ===
model = Model("FlightAssignment")
model.setParam("OutputFlag", 0)  # Konsol çıktısını kapatmak için

x = {}
for i in range(n_flights):
    for j in range(max_planes):
        x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

y = {}
for j in range(max_planes):
    y[j] = model.addVar(vtype=GRB.BINARY, name=f"y_{j}")

model.update()

# === F. Amaç Fonksiyonu ===
model.setObjective(
    sum(df.loc[i, "price"] * x[i, j] for i in range(n_flights) for j in range(max_planes)),
    GRB.MINIMIZE
)

# === G. Kısıtlar ===

# Her uçuş tam 1 uçağa atanmalı
for i in range(n_flights):
    model.addConstr(sum(x[i, j] for j in range(max_planes)) == 1)

# Çakışan uçuşlar aynı uçağa atanamaz
for (i, k) in conflict:
    for j in range(max_planes):
        model.addConstr(x[i, j] + x[k, j] <= 1)

# Uçuş atanan uçak aktif sayılır
for i in range(n_flights):
    for j in range(max_planes):
        model.addConstr(x[i, j] <= y[j])

start = time.time()
model.optimize()
end = time.time()

if model.status == GRB.OPTIMAL:
    print(f"\nGurobi Toplam Maliyet (USD): {model.ObjVal}\n")
    for i in range(n_flights):
        for j in range(max_planes):
            if x[i, j].X > 0.5:
                flight_info = f"{df.loc[i, 'origin']} → {df.loc[i, 'destination']} ({df.loc[i, 'dep_time']} - {df.loc[i, 'arr_time']})"
                print(f"Uçuş {i}: {flight_info} → Uçak {j}")
    print(f"\nÇözüm Süresi: {end - start:.2f} saniye")
else:
    print("Optimal çözüm bulunamadı.")

