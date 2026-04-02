import streamlit as st
import pandas as pd
import ql_bookings_dynamic_final as ql

st.set_page_config(layout="wide")

st.title("🚀 Smart Route Optimizer")

# ✅ Load only data (light)
df = pd.read_csv("bookings3.csv")

cities = sorted(set(df['Pickup Location']).union(set(df['Drop Location'])))

col1, col2 = st.columns(2)
start = col1.selectbox("🟢 Source", cities)
goal  = col2.selectbox("🔴 Destination", cities)

# 🚀 ONLY run heavy logic on button click
if st.button("🚀 Find Route"):

    with st.spinner("Calculating route..."):

        path, dist, fig = ql.run_dynamic_route(start, goal, df)

    st.success("✅ Route Found")

    st.write(f"📏 Distance: {dist:.2f} km")
    st.write(f"📍 Path: {' → '.join(path)}")

    st.pyplot(fig)
