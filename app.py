import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --------------------
# Group configuration
# --------------------
groups = ["A", "B", "C", "D"]

group_offsets = {
    "A": 0,
    "B": 7,
    "C": 14,  # Group C starts Night today
    "D": 21
}

selected_group = st.selectbox("Select Group", groups, index=groups.index("C"))

today = datetime.today().date()
start_date = st.date_input("Start Date", today)

# --------------------
# Shift cycle
# --------------------
shift_cycle = [
    ("Night", 7),
    ("Off", 2),
    ("Evening", 7),
    ("Off", 2),
    ("Morning", 7),
    ("Off", 3),
]

shift_colors = {
    "Morning": "#FFF59D",
    "Evening": "#FFCC80",
    "Night": "#90CAF9",
    "Off": "#E0E0E0"
}

# --------------------
# Build schedule
# --------------------
schedule = []

cycle_start = start_date - timedelta(days=group_offsets[selected_group])
current_date = cycle_start

while current_date < start_date + timedelta(days=365):
    for shift_name, duration in shift_cycle:
        for i in range(duration):
            day = current_date + timedelta(days=i)
            if day >= start_date:
                schedule.append({
                    "Date": day,
                    "Shift": shift_name,
                    "Color": shift_colors[shift_name]
                })
        current_date += timedelta(days=duration)

# --------------------
# DataFrame
# --------------------
df = pd.DataFrame(schedule)
df["Date"] = pd.to_datetime(df["Date"])
df_display = df.copy()
df_display["Date"] = df_display["Date"].dt.strftime("%a %d-%m-%Y")

def color_rows(row):
    return [f"background-color: {row['Color']}"] * len(row)

st.subheader(f"Group {selected_group} - 1 Year Schedule")
st.dataframe(
    df_display.style.apply(color_rows, axis=1),
    use_container_width=True
)
