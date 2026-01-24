import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from hijri_converter import Gregorian

# --- Streamlit page setup ---
st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --- Groups selection ---
groups = ["A", "B", "C", "D"]
group = st.selectbox("Select Group:", groups, index=1)  # default B

# --- Start dates for each group ---
group_start_dates = {
    "A": datetime(2026, 1, 25),
    "B": datetime(2026, 1, 18),
    "C": datetime(2026, 1, 25),
    "D": datetime(2026, 1, 18)
}
start_date = group_start_dates[group]
st.write("Selected Group:", group)
st.write("Shift cycle start date:", start_date.strftime("%d-%m-%Y"))

# --- Optional: check shift for a specific date ---
check_date = st.date_input("Check shift for a specific date:", datetime.today())

# --- Create yearly shift schedule ---
schedule = []

def add_shifts(start, shift_type, days):
    for i in range(days):
        date = start + timedelta(days=i)
        hijri = Gregorian(date.year, date.month, date.day).to_hijri()
        hijri_str = f"{hijri.day}-{hijri.month}-{hijri.year}"
        
        # Mark Ramadan (9th month) and Eid (1st and 10th month)
        holiday_flag = ""
        if hijri.month == 9:
            holiday_flag = " (Ramadan)"
        elif hijri.month in [1, 10]:
            holiday_flag = " (Eid)"

        schedule.append({
            "Date (Gregorian)": date.strftime("%d-%m-%Y"),
            "Date (Hijri)": hijri_str + holiday_flag,
            "Shift": shift_type
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

df = pd.DataFrame(schedule)

# --- Show full schedule for the selected group ---
st.subheader(f"Full yearly schedule for group {group}")
st.dataframe(df, use_container_width=True)

# --- Show shift for specific date ---
specific_shift = df[df["Date (Gregorian)"] == check_date.strftime("%d-%m-%Y")]
if not specific_shift.empty:
    st.subheader(f"Shift on {check_date.strftime('%d-%m-%Y')}")
    st.write(specific_shift.iloc[0])
else:
    st.write("No shift found for this date.")
