import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date

st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# ---- GROUP START DATES (ALL START WITH NIGHT) ----
today = date.today()

group_start_dates = {
    "A": date(2026, 1, 1),
    "B": date(2026, 1, 18),
    "C": today,          # Group C starts TODAY on Night
    "D": date(2026, 2, 1)
}

groups = ["A", "B", "C", "D"]
default_group = "B"

group = st.selectbox("Select Group", groups, index=groups.index(default_group))
start_date = group_start_dates[group]

st.write("Group:", group)
st.write("Cycle Start Date:", start_date.strftime("%d-%m-%Y"))

# ---- BUILD SHIFT CYCLE ----
schedule = []

def add_shifts(start, shift_type, days):
    for i in range(days):
        d = start + timedelta(days=i)
        schedule.append({
            "Date": d,
            "Shift": shift_type,
            "Color": {
                "Morning": "#FFF59D",
                "Evening": "#FFCC80",
                "Night": "#81D4FA",
                "Off": "#E0E0E0"
            }[shift_type]
        })

current_date = start_date
end_date = start_date + timedelta(days=365)

while current_date < end_date:
    add_shifts(current_date, "Night", 7)
    current_date += timedelta(days=7)

    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)

    add_shifts(current_date, "Evening", 7)
    current_date += timedelta(days=7)

    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)

    add_shifts(current_date, "Morning", 7)
    current_date += timedelta(days=7)

    add_shifts(current_date, "Off", 3)
    current_date += timedelta(days=3)

# ---- DATAFRAME ----
df = pd.DataFrame(schedule)
df["Date"] = pd.to_datetime(df["Date"])

df_display = df.copy()
df_display["Date"] = df_display["Date"].dt.strftime("%a %d-%m-%Y")

def color_rows(row):
    return [f"background-color: {row['Color']}"] * len(row)

st.dataframe(
    df_display.style.apply(color_rows, axis=1),
    use_container_width=True
)
