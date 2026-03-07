import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from hijri_converter import convert

# --- CONFIGURATION ---
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

RAMADAN_MONTH = 9
RAMADAN_DAYS = range(1, 31)

EID_FTR_MONTH, EID_FTR_DAYS = 10, range(1, 6)
EID_ADHA_MONTH, EID_ADHA_DAYS = 12, range(10, 15)

COLOR_MAP = {
    "Night": "#1f77b4",
    "Morning": "#cbc969",
    "Evening": "#ff7f0e",
    "OFF": "#E3D7D7"
}

# --- FUNCTIONS ---
def generate_schedule(start_date, days=365):

    schedule = []

    rotation_index = 0
    rotation_day_count = 0
    rotation_type, rotation_length = ROTATION[rotation_index]

    for i in range(days):

        current_date = start_date + timedelta(days=i)

        hijri_date = convert.Gregorian(
            current_date.year,
            current_date.month,
            current_date.day
        ).to_hijri()

        holiday_name = None

        if hijri_date.month == RAMADAN_MONTH and hijri_date.day in RAMADAN_DAYS:
            holiday_name = "Ramadan"

        elif hijri_date.month == EID_FTR_MONTH and hijri_date.day in EID_FTR_DAYS:
            holiday_name = "Eid al-Fitr"

        elif hijri_date.month == EID_ADHA_MONTH and hijri_date.day in EID_ADHA_DAYS:
            holiday_name = "Eid al-Adha"

        hijri_str = f"{hijri_date.day}-{hijri_date.month}-{hijri_date.year}"

        schedule.append({
            "Date (Gregorian)": current_date.strftime("%Y-%m-%d"),
            "Date (Hijri)": hijri_str,
            "Shift": rotation_type,
            "Holiday": holiday_name
        })

        rotation_day_count += 1

        if rotation_day_count >= rotation_length:

            rotation_index = (rotation_index + 1) % len(ROTATION)
            rotation_type, rotation_length = ROTATION[rotation_index]
            rotation_day_count = 0

    return pd.DataFrame(schedule)

# --- APP ---
st.title("Yearly Shift Schedule")

group_selected = st.selectbox("Select Your Group:", list(GROUPS.keys()))

df = generate_schedule(GROUPS[group_selected])

# اختيار التاريخ
selected_date = st.date_input("Choose a date to see your shift")

selected = df[df["Date (Gregorian)"] == selected_date.strftime("%Y-%m-%d")]

if not selected.empty:

    shift = selected.iloc[0]["Shift"]
    hijri = selected.iloc[0]["Date (Hijri)"]
    holiday = selected.iloc[0]["Holiday"]

    st.success(f"Shift: {shift}")
    st.write(f"Hijri Date: {hijri}")

    if holiday:
        st.warning(f"Holiday: {holiday}")

st.dataframe(df)