import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_calendar import calendar
from hijri_converter import Gregorian

st.set_page_config(page_title="Hadeed Shift", layout="wide")

# ----- LOGO -----
st.markdown("""
<div style="text-align:center;
padding:25px;
border-radius:18px;
background:white;
width:420px;
margin:auto;
box-shadow:0px 6px 20px rgba(0,0,0,0.15);">

<div style="font-size:70px;color:#1c3d8f;font-weight:bold;">حديد</div>
<div style="font-size:50px;color:#f39200;font-weight:bold;">hadeed</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# ----- GROUPS -----
GROUPS = {
    "B": datetime(2026, 1, 18),
    "C": datetime(2026, 1, 25),
}

ROTATION = [
    ("N", 7),
    ("OFF", 2),
    ("E", 7),
    ("OFF", 2),
    ("M", 7),
    ("OFF", 3),
]

COLOR_MAP = {
    "N": "#75D0F4",
    "E": "#FFA500",
    "M": "#F8E859",
    "OFF": "#B9B7B7"
}

def generate_schedule(start_date, days=365):

    events = []

    rotation_index = 0
    rotation_day_count = 0
    rotation_type, rotation_length = ROTATION[rotation_index]

    for i in range(days):

        current_date = start_date + timedelta(days=i)

        hijri = Gregorian(
            current_date.year,
            current_date.month,
            current_date.day
        ).to_hijri()

        hijri_text = f"{hijri.day}/{hijri.month}"

        title = f"{rotation_type} | {hijri_text}"

        color = COLOR_MAP[rotation_type]

        # رمضان
        if hijri.month == 9:
            title += " 🌙"
            color = "#9c27b0"

        # عيد الفطر
        if hijri.month == 10 and hijri.day <= 3:
            title += " 🎉"
            color = "#4caf50"

        # عيد الأضحى
        if hijri.month == 12 and 10 <= hijri.day <= 13:
            title += " 🐑"
            color = "#2196f3"

        events.append({
            "title": title,
            "start": current_date.strftime("%Y-%m-%d"),
            "color": color
        })

        rotation_day_count += 1

        if rotation_day_count >= rotation_length:

            rotation_index = (rotation_index + 1) % len(ROTATION)
            rotation_type, rotation_length = ROTATION[rotation_index]
            rotation_day_count = 0

    return events

group_selected = st.selectbox("Select Group", list(GROUPS.keys()))

events = generate_schedule(GROUPS[group_selected])

# ----- TODAY SHIFT -----
today = datetime.today()

rotation_index = 0
rotation_day_count = 0
rotation_type, rotation_length = ROTATION[rotation_index]

for i in range(365):

    date = GROUPS[group_selected] + timedelta(days=i)

    if date.date() == today.date():
        today_shift = rotation_type
        break

    rotation_day_count += 1

    if rotation_day_count >= rotation_length:
        rotation_index = (rotation_index + 1) % len(ROTATION)
        rotation_type, rotation_length = ROTATION[rotation_index]
        rotation_day_count = 0

st.markdown(f"""
<div style="
background-color:#1c7c2c;
color:white;
padding:14px;
border-radius:10px;
font-size:20px;
font-weight:bold;
text-align:center;
">
⭐ Today's Shift: {today_shift}
</div>
""", unsafe_allow_html=True)

st.write("")

# ----- CALENDAR -----
calendar(events=events)
