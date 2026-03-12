import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# CONFIG
GROUPS = {
    "B": datetime(2026, 1, 18),
    "C": datetime(2026, 1, 25),
}

ROTATION = [
    ("Night", 7),
    ("OFF", 2),
    ("Evening", 7),
    ("OFF", 2),
    ("Morning", 7),
    ("OFF", 3),
]

def generate_schedule(start_date, days=365):

    schedule = []
    rotation_index = 0
    rotation_day_count = 0
    rotation_type, rotation_length = ROTATION[rotation_index]

    for i in range(days):

        current_date = start_date + timedelta(days=i)

        schedule.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Shift": rotation_type
        })

        rotation_day_count += 1

        if rotation_day_count >= rotation_length:
            rotation_index = (rotation_index + 1) % len(ROTATION)
            rotation_type, rotation_length = ROTATION[rotation_index]
            rotation_day_count = 0

    return pd.DataFrame(schedule)


st.title("Shift Schedule")

group_selected = st.selectbox("Select Group", list(GROUPS.keys()))

df = generate_schedule(GROUPS[group_selected])

selected_date = st.date_input("Choose Date")

result = df[df["Date"] == selected_date.strftime("%Y-%m-%d")]

if not result.empty:
    st.success(f"Your shift: {result.iloc[0]['Shift']}")

st.dataframe(df)
