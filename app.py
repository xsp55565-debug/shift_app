import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Page setup
st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --- Group selection ---
groups = ["A", "B", "C", "D"]
default_group_index = groups.index("B")  # default group B
group = st.selectbox("Select Group:", groups, index=default_group_index)

# --- Start date selection ---
start_date = st.date_input("Select Start Date:", datetime(2026, 1, 18))
st.write("Selected Group:", group)
st.write("Start Date:", start_date.strftime("%d-%m-%Y"))

# --- Build annual schedule ---
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
    add_shifts(current_date, "Night", 7)   # 10 PM - 6 AM
    current_date += timedelta(days=7)
    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)
    add_shifts(current_date, "Evening", 7) # 2 PM - 10 PM
    current_date += timedelta(days=7)
    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)
    add_shifts(current_date, "Morning", 7) # 6 AM - 2 PM
    current_date += timedelta(days=7)
    add_shifts(current_date, "Off", 3)
    current_date += timedelta(days=3)

# Convert to DataFrame
df = pd.DataFrame(schedule)
df["Date"] = pd.to_datetime(df["Date"])
df_display = df.copy()
df_display["Date"] = df_display["Date"].dt.strftime("%a, %d-%m-%Y")

# --- Function to color rows ---
def color_rows(row):
    return [f"background-color: {row['Color']}"] * len(row)

# --- Select a date to see shift ---
selected_date = st.date_input("Check your shift for a specific date:", datetime.now())
shift_info = df[df["Date"] == pd.to_datetime(selected_date)]
if not shift_info.empty:
    st.write(f"Shift on {selected_date.strftime('%d-%m-%Y')}: {shift_info.iloc[0]['Shift']}")
else:
    st.write(f"No shift found for {selected_date.strftime('%d-%m-%Y')}")

# --- Show full schedule ---
st.subheader("Full Schedule")
st.dataframe(df_display.style.apply(color_rows, axis=1), use_container_width=True)
