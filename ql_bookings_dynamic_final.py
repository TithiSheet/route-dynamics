# Generated from: ql_bookings_dynamic_final (1).ipynb
# Converted at: 2026-03-20T12:36:19.231Z
# Next step (optional): refactor into modules & generate tests with RunCell
# Quick start: pip install runcell

''' import random
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

df = pd.read_csv("bookings3.csv")   
# Clean: convert and drop null distances
df['Ride Distance'] = pd.to_numeric(df['Ride Distance'], errors='coerce')
df = df.dropna(subset=['Ride Distance'])
df.head(20)


# Create list of unique locations
cities      = sorted(set(df["Pickup Location"]).union(set(df["Drop Location"])))
city_to_idx = {city: i for i, city in enumerate(cities)}
idx_to_city = {i: city for city, i in city_to_idx.items()}

# Initialize adjacency matrix
n = len(cities)
distance_matrix = np.full((n, n), np.inf)
np.fill_diagonal(distance_matrix, 0)


# Fill adjacency matrix
# Where multiple rides exist between two locations, keep minimum distance
for _, row in df.iterrows():
    i = city_to_idx[row["Pickup Location"]]
    j = city_to_idx[row["Drop Location"]]
    d = row["Ride Distance"]
    if d < distance_matrix[i, j]:
        distance_matrix[i, j] = d
        distance_matrix[j, i] = d

# Q-Learning setup
Q = np.zeros((n, n))

alpha    = 0.8     # Learning rate
gamma    = 0.95    # Discount factor
epsilon  = 0.4     # Initial exploration rate
episodes = 15000   # Training episodes
max_steps = 300    # Prevent infinite loops

print(f"Locations loaded : {n}")
print(f"Routes loaded    : {(distance_matrix != np.inf).sum() // 2}")


def valid_actions(state):
    return [i for i in range(n) if distance_matrix[state, i] != np.inf and i != state]

def train_q_learning(start_city, goal_city):
    """Train Q-Learning agent on the base distance matrix.
    Learns the shortest path through trial and error.
    Reward: +1000 on reaching goal, -dist-1 per step.
    Policy: epsilon-greedy with linear epsilon decay.
    """
    global Q
    Q = np.zeros((n, n))   # reset Q-table for fresh training

    start = city_to_idx[start_city]
    goal  = city_to_idx[goal_city]

    for ep in range(episodes):
        state = start
        steps = 0
        # Epsilon decays linearly: explore early, exploit later
        eps = max(0.01, epsilon * (1 - ep / episodes))

        while state != goal and steps < max_steps:
            steps  += 1
            actions = valid_actions(state)
            if not actions:
                break

            # Epsilon-greedy action selection
            if random.random() < eps:
                action = random.choice(actions)                    # explore
            else:
                action = max(actions, key=lambda a: Q[state, a])  # exploit

            # Reward shaping
            if action == goal:
                reward = 1000   # big reward for reaching goal
            else:
                reward = -distance_matrix[state, action] - 1  # penalize step cost

            # Bellman Q-update
            next_actions = valid_actions(action)
            future_q     = max([Q[action, a] for a in next_actions], default=0)
            Q[state, action] += alpha * (reward + gamma * future_q - Q[state, action])

            state = action

        if (ep + 1) % 3000 == 0:
            print(f"  Episode {ep+1}/{episodes} complete")


# Extract optimal path
def get_optimal_path(start_city, goal_city):
    """Greedily follow the highest Q-values from start to goal."""
    start = city_to_idx[start_city]
    goal  = city_to_idx[goal_city]

    state          = start
    path           = [start]
    total_distance = 0
    steps          = 0

    while state != goal and steps < max_steps:
        steps   += 1
        actions  = valid_actions(state)
        if not actions:
            break

        # Select the action with the highest Q-value
        action = max(actions, key=lambda a: Q[state, a])
        if len(path) >= 2 and action == path[-2]:
            pass
        path.append(action)
        total_distance += distance_matrix[state, action]
        state = action

    return [idx_to_city[i] for i in path], total_distance
import networkx as nx
import matplotlib.pyplot as plt

def visualize_network_with_path(optimal_path, total_distance, start_city, goal_city):
    # Create a graph
    G = nx.Graph()

    # Add nodes
    for city in cities:
        G.add_node(city)

    # Add edges with distances as weights
    for _, row in df.iterrows():
        G.add_edge(row["Pickup Location"], row["Drop Location"], weight=row["Ride Distance"])

    # Visualize the graph
    pos = nx.spring_layout(G, seed=170)  # for consistent layout

    plt.figure(figsize=(12, 8))

    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="skyblue")

    # Highlight nodes in the optimal path
    path_nodes = optimal_path
    nx.draw_networkx_nodes(G, pos, nodelist=path_nodes, node_size=800,
                            node_color="lightgreen", edgecolors='black', linewidths=1)

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color="gray")

    # Highlight optimal path edges
    path_edges = list(zip(optimal_path, optimal_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2.5, edge_color="red")

    # Add labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")

    plt.title(f"Network of Locations with Optimal Path from {start_city} to {goal_city}")
    plt.axis("off")
    plt.show()


# Define start and goal locations
start_city = "AIIMS"
goal_city  = "Anand Vihar"

# Train Q-Learning agent
print(f"Training Q-Learning agent: {start_city} -> {goal_city}")
train_q_learning(start_city, goal_city)

# Get the optimal path and distance
path, dist = get_optimal_path(start_city, goal_city)

print(f"Optimal Path from {start_city} to {goal_city}: {path}")
print(f"Total Distance: {dist:.2f} km")

# Visualize the network with the optimal path and highlighted locations
visualize_network_with_path(path, dist, start_city, goal_city)


# ---
# ## Dynamic Environment — Q-Learning Agent
# > Change `START_CITY` and `GOAL_CITY` to explore any route!
# 
# 


# =====================================================
#   CHANGE ONLY THESE TWO LOCATIONS
# =====================================================

START_CITY = "AIIMS"          # <-- Change me!
GOAL_CITY  = "Anand Vihar"    # <-- Change me!

import pandas as pd
_df = pd.read_csv("bookings3.csv")
_df['Ride Distance'] = pd.to_numeric(_df['Ride Distance'], errors='coerce')
_df = _df.dropna(subset=['Ride Distance'])
_cities = sorted(set(_df['Pickup Location']).union(set(_df['Drop Location'])))
print("Available locations:")
print(", ".join(_cities))
print(f"\nSelected:  {START_CITY}  ->  {GOAL_CITY}")


# =====================================================
# Q-LEARNING AGENT — DYNAMIC ENVIRONMENT
# Learns to avoid: Blockage, Heavy Crowd,
#                  Road Work, Bad Weather
# Pure Reinforcement Learning — no Dijkstra, no BFS
# =====================================================
import random
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from copy import deepcopy
from collections import Counter, defaultdict

random.seed(42)
np.random.seed(42)

# -- Load data --
df          = pd.read_csv("bookings3.csv")
df['Ride Distance'] = pd.to_numeric(df['Ride Distance'], errors='coerce')
df          = df.dropna(subset=['Ride Distance'])
cities      = sorted(set(df['Pickup Location']).union(set(df['Drop Location'])))
city_to_idx = {city: i for i, city in enumerate(cities)}
idx_to_city = {i: city for city, i in city_to_idx.items()}
n           = len(cities)

assert START_CITY in city_to_idx, f"'{START_CITY}' not in dataset!"
assert GOAL_CITY  in city_to_idx, f"'{GOAL_CITY}' not in dataset!"
assert START_CITY != GOAL_CITY,   "Start and Goal must be different!"

# -- Build base distance matrix --
# Keep minimum distance for duplicate location pairs
base_dm = np.full((n, n), np.inf)
np.fill_diagonal(base_dm, 0)
for _, row in df.iterrows():
    i = city_to_idx[row['Pickup Location']]
    j = city_to_idx[row['Drop Location']]
    d = row['Ride Distance']
    if d < base_dm[i, j]:
        base_dm[i, j] = d
        base_dm[j, i] = d

# Unique edges list
edges = [(i, j) for i in range(n) for j in range(i+1, n) if base_dm[i, j] != np.inf]

# -- Dynamic event types --
EVENTS = {
    'CLEAR':       {'color': '#A8D5A2', 'cost_mult': 1.0,    'label': 'Clear Route'},
    'HEAVY_CROWD': {'color': '#FFD700', 'cost_mult': 1.8,    'label': 'Heavy Crowd (+80%)'},
    'ROAD_WORK':   {'color': '#FF8C00', 'cost_mult': 2.2,    'label': 'Road Work (+120%)'},
    'WEATHER':     {'color': '#6BAED6', 'cost_mult': 1.5,    'label': 'Bad Weather (+50%)'},
    'BLOCKAGE':    {'color': '#CC0000', 'cost_mult': np.inf, 'label': 'Route Blocked'},
}

# -- Randomly assign events to routes (seed=42 for reproducibility) --
def generate_events(edges, blockage_prob=0.12, event_prob=0.30, seed=42):
    random.seed(seed)
    emap = {}
    for i, j in edges:
        r = random.random()
        if   r < blockage_prob:
            emap[(i, j)] = 'BLOCKAGE'
        elif r < blockage_prob + event_prob:
            emap[(i, j)] = random.choice(['HEAVY_CROWD', 'ROAD_WORK', 'WEATHER'])
        else:
            emap[(i, j)] = 'CLEAR'
    return emap

edge_event = generate_events(edges)
evt_counts = Counter(edge_event.values())

# -- Build dynamic cost matrix --
# Blocked routes  -> cost = inf (agent cannot use these)
# Other events    -> cost = base_distance x multiplier
# Q-Learning learns to avoid high-cost routes through reward shaping
dyn_dm = deepcopy(base_dm)
for (i, j), evt in edge_event.items():
    mult = EVENTS[evt]['cost_mult']
    dyn_dm[i, j] = np.inf if mult == np.inf else base_dm[i, j] * mult
    dyn_dm[j, i] = np.inf if mult == np.inf else base_dm[j, i] * mult

# -- Q-Learning: train on dynamic matrix --
# BLOCKED edges are inf -> valid_actions() never returns them
# HEAVY_CROWD / ROAD_WORK / WEATHER -> large negative reward
# -> Bellman update drives Q[s,a] low for bad routes
# -> Agent learns to prefer CLEAR routes automatically
def train_q_learning(sc, gc, dm,
                     episodes=15000,
                     alpha=0.8,
                     gamma=0.95,
                     eps0=0.4):
    s, g = city_to_idx[sc], city_to_idx[gc]
    Q    = np.zeros((n, n))

    def valid_actions(x):
        return [i for i in range(n) if dm[x, i] != np.inf and i != x]

    for ep in range(episodes):
        state   = s
        steps   = 0
        epsilon = max(0.01, eps0 * (1 - ep / episodes))  # decay exploration

        while state != g and steps < 300:
            steps += 1
            acts  = valid_actions(state)
            if not acts:
                break

            # Epsilon-greedy: explore or exploit
            if random.random() < epsilon:
                action = random.choice(acts)                    # explore
            else:
                action = max(acts, key=lambda a: Q[state, a])  # exploit

            # Reward: +5000 at goal, penalize distance per step
            reward   = 5000 if action == g else -dm[state, action] / 50

            # Bellman Q-update
            future_q = max([Q[action, a] for a in valid_actions(action)], default=0)
            Q[state, action] += alpha * (reward + gamma * future_q - Q[state, action])
            state = action

    return Q

# -- Extract path by greedily following Q-values --
def extract_path(Q, sc, gc, dm):
    s, g    = city_to_idx[sc], city_to_idx[gc]
    state   = s
    path    = [s]
    visited = {s}
    steps   = 0

    def valid_actions(x):
        return [i for i in range(n) if dm[x, i] != np.inf and i != x]

    while state != g and steps < 300:
        steps += 1
        acts  = valid_actions(state)
        if not acts:
            break
        pool   = [a for a in acts if a not in visited] or acts
        action = max(pool, key=lambda a: Q[state, a])
        path.append(action)
        visited.add(action)
        state = action

    return [idx_to_city[i] for i in path]

# -- Train & get path --
print(f"Training Q-Learning agent on dynamic environment...")
print(f"Route: {START_CITY}  ->  {GOAL_CITY}")
Q_agent = train_q_learning(START_CITY, GOAL_CITY, dyn_dm)
path    = extract_path(Q_agent, START_CITY, GOAL_CITY, dyn_dm)
km      = sum(base_dm[city_to_idx[path[i]], city_to_idx[path[i+1]]] for i in range(len(path)-1))

print(f"\nQ-Agent Path : {' -> '.join(path)}")
print(f"Distance     : {km:.2f} km")
print(f"Event Summary: {dict(evt_counts)}")

# =====================================================
# GRAPH — DYNAMIC ENVIRONMENT
# =====================================================
G = nx.Graph()
for city in cities:
    G.add_node(city)
for i, j in edges:
    G.add_edge(idx_to_city[i], idx_to_city[j], weight=base_dm[i, j])

pos     = nx.spring_layout(G, seed=170)
ped     = list(zip(path, path[1:]))
ped_set = set(map(frozenset, ped))

# Group edges by event type for fast batch drawing
edges_by_evt = defaultdict(list)
for i, j in edges:
    evt = edge_event.get((i, j), 'CLEAR')
    edges_by_evt[evt].append((idx_to_city[i], idx_to_city[j]))

fig, ax = plt.subplots(figsize=(18, 12))
fig.patch.set_facecolor('#0d0d1a')
ax.set_facecolor('#0d0d1a')

# Draw all edges colored by event type (batch per condition for speed)
for evt, elist in edges_by_evt.items():
    non_path = [(u, v) for u, v in elist if frozenset([u, v]) not in ped_set]
    if non_path:
        nx.draw_networkx_edges(G, pos, edgelist=non_path,
            width=3.0 if evt == 'BLOCKAGE' else 1.4,
            edge_color=EVENTS[evt]['color'],
            style='dashed' if evt == 'BLOCKAGE' else 'solid',
            alpha=0.80, ax=ax)

# Draw Q-Agent rerouted path in bright green
nx.draw_networkx_edges(
    G, pos, edgelist=ped,
    width=7, edge_color='#00FF7F', ax=ax
)

# Node colors
nc = [
    '#00FF00' if c == START_CITY else
    '#FF3333' if c == GOAL_CITY  else
    '#00BFFF' if c in path       else
    '#2d2d50'
    for c in G.nodes()
]
ns = [
    900 if (c == START_CITY or c == GOAL_CITY) else
    650 if c in path else 350
    for c in G.nodes()
]
nx.draw_networkx_nodes(G, pos, node_color=nc, node_size=ns,
                        ax=ax, edgecolors='white', linewidths=0.6)
nx.draw_networkx_labels(G, pos, font_size=6.5,
                         font_color='white', font_weight='bold', ax=ax)

ax.set_title(
    f"DYNAMIC ENVIRONMENT  |  {START_CITY}  ->  {GOAL_CITY}\n"
    f"Q-Agent Path: {' -> '.join(path)}  |  {km:.2f} km",
    fontsize=13, color='white', fontweight='bold', pad=14
)
ax.axis('off')

ax.legend(
    handles=[
        mpatches.Patch(color='#CC0000', label=f"Route Blocked    ({evt_counts.get('BLOCKAGE',    0)}) - Impassable"),
        mpatches.Patch(color='#FFD700', label=f"Heavy Crowd      ({evt_counts.get('HEAVY_CROWD', 0)}) - +80% cost"),
        mpatches.Patch(color='#FF8C00', label=f"Road Work        ({evt_counts.get('ROAD_WORK',   0)}) - +120% cost"),
        mpatches.Patch(color='#6BAED6', label=f"Bad Weather      ({evt_counts.get('WEATHER',     0)}) - +50% cost"),
        mpatches.Patch(color='#A8D5A2', label=f"Clear Route      ({evt_counts.get('CLEAR',       0)})"),
        mpatches.Patch(color='#00FF7F', label=f"Q-Agent Path     ({km:.2f} km)"),
        mpatches.Patch(color='#00FF00', label=f"Start: {START_CITY}"),
        mpatches.Patch(color='#FF3333', label=f"Goal:  {GOAL_CITY}"),
    ],
    loc='lower left', fontsize=9,
    facecolor='#1a1a3a', edgecolor='white', labelcolor='white'
)

plt.tight_layout()
plt.savefig(f"dynamic_env_{START_CITY}_to_{GOAL_CITY}.png",
            dpi=150, bbox_inches='tight', facecolor='#0d0d1a')
plt.show()



def run_dynamic_route(start_city, goal_city, df):

    import numpy as np
    import random
    import matplotlib.pyplot as plt
    from collections import Counter

    # =========================
    # PREPARE DATA (same as your code)
    # =========================
    cities = sorted(set(df['Pickup Location']).union(set(df['Drop Location'])))
    city_to_idx = {city: i for i, city in enumerate(cities)}
    idx_to_city = {i: city for city, i in city_to_idx.items()}
    n = len(cities)

    base_dm = np.full((n, n), np.inf)
    np.fill_diagonal(base_dm, 0)

    for _, row in df.iterrows():
        i = city_to_idx[row['Pickup Location']]
        j = city_to_idx[row['Drop Location']]
        d = row['Ride Distance']

        if d < base_dm[i, j]:
            base_dm[i, j] = d
            base_dm[j, i] = d

    edges = [(i, j) for i in range(n) for j in range(i+1, n) if base_dm[i, j] != np.inf]

    # =========================
    # EVENTS
    # =========================
    def generate_events():
        emap = {}
        for i, j in edges:
            r = random.random()
            if r < 0.1:
                emap[(i, j)] = 'BLOCKAGE'
            elif r < 0.3:
                emap[(i, j)] = 'TRAFFIC'
            else:
                emap[(i, j)] = 'CLEAR'
        return emap

    event_map = generate_events()
    dyn_dm = base_dm.copy()

    for (i, j), evt in event_map.items():
        if evt == 'BLOCKAGE':
            dyn_dm[i, j] = np.inf
            dyn_dm[j, i] = np.inf
        elif evt == 'TRAFFIC':
            dyn_dm[i, j] *= 1.5
            dyn_dm[j, i] *= 1.5

    # =========================
    # Q LEARNING
    # =========================
    Q = np.zeros((n, n))

    def valid_actions(s):
        return [i for i in range(n) if dyn_dm[s, i] != np.inf and i != s]
    s = city_to_idx[start_city]
    g = city_to_idx[goal_city]
    for _ in range(500):
        state = s
        while state != g:
            actions = valid_actions(state)
            if not actions:
                break
            action = random.choice(actions)
            reward = 1000 if action == g else -dyn_dm[state, action]
            future = max([Q[action, a] for a in valid_actions(action)], default=0)
            Q[state, action] += 0.8 * (reward + 0.95 * future - Q[state, action])
            state = action
    # =========================
    # PATH
    # =========================
    path_idx = [s]
    state = s
    while state != g:
        actions = valid_actions(state)
        if not actions:
            break
        action = max(actions, key=lambda a: Q[state, a])
        path_idx.append(action)
        state = action
    path = [idx_to_city[i] for i in path_idx]
    dist = 0
    for i in range(len(path)-1):
        dist += base_dm[city_to_idx[path[i]], city_to_idx[path[i+1]]]
    # =========================
    # GRAPH FIGURE
    # =========================
    import networkx as nx
    G = nx.Graph()
    for city in cities:
        G.add_node(city)
    for i, j in edges:
        G.add_edge(idx_to_city[i], idx_to_city[j])
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(8,6))
    nx.draw(G, pos, node_size=50, ax=ax)
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)
    return path, dist, fig '''

import streamlit as st
import pandas as pd
import networkx as nx
import random
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("🚀 Smart Route Optimizer (Dynamic Environment)")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(
        "bookings3.csv",
        encoding="latin1",
        on_bad_lines="skip",
        engine="python"
    )

    df.columns = df.columns.str.strip()
    df['Ride Distance'] = pd.to_numeric(df['Ride Distance'], errors='coerce')
    df = df.dropna(subset=['Ride Distance', 'Pickup Location', 'Drop Location'])

    return df

df = load_data()

if df.empty:
    st.error("❌ Data not loaded")
    st.stop()

# =========================
# BUILD GRAPH
# =========================
@st.cache_resource
def build_graph(df):
    G = nx.Graph()

    for _, row in df.iterrows():
        u = row['Pickup Location']
        v = row['Drop Location']
        d = row['Ride Distance']

        if G.has_edge(u, v):
            if d < G[u][v]['weight']:
                G[u][v]['weight'] = d
        else:
            G.add_edge(u, v, weight=d)

    return G

G = build_graph(df)

cities = sorted(set(df['Pickup Location']).union(set(df['Drop Location'])))

# =========================
# UI INPUT
# =========================
col1, col2 = st.columns(2)

start = col1.selectbox("🟢 Source", cities)
goal = col2.selectbox("🔴 Destination", cities)

# =========================
# DYNAMIC CONDITIONS
# =========================
def apply_dynamic_conditions(G):
    temp = G.copy()
    event_map = {}

    for u, v in temp.edges():
        r = random.random()

        if r < 0.05:
            temp.remove_edge(u, v)
            event_map[(u, v)] = "🚧 BLOCKED"
        elif r < 0.20:
            temp[u][v]['weight'] *= 1.5
            event_map[(u, v)] = "🚦 TRAFFIC"
        elif r < 0.30:
            temp[u][v]['weight'] *= 1.3
            event_map[(u, v)] = "🌧 BAD WEATHER"
        else:
            event_map[(u, v)] = "✅ CLEAR"

    return temp, event_map

# =========================
# FIXED COORDS (NO BLINK)
# =========================
random.seed(42)
coords = {city: (random.uniform(20, 28), random.uniform(70, 88)) for city in cities}

# =========================
# BUTTON
# =========================
if st.button("🚀 Find Optimal Route"):

    temp_G, event_map = apply_dynamic_conditions(G)

    try:
        path = nx.shortest_path(temp_G, start, goal, weight='weight')
        dist = nx.shortest_path_length(temp_G, start, goal, weight='weight')
    except:
        st.error("❌ No route available due to conditions")
        st.stop()

    # =========================
    # RESULT
    # =========================
    st.success("✅ Optimal Route Found")

    stops = len(path) - 1
    time = (dist / 40) * 60

    st.write(f"📍 Path: {' → '.join(path)}")
    st.write(f"📏 Distance: {dist:.2f} km")
    st.write(f"🛑 Stops: {stops}")
    st.write(f"⏱️ Time: {time:.0f} mins")

    # =========================
    # GRAPH (ONLY ROUTE + NEARBY)
    # =========================
    st.subheader("📊 Route Graph with Dynamic Conditions")

    fig, ax = plt.subplots(figsize=(6, 4))

    sub_nodes = set(path)
    sub_G = G.subgraph(sub_nodes)

    pos = nx.spring_layout(sub_G, seed=42)

    edge_colors = []
    for u, v in sub_G.edges():
        event = event_map.get((u, v), "CLEAR")

        if "BLOCKED" in event:
            edge_colors.append("red")
        elif "TRAFFIC" in event:
            edge_colors.append("orange")
        elif "WEATHER" in event:
            edge_colors.append("purple")
        else:
            edge_colors.append("green")

    nx.draw(
        sub_G,
        pos,
        with_labels=True,
        node_color="skyblue",
        edge_color=edge_colors,
        node_size=800,
        font_size=8,
        ax=ax
    )

    st.pyplot(fig)

    # =========================
    # MAP
    # =========================
    st.subheader("🗺️ Route Map")

    m = folium.Map(location=coords[start], zoom_start=6)

    route_coords = [coords[c] for c in path]

    folium.PolyLine(route_coords, color="blue", weight=5).add_to(m)

    folium.Marker(coords[start], popup=start, icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(coords[goal], popup=goal, icon=folium.Icon(color="red")).add_to(m)

    st_folium(m, width=900, height=500)

    # =========================
    # EVENT LEGEND
    # =========================
    st.subheader("⚡ Dynamic Conditions Legend")

    st.write("🔴 Red = Blocked Road")
    st.write("🟠 Orange = Heavy Traffic")
    st.write("🟣 Purple = Bad Weather")
    st.write("🟢 Green = Clear Road")










