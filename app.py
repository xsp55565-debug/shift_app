import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar
from hijri_converter import Gregorian

st.set_page_config(page_title="Hadeed Shift", layout="wide")

# ---------- LOGO ----------
st.markdown("""
<div style="text-align:center;padding:20px;border-radius:20px;background:white;
width:320px;margin:auto;box-shadow:0px 6px 20px rgba(0,0,0,0.15);">
<div style="font-size:60px;color:#1c3d8f;font-weight:bold;">حديد</div>
<div style="font-size:36px;color:#f39200;font-weight:bold;">hadeed</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- GROUP SELECT ----------
GROUPS = {
    "B": datetime(2026,1,18),
    "C": datetime(2026,1,25),
}

st.markdown("### اختر مجموعتك")
group_selected = st.selectbox("", list(GROUPS.keys()))

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

# ---------- GENERATE EVENTS ----------
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

        title=f"{SHIFT_SHORT[rotation_type]}\n{hijri_text}"

        color=COLOR_MAP[rotation_type]

        # رمضان
        if hijri.month==9:
            title=f"{SHIFT_SHORT[rotation_type]} 🌙\n{hijri_text}"
            color="#9c27b0"

        # عيد الفطر
        if hijri.month==10 and hijri.day<=3:
            title=f"🎉 {SHIFT_SHORT[rotation_type]}\n{hijri_text}"
            color="#4caf50"

        # عيد الأضحى
        if hijri.month==12 and 10<=hijri.day<=13:
            title=f"🐑 {SHIFT_SHORT[rotation_type]}\n{hijri_text}"
            color="#2196f3"

        events.append({
            "title":title,
            "start":current_date.strftime("%Y-%m-%d"),
            "color":color
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

rotation_index=0
rotation_day=0
rotation_type,rotation_length=ROTATION[rotation_index]

today_shift=""

for i in range(365):

    date=GROUPS[group_selected]+timedelta(days=i)

    if date.date()==today.date():
        today_shift=rotation_type
        break

    rotation_day+=1

    if rotation_day>=rotation_length:
        rotation_index=(rotation_index+1)%len(ROTATION)
        rotation_type,rotation_length=ROTATION[rotation_index]
        rotation_day=0

st.markdown(f"""
<div style="background:#0f5132;color:white;padding:15px;border-radius:12px;
font-size:22px;font-weight:bold;text-align:center;">
⭐ دوام اليوم: {today_shift}
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- CALENDAR ----------
calendar_options = {
"initialView":"dayGridMonth",
"height":650,
}

calendar(events=events, options=calendar_options)
