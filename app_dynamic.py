import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

import ql_bookings_dynamic_final as ql

st.set_page_config(layout="wide")

st.title("🚀 Smart Route Optimizer (Dynamic Environment)")

# =========================
# LOAD DATA (ONLY FOR UI)
# =========================
df = pd.read_csv("bookings3.csv")
df.columns = df.columns.str.strip()

cities = sorted(set(df['Pickup Location']).union(set(df['Drop Location'])))

# =========================
# INPUT
# =========================
col1, col2 = st.columns(2)

start = col1.selectbox("🟢 Source", cities)
goal  = col2.selectbox("🔴 Destination", cities)

# =========================
# GRAPH PLACE (ALWAYS SHOW)
# =========================
graph_placeholder = st.empty()

def draw_graph(G, path=None, event_map=None):
    fig, ax = plt.subplots(figsize=(8,5))
    pos = nx.spring_layout(G, seed=42)

    colors = []
    for u, v in G.edges():
        if event_map:
            evt = event_map.get((u,v), event_map.get((v,u),"CLEAR"))

            if evt == "BLOCKED":
                colors.append("red")
            elif evt == "TRAFFIC":
                colors.append("orange")
            elif evt == "WEATHER":
                colors.append("purple")
            else:
                colors.append("gray")
        else:
            colors.append("gray")

    nx.draw(G, pos, edge_color=colors, node_size=200, ax=ax)

    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges,
                               width=4, edge_color="green", ax=ax)

    nx.draw_networkx_nodes(G, pos, nodelist=[start], node_color="green", node_size=400)
    nx.draw_networkx_nodes(G, pos, nodelist=[goal], node_color="red", node_size=400)

    nx.draw_networkx_labels(G, pos, font_size=6)

    ax.axis("off")
    return fig

# Initial graph
_, _, _, G = ql.run_dynamic_route(start, goal)
graph_placeholder.pyplot(draw_graph(G))

# =========================
# BUTTON
# =========================
if st.button("🚀 Find Route"):

    path, dist, event_map, G = ql.run_dynamic_route(start, goal)

    if path is None:
        st.error("❌ No path found")
    else:
        st.success("✅ Route Found")

        st.write(f"📍 Path: {' → '.join(path)}")
        st.write(f"📏 Distance: {dist:.2f} km")

        fig = draw_graph(G, path, event_map)
        graph_placeholder.pyplot(fig)

        st.subheader("⚡ Conditions")
        st.write("🔴 Blocked | 🟠 Traffic | 🟣 Weather | 🟢 Path")
