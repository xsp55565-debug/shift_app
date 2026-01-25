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
    (9, 1),  # Ramadan start
    (10, 1), # Eid al-Fitr
    (12, 10) # Eid al-Adha
]

COLOR_MAP = {
    "Night": "#1f77b4",
    "Morning": "#2ca02c",
    "Evening": "#ff7f0e",
    "OFF": "#ffffff"
}

# --- HELPER FUNCTIONS ---
def generate_schedule(start_date, days=365):
    schedule = []
    rotation_index = 0
    rotation_day_count = 0
    rotation_type, rotation_length = ROTATION[rotation_index]

    for i in range(days):
        current_date = start_date + timedelta(days=i)
        # Hijri date
        hijri_date = Gregorian(current_date.year, current_date.month, current_date.day).to_hijri()
        is_holiday = (hijri_date.month, hijri_date.day) in HOLIDAYS_HIJRI
        schedule.append({
            "Date (Gregorian)": current_date.strftime("%Y-%m-%d"),
            "Date (Hijri)": f"{hijri_date.day}-{hijri_date.month}-{hijri_date.year}" + (" 🎉" if is_holiday else ""),
            "Shift": rotation_type
        })
        rotation_day_count += 1
        if rotation_day_count >= rotation_length:
            rotation_index = (rotation_index + 1) % len(ROTATION)
            rotation_type, rotation_length = ROTATION[rotation_index]
            rotation_day_count = 0
    return pd.DataFrame(schedule)

def color_shifts(row):
    color = COLOR_MAP.get(row["Shift"], "#ffffff")
    return [f"background-color: {color}"]*len(row)

# --- STREAMLIT APP ---
st.title("Yearly Shift Schedule")

group_selected = st.selectbox("Select Your Group:", list(GROUPS.keys()))

df = generate_schedule(GROUPS[group_selected])

st.dataframe(df.style.apply(color_shifts, axis=1))
