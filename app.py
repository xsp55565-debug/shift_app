import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_calendar import calendar

st.set_page_config(page_title="Hadeed Shift", layout="wide")

# ----- LOGO -----
st.markdown("""
<div style="text-align:center;
padding:30px;
border-radius:20px;
background:white;
width:500px;
margin:auto;
box-shadow:0px 6px 20px rgba(0,0,0,0.15);">

<div style="font-size:90px;color:#1c3d8f;font-weight:bold;">حديد</div>
<div style="font-size:70px;color:#f39200;font-weight:bold;">hadeed</div>

</div>
""", unsafe_allow_html=True)

st.write("")

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

COLOR_MAP = {
    "Night": "#77CBED",
    "Evening": "#FFA500",
    "Morning": "#FEF06B",
    "OFF": "#C7C2C2DB"
}

def generate_schedule(start_date, days=365):

    events = []

    rotation_index = 0
    rotation_day_count = 0
    rotation_type, rotation_length = ROTATION[rotation_index]

    for i in range(days):

        current_date = start_date + timedelta(days=i)

        events.append({
            "title": rotation_type,
            "start": current_date.strftime("%Y-%m-%d"),
            "color": COLOR_MAP[rotation_type]
        })

        rotation_day_count += 1

        if rotation_day_count >= rotation_length:
            rotation_index = (rotation_index + 1) % len(ROTATION)
            rotation_type, rotation_length = ROTATION[rotation_index]
            rotation_day_count = 0

    return events

group_selected = st.selectbox("Select Group", list(GROUPS.keys()))

events = generate_schedule(GROUPS[group_selected])

calendar(events=events)
