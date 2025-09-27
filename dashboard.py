import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px

# --- Simulate Rack Data ---
# Only if 'rack_data.csv' does not exist, generate simulated data
import os
if not os.path.exists("rack_data.csv"):
    racks = ["Rack1", "Rack2", "Rack3", "Rack4"]
    records = []
    for i in range(50):  # 50 time points
        timestamp = datetime.datetime.now() + datetime.timedelta(seconds=i*10)
        for rack in racks:
            power = np.random.randint(200, 500)  # Random power usage in Watts
            records.append([timestamp, rack, power])
    df = pd.DataFrame(records, columns=["timestamp", "rack_id", "power_watts"])
    df.to_csv("rack_data.csv", index=False)
else:
    df = pd.read_csv("rack_data.csv")

df['timestamp'] = pd.to_datetime(df['timestamp'])

# --- Dashboard Title and Description ---
st.title("DCIM Energy Tracker – Rack-Level Monitoring")
st.markdown("""
This dashboard shows the energy consumption of individual server racks in a data center.

- **Power (Watts)**: How much electricity each rack is using.
- **High usage alert**: Racks consuming too much power are highlighted.
""")
st.info("1 Watt = 1 Joule per second. Higher wattage means more energy consumption.")

# --- Sidebar: Rack Selection ---
rack_selected = st.sidebar.selectbox("Select Rack", df['rack_id'].unique())
rack_data = df[df['rack_id'] == rack_selected]

# --- KPI Cards ---
st.subheader("Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Average Power", f"{rack_data['power_watts'].mean():.2f} W")
col2.metric("Max Power", f"{rack_data['power_watts'].max()} W")
col3.metric("Min Power", f"{rack_data['power_watts'].min()} W")

# --- Line Chart for Selected Rack ---
st.subheader(f"Power Usage Over Time – {rack_selected}")
fig_line = px.line(
    rack_data, x='timestamp', y='power_watts',
    labels={"power_watts":"Power (Watts)", "timestamp":"Time"},
    title=f'Power Usage for {rack_selected}'
)
st.plotly_chart(fig_line)

# --- Bar Chart Comparing All Racks ---
st.subheader("Average Power per Rack")
rack_summary = df.groupby('rack_id')['power_watts'].mean().reset_index()
fig_bar = px.bar(
    rack_summary, x='rack_id', y='power_watts', color='power_watts',
    color_continuous_scale=['green','yellow','red'],
    labels={"power_watts":"Average Power (W)", "rack_id":"Rack ID"},
    title="Average Power per Rack"
)
st.plotly_chart(fig_bar)

# --- Alerts Section ---
st.subheader("Alerts")
high_usage = rack_data[rack_data['power_watts'] > 450]  # Threshold example
if not high_usage.empty:
    st.warning(f"Warning: {len(high_usage)} readings above 450 Watts!")
else:
    st.success("All racks are operating within normal power range.")

# --- Latest Readings Table ---
st.subheader("Latest Readings")
st.dataframe(rack_data.tail(10))
