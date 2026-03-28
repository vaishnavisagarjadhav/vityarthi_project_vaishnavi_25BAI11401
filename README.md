# 🏥 ICU Patient Allocation System

> **Combining Machine Learning + Graph Algorithms to automate critical ICU bed allocation in real time.**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Algorithm](https://img.shields.io/badge/Algorithm-BFS%20%7C%20DFS-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Working%20Prototype-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 📌 Overview

This project is a **decision-support system** for hospital ICU management built as part of the *Fundamentals of AI & ML* course (B.Tech CSE AI & ML, 1st Year).

Given a patient's vitals, the system:
1. **Predicts severity** (Low / Medium / Critical) using a trained **Decision Tree classifier**
2. If critical — **finds the nearest available ICU bed** using **BFS** through a hospital graph
3. **Lists all available ICU options** using **DFS** for staff reference
4. **Marks the allocated bed as occupied** to prevent double-booking

---

## 🧠 Concepts Used

| Concept | Implementation |
|---|---|
| Supervised ML | `DecisionTreeClassifier` from scikit-learn |
| Graph Representation | Adjacency list (`dict`) |
| BFS | Nearest ICU — shortest path guaranteed |
| DFS | All available ICU paths — complete exploration |
| Data Structures | `deque` for BFS queue, `set` for visited tracking |

---

## 🗂️ Project Structure

```
icu-allocation/
│
├── icu_allocation.py      # Main system (ML + BFS + DFS integrated)
└── README.md              # You are here
```

---

## 🏗️ Hospital Graph Layout

```
Entrance
   ├── Ward_A
   │     ├── ICU_1  ✅ Available
   │     └── ICU_2  ❌ Occupied
   └── Ward_B
         └── ICU_3  ✅ Available
```

The hospital is modelled as a **directed graph** (adjacency list). BFS traverses this graph level by level from the Entrance to guarantee the shortest path to a free ICU bed.

---

## ⚙️ How It Works

### Step 1 — Severity Prediction (ML)

Three patient vitals are fed into a trained Decision Tree:

```python
features = [age, heart_rate, spo2]
# Output: 0 = Low | 1 = Medium | 2 = Critical
```

### Step 2 — ICU Allocation (BFS)

If severity is **Critical**, BFS starts from the hospital Entrance and expands level by level until it finds the first available ICU bed:

```python
def bfs_find_icu(start):
    queue = deque([(start, [start])])
    while queue:
        node, path = queue.popleft()
        if node in icu_beds and icu_beds[node]:
            return node, path   # ← nearest available ICU
        for neighbor in graph[node]:
            ...
```

### Step 3 — All Options (DFS)

DFS explores every branch recursively and returns **all** reachable available ICUs — useful for staff to see the full picture:

```python
def dfs_all_icu(start, visited=None, path=None):
    if start in icu_beds and icu_beds[start]:
        results.append((start, path.copy()))   # ← collect, don't stop
    for neighbor in graph[start]:
        ...
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install scikit-learn numpy
```

### Run

```bash
python icu_allocation.py
```

### Sample Run

```
Enter patient details:
Age: 70
Heart Rate: 120
SpO2: 80

Predicted Severity: Critical

Allocated ICU: ICU_1
Path: Entrance → Ward_A → ICU_1

All available ICU paths (DFS):
ICU_3: Entrance → Ward_B → ICU_3
```

---

## 🧪 Test Cases

| Age | Heart Rate | SpO2 | Predicted Severity | ICU Allocated |
|-----|-----------|------|--------------------|---------------|
| 70  | 120       | 80   | Critical           | ICU_1         |
| 25  | 80        | 98   | Low                | General Ward  |
| 45  | 110       | 85   | Medium             | General Ward  |
| 50  | 100       | 88   | Critical           | ICU_1 (or next available) |

---

## 📊 BFS vs DFS — Quick Comparison

| Property | BFS | DFS |
|---|---|---|
| Data structure | Queue (`deque`) | Call stack (recursion) |
| Finds shortest path? | ✅ Yes | ❌ No |
| Finds all options? | ❌ Stops at first | ✅ Yes |
| Used here for | Bed allocation | Listing all options |
| Time complexity | O(V + E) | O(V + E) |

---

## ⚠️ Limitations

- Training dataset is very small (6 samples) — model will overfit
- Hospital graph is hardcoded — no live database connection
- No persistent storage — ICU status resets on restart
- Only 3 features used — real triage uses many more vitals

---

## 🔮 Future Scope

- [ ] Train on real clinical dataset (thousands of records)
- [ ] Add more vitals: blood pressure, temperature, respiratory rate
- [ ] Connect to live hospital bed management system
- [ ] Replace BFS with **Dijkstra / A\*** for weighted hospital graphs
- [ ] Add a priority waitlist when all ICUs are full
- [ ] Build a web UI with Flask or Django

---

## 📚 References

- Géron, A. — *Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow*
- Cormen et al. — *Introduction to Algorithms (CLRS)*
- [scikit-learn Decision Tree docs](https://scikit-learn.org/stable/modules/tree.html)
- [Python collections.deque docs](https://docs.python.org/3/library/collections.html#collections.deque)

---

## 👤 Author

**[Your Name]**
B.Tech CSE (AI & ML), 1st Year
[Your College Name]

---

