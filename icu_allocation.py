from collections import deque
from sklearn.tree import DecisionTreeClassifier
import numpy as np


X = np.array([
    [25, 80, 98],
    [60, 95, 92],
    [45, 110, 85],
    [70, 120, 80],
    [30, 85, 97],
    [50, 100, 88]
])

# Labels: 0 = Low, 1 = Medium, 2 = Critical
y = np.array([0, 1, 1, 2, 0, 2])

model = DecisionTreeClassifier()
model.fit(X, y)

def predict_severity(age, heart_rate, spo2):
    pred = model.predict([[age, heart_rate, spo2]])[0]
    levels = ["Low", "Medium", "Critical"]
    return pred, levels[pred]

graph = {
    "Entrance": ["Ward_A", "Ward_B"],
    "Ward_A": ["ICU_1", "ICU_2"],
    "Ward_B": ["ICU_3"],
    "ICU_1": [],
    "ICU_2": [],
    "ICU_3": []
}

# ICU availability
icu_beds = {
    "ICU_1": True,
    "ICU_2": False,
    "ICU_3": True
}

def bfs_find_icu(start):
    visited = set()
    queue = deque([(start, [start])])

    while queue:
        node, path = queue.popleft()

        if node in icu_beds and icu_beds[node]:
            return node, path

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, []

def dfs_all_icu(start, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    results = []

    if start in icu_beds and icu_beds[start]:
        results.append((start, path.copy()))

    for neighbor in graph[start]:
        if neighbor not in visited:
            results.extend(dfs_all_icu(neighbor, visited, path))

    path.pop()
    visited.remove(start)

    return results

def allocate_icu():
    print("Enter patient details:")

    age = int(input("Age: "))
    heart_rate = int(input("Heart Rate: "))
    spo2 = int(input("SpO2: "))

    severity_num, severity = predict_severity(age, heart_rate, spo2)

    print(f"\nPredicted Severity: {severity}")

    if severity == "Critical":
        icu, path = bfs_find_icu("Entrance")

        if icu:
            print(f"\nAllocated ICU: {icu}")
            print("Path:", " → ".join(path))
            icu_beds[icu] = False  
        else:
            print("No ICU beds available!")

    else:
        print("ICU not required. Send to general ward.")

    print("\nAll available ICU paths (DFS):")
    all_paths = dfs_all_icu("Entrance")
    for icu, path in all_paths:
        print(f"{icu}: {' → '.join(path)}")

allocate_icu()