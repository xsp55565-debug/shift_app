import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from hijri_converter import convert

st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --- Choose group and start date ---
groups = ["A", "B", "C", "D"]
default_group_index = groups.index("B")  # Default to B
group = st.selectbox("Select Group:", groups, index=default_group_index)

start_date = st.date_input("Select Start Date:", datetime(2026, 1, 25))
st.write("Selected Group:", group)
st.write("Start Date:", start_date.strftime("%d-%m-%Y"))

# --- Create yearly schedule ---
schedule = []

# Shift cycle
def add_shifts(start, shift_type, days):
    color_map = {
        "Morning": "yellow",
        "Evening": "orange",
        "Night": "lightblue",
        "Off": "lightgray"
    }
    for i in range(days):
        date = start + timedelta(days=i)
        hijri_date = convert.Gregorian(date.year, date.month, date.day).to_hijri()
        hijri_str = f"{hijri_date.day}-{hijri_date.month}-{hijri_date.year}H"
        gregorian_str = date.strftime("%a, %d-%m-%Y")

        # Special coloring for Ramadan or Eid
        special_color = None
        if hijri_date.month == 9:  # Ramadan
            special_color = "lightgreen"
        elif (hijri_date.month == 10 and hijri_date.day in [1,2,3]):  # Eid al-Adha
            special_color = "lightpink"

        schedule.append({
            "Gregorian": gregorian_str,
            "Hijri": hijri_str,
            "Shift": shift_type,
            "Color": special_color if special_color else color_map[shift_type]
        })

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

# --- Coloring rows ---
def color_rows(row):
    return [f"background-color: {row['Color']}"] * len(row)

# --- Display DataFrame without showing color names ---
df_display = df.drop(columns=["Color"])
st.dataframe(
    df_display.style.apply(color_rows, axis=1),
    use_container_width=True
)
