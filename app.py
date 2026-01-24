import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from hijri_converter import Gregorian

# --- Page config ---
st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --- Select Group ---
groups = ["A", "B", "C", "D"]
default_group_index = groups.index("B")  # Default is B
group = st.selectbox("Select Group:", groups, index=default_group_index)

# --- Select Start Date ---
start_date = st.date_input("Select Start Date:", datetime(2026, 1, 25))
st.write("Selected Group:", group)
st.write("Start Date:", start_date.strftime("%d-%m-%Y"))

# --- Create schedule ---
schedule = []

def add_shifts(start, shift_type, days):
    for i in range(days):
        date = start + timedelta(days=i)
        hijri = Gregorian(date.year, date.month, date.day).to_hijri()
        hijri_str = f"{hijri.day}-{hijri.month}-{hijri.year}"
        # Highlight Ramadan (9th month) and Eid (1st & 10th months)
        color = "lightgray"  # Default off color
        if shift_type == "Morning":
            color = "#FFF176"
        elif shift_type == "Evening":
            color = "#FFB74D"
        elif shift_type == "Night":
            color = "#81D4FA"
        if hijri.month == 9:  # Ramadan
            color = "#FFD54F"
        if hijri.month == 1 or hijri.month == 10:  # Eid
            color = "#4DB6AC"
        schedule.append({
            "Date (Gregorian)": date.strftime("%d-%m-%Y"),
            "Date (Hijri)": hijri_str,
            "Shift": shift_type,
            "Color": color
        })

# --- Build yearly schedule ---
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

# --- Convert to DataFrame ---
df = pd.DataFrame(schedule)

# --- Display table ---
def color_rows(row):
    return [f"background-color: {row['Color']}"] * len(row)

df_display = df.copy()
df_display = df_display.drop(columns=["Color"])  # Hide color column
st.dataframe(df_display.style.apply(color_rows, axis=1), use_container_width=True)
