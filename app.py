import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from hijri_converter import convert

st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --- Select Group and Start Date ---
groups = ["A", "B", "C", "D"]
default_group_index = groups.index("B")  # default to B
group = st.selectbox("Select Group:", groups, index=default_group_index)

start_date = st.date_input("Select Start Date:", datetime(2026, 1, 25))
st.write("Selected Group:", group)
st.write("Start Date (Gregorian):", start_date.strftime("%d-%m-%Y"))

# --- Generate Yearly Schedule ---
schedule = []

def add_shifts(start, shift_type, days):
    for i in range(days):
        date = start + timedelta(days=i)
        # Convert to Hijri
        hijri_date = convert.Gregorian(date.year, date.month, date.day).to_hijri()
        hijri_str = f"{hijri_date.day}-{hijri_date.month}-{hijri_date.year}"
        # Mark holidays (example: Ramadan and Eid)
        holiday = ""
        if hijri_date.month == 9:  # Ramadan
            holiday = "Ramadan"
        elif hijri_date.month == 10 and hijri_date.day in [1, 2]:  # Eid al-Adha
            holiday = "Eid"
        schedule.append({
            "Date (Gregorian)": date,
            "Date (Hijri)": hijri_str,
            "Shift": shift_type,
            "Holiday": holiday,
            "Color": {
                "Morning": "yellow",
                "Evening": "orange",
                "Night": "lightblue",
                "Off": "lightgray"
            }[shift_type]
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

# --- Convert to DataFrame ---
df = pd.DataFrame(schedule)
df["Date (Gregorian)"] = pd.to_datetime(df["Date (Gregorian)"])
df_display = df.copy()
df_display["Date (Gregorian)"] = df_display["Date (Gregorian)"].dt.strftime("%a, %d-%m-%Y")

# --- Style rows based on Color (without showing Color column) ---
def color_rows(row):
    return [f"background-color: {row['Color']}"] * len(row)

df_display_styled = df_display.drop(columns=["Color"])  # hide Color column

# --- Display Table ---
st.dataframe(
    df_display_styled.style.apply(color_rows, axis=1),
    use_container_width=True
)
