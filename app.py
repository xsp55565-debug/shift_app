import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from hijri_converter import convert

# --- Streamlit page config ---
st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --- Groups and default start dates ---
groups = ["A", "B", "C", "D"]
default_group_index = groups.index("B")  # Default group is B
group = st.selectbox("Select Group:", groups, index=default_group_index)

# Default start dates for each group (adjust as needed)
start_dates = {
    "A": datetime(2026, 1, 18),
    "B": datetime(2026, 1, 18),
    "C": datetime(2026, 1, 25),
    "D": datetime(2026, 2, 1)
}

start_date = st.date_input("Select Start Date:", start_dates[group])
st.write("Selected Group:", group)
st.write("Start Date:", start_date.strftime("%d-%m-%Y"))

# --- Select a specific date to check shift ---
check_date = st.date_input("Check Shift on Date:", datetime.today())
hijri_date = convert.Gregorian(check_date.year, check_date.month, check_date.day).to_hijri()
st.write(f"Selected Date Hijri: {hijri_date.day}-{hijri_date.month}-{hijri_date.year}")

# --- Create the schedule ---
schedule = []

def add_shifts(start, shift_type, days):
    for i in range(days):
        date = start + timedelta(days=i)
        schedule.append({
            "Date": date,
            "Shift": shift_type,
            "Color": {
                "Morning": "yellow",
                "Evening": "orange",
                "Night": "lightblue",
                "Off": "lightgray"
            }[shift_type]
        })

current_date = start_date
while current_date < start_date + timedelta(days=365):
    # Night shift: 7 days
    add_shifts(current_date, "Night", 7)
    current_date += timedelta(days=7)
    # Off: 2 days
    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)
    # Evening shift: 7 days
    add_shifts(current_date, "Evening", 7)
    current_date += timedelta(days=7)
    # Off: 2 days
    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)
    # Morning shift: 7 days
    add_shifts(current_date, "Morning", 7)
    current_date += timedelta(days=7)
    # Off: 3 days
    add_shifts(current_date, "Off", 3)
    current_date += timedelta(days=3)

# --- Convert to DataFrame ---
df = pd.DataFrame(schedule)
df["Date"] = pd.to_datetime(df["Date"])
df_display = df.copy()
df_display["Date"] = df_display["Date"].dt.strftime("%a, %d-%m-%Y")

# --- Highlight colors ---
def color_rows(row):
    return [f"background-color: {row['Color']}"] * len(row)

# --- Show full schedule ---
st.subheader("Full Schedule")
st.dataframe(df_display.style.apply(color_rows, axis=1), use_container_width=True)

# --- Show shift for selected date ---
shift_on_date = df[df["Date"] == pd.to_datetime(check_date)]
if not shift_on_date.empty:
    st.subheader("Shift on Selected Date")
    st.write(shift_on_date[["Date", "Shift"]].reset_index(drop=True))
else:
    st.write("No shift found for this date.")
