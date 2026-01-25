import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from hijri_converter import Gregorian

# --- CONFIGURATION ---
GROUPS = {
    "B": datetime(2026, 1, 18),  # B starts 18 Jan 2026 Night
    "C": datetime(2026, 1, 25),  # C starts 25 Jan 2026 Night
}

ROTATION = [
    ("Night", 7),  # 10PM - 6AM, 7 days
    ("OFF", 2),
    ("Evening", 7),  # 2PM - 10PM, 7 days
    ("OFF", 2),
    ("Morning", 7),  # 6AM - 2PM, 7 days
    ("OFF", 3),
]

HOLIDAYS_HIJRI = [
    (9, 1, "Ramadan"),     # بداية رمضان
    (10, 1, "Eid al-Fitr"), 
    (12, 10, "Eid al-Adha")
]

COLOR_MAP = {
    "Night": "#1f77b4",
    "Morning": "#2ca02c",
    "Evening": "#ff7f0e",
    "OFF": "#ffffff"
}

HOLIDAY_COLOR = {
    "Ramadan": "red",
    "Eid al-Fitr": "blue",
    "Eid al-Adha": "blue"
}

RAMADAN_MONTH = 9
RAMADAN_DAYS = range(1, 31)  # كامل أيام رمضان
EID_FTR_MONTH, EID_FTR_DAYS = 10, range(1,4)  # عيد الفطر 3 أيام
EID_ADHA_MONTH, EID_ADHA_DAYS = 12, range(10,13)  # عيد الأضحى 3 أيام

# --- HELPER FUNCTIONS ---
def generate_schedule(start_date, days=365):
    schedule = []
    rotation_index = 0
    rotation_day_count = 0
    rotation_type, rotation_length = ROTATION[rotation_index]

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        hijri_date = Gregorian(current_date.year, current_date.month, current_date.day).to_hijri()
        holiday_name = None
        # Check if today is holiday
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

def style_schedule(row):
    styles = []
    # Shift background
    color = COLOR_MAP.get(row["Shift"], "#ffffff")
    for col in row.index:
        styles.append(f"background-color: {color}")
    # Highlight holidays or Ramadan on Hijri date
    if row["Holiday"] == "Ramadan":
        styles[row.index.get_loc("Date (Hijri)")] = "color: red; font-weight: bold"
    elif row["Holiday"] in ["Eid al-Fitr", "Eid al-Adha"]:
        styles[row.index.get_loc("Date (Hijri)")] = "color: blue; font-weight: bold"
    return styles

# --- STREAMLIT APP ---
st.title("Yearly Shift Schedule")

group_selected = st.selectbox("Select Your Group:", list(GROUPS.keys()))

df = generate_schedule(GROUPS[group_selected])

st.dataframe(df.style.apply(style_schedule, axis=1))
