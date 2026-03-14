import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar
from hijri_converter import Gregorian

st.set_page_config(page_title="Hadeed Shift", layout="wide")

# ---------- LOGO ----------
st.markdown("""
<div style="text-align:center;padding:15px;border-radius:18px;background:white;
width:220px;margin:auto;box-shadow:0px 4px 12px rgba(0,0,0,0.15);">
<div style="font-size:48px;color:#1c3d8f;font-weight:bold;">حديد</div>
<div style="font-size:24px;color:#f39200;font-weight:bold;">hadeed</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- GROUP ----------
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

# ---------- SHIFT FUNCTION ----------
def get_shift_for_date(start_date, target_date):

    rotation_index=0
    rotation_day=0
    rotation_type,rotation_length=ROTATION[rotation_index]

    for i in range(2000):

        date=start_date+timedelta(days=i)

        if date.date()==target_date.date():
            return rotation_type

        rotation_day+=1

        if rotation_day>=rotation_length:
            rotation_index=(rotation_index+1)%len(ROTATION)
            rotation_type,rotation_length=ROTATION[rotation_index]
            rotation_day=0

# ---------- GENERATE CALENDAR ----------
def generate_schedule(start_date, days=365):

    events=[]

    rotation_index=0
    rotation_day=0
    rotation_type,rotation_length=ROTATION[rotation_index]

    for i in range(days):

        current_date=start_date+timedelta(days=i)

        hijri=Gregorian(
            current_date.year,
            current_date.month,
            current_date.day
        ).to_hijri()

        hijri_text=f"{hijri.day}/{hijri.month}"

        title=f"{rotation_type} | {hijri_text}"

        events.append({
            "title":title,
            "start":current_date.strftime("%Y-%m-%d"),
            "color":COLOR_MAP[rotation_type]
        })

        rotation_day+=1

        if rotation_day>=rotation_length:
            rotation_index=(rotation_index+1)%len(ROTATION)
            rotation_type,rotation_length=ROTATION[rotation_index]
            rotation_day=0

    return events

events=generate_schedule(GROUPS[group_selected])

# ---------- TODAY SHIFT ----------
today=datetime.today()
today_shift=get_shift_for_date(GROUPS[group_selected], today)

st.markdown(f"""
<div style="background:#0f5132;color:white;padding:10px;border-radius:10px;
font-size:18px;font-weight:bold;text-align:center;">
Today Shift: {today_shift}
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- DATE CHECK ----------
st.markdown("### Check Shift")

selected_date=st.date_input("Select Date")

shift_selected=get_shift_for_date(GROUPS[group_selected], datetime.combine(selected_date, datetime.min.time()))

st.success(f"Shift: {shift_selected}")

# ---------- CALENDAR ----------
calendar_options = {
"initialView":"dayGridMonth",
"height":700,
"headerToolbar":{
"left":"prev,next today",
"center":"title",
"right":""
}
}

calendar(events=events, options=calendar_options)
