import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from hijri_converter import Gregorian

st.set_page_config(page_title="Hadeed Shift", layout="wide")

# ---------- LOGO ----------
st.markdown("""
<div style="text-align:center;padding:18px;border-radius:18px;background:white;
width:240px;margin:auto;box-shadow:0px 5px 15px rgba(0,0,0,0.15);">
<div style="font-size:50px;color:#1c3d8f;font-weight:bold;">حديد</div>
<div style="font-size:26px;color:#f39200;font-weight:bold;">hadeed</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- GROUPS ----------
GROUPS = {
    "B": datetime(2026,1,18),
    "C": datetime(2026,1,25),
}

group_selected = st.selectbox("Select Group", list(GROUPS.keys()))

# ---------- ROTATION ----------
ROTATION = [
    ("Night",7),
    ("OFF",2),
    ("Evening",7),
    ("OFF",2),
    ("Morning",7),
    ("OFF",3),
]

COLOR_MAP = {
    "Night":"#87CEEB",
    "Evening":"#FFA500",
    "Morning":"#FFF176",
    "OFF":"#E0E0E0"
}

SHIFT_SHORT = {
    "Morning":"M",
    "Evening":"E",
    "Night":"N",
    "OFF":"OFF"
}

# ---------- GENERATE SCHEDULE ----------
def generate_schedule(start_date, days=365):

    schedule=[]

    rotation_index=0
    rotation_day=0
    rotation_type,rotation_length=ROTATION[rotation_index]

    for i in range(days):

        date=start_date+timedelta(days=i)

        hijri=Gregorian(date.year,date.month,date.day).to_hijri()

        hijri_text=f"{hijri.day}/{hijri.month}"

        schedule.append({
            "date":date,
            "shift":rotation_type,
            "shift_short":SHIFT_SHORT[rotation_type],
            "color":COLOR_MAP[rotation_type],
            "hijri":hijri_text
        })

        rotation_day+=1

        if rotation_day>=rotation_length:
            rotation_index=(rotation_index+1)%len(ROTATION)
            rotation_type,rotation_length=ROTATION[rotation_index]
            rotation_day=0

    return schedule

schedule=generate_schedule(GROUPS[group_selected])

# ---------- TODAY SHIFT ----------
today=datetime.today().date()

today_shift=[d["shift"] for d in schedule if d["date"].date()==today]

if today_shift:
    st.markdown(f"""
<div style="background:#0f5132;color:white;padding:12px;border-radius:10px;
font-size:18px;font-weight:bold;text-align:center;">
Today Shift: {today_shift[0]}
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- CALENDAR GRID ----------
st.markdown("### Shift Calendar")

cols = st.columns(7)

for i,day in enumerate(schedule[:35]):

    col=cols[i%7]

    with col:

        st.markdown(f"""
        <div style="
        background:{day['color']};
        padding:12px;
        border-radius:10px;
        text-align:center;
        margin-bottom:10px;
        color:black;
        font-weight:bold;">
        
        {day['date'].day}<br>
        {day['shift_short']}<br>
        {day['hijri']}
        
        </div>
        """, unsafe_allow_html=True)
