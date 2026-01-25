import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from hijri_converter import Gregorian

st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --- Select Group and Start Date ---
groups = ["A", "B", "C", "D"]
default_group_index = groups.index("B")
group = st.selectbox("Select Group:", groups, index=default_group_index)

start_date = st.date_input("Select Start Date:", datetime(2026, 1, 25))
st.write("Selected Group:", group)
st.write("Start Date:", start_date.strftime("%d-%m-%Y"))

# --- Create the annual schedule ---
schedule = []

# Function to add shifts
def add_shifts(start, shift_type, days):
    colors = {
        "Morning": "lightyellow",
        "Evening": "lightsalmon",
        "Night": "lightblue",
        "Off": "lightgray"
    }
    for i in range(days):
        date = start + timedelta(days=i)
        hijri_date = Gregorian(date.year, date.month, date.day).to_hijri()
        hijri_str = f"{hijri_date.day}-{hijri_date.month}-{hijri_date.year}"
        schedule.append({
            "Gregorian": date.strftime("%d-%m-%Y"),
            "Hijri": hijri_str,
            "Shift": shift_type,
            "Color": colors[shift_type]
        })

# Build the schedule for 1 year
current_date = start_date
while current_date < start_date + timedelta(days=365):
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

# Convert to DataFrame
df = pd.DataFrame(schedule)

# --- Highlight rows by shift ---
def color_rows(row):
    return [f"background-color: {row['Color']}"] * len(row)

# --- Display the schedule ---
st.dataframe(df.style.apply(color_rows, axis=1), use_container_width=True)

# --- Allow checking shift by date ---
check_date = st.date_input("Check your shift for a specific date:")
if check_date:
    match = df[df["Gregorian"] == check_date.strftime("%d-%m-%Y")]
    if not match.empty:
        shift = match.iloc[0]["Shift"]
        hijri = match.iloc[0]["Hijri"]
        st.success(f"Your shift on {check_date.strftime('%d-%m-%Y')} (Hijri {hijri}) is: {shift}")
    else:
        st.warning("No shift found for this date.")
