import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar
from hijri_converter import Gregorian

st.set_page_config(page_title="Hadeed Shift", layout="wide")

# ---------- LOGO ----------
st.markdown("""
<div style="text-align:center;padding:20px;border-radius:20px;background:white;
width:240px;margin:auto;box-shadow:0px 6px 20px rgba(0,0,0,0.15);">
<div style="font-size:50px;color:#1c3d8f;font-weight:bold;">حديد</div>
<div style="font-size:28px;color:#f39200;font-weight:bold;">hadeed</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- COLOR LEGEND ----------
st.markdown("""
<div style="margin:auto;margin-top:10px;padding:12px;border-radius:12px;
background:white;width:520px;box-shadow:0px 3px 12px rgba(0,0,0,0.1);
font-size:14px;text-align:center;">

<b>توضيح الألوان</b><br><br>

<span style="background:#FFF176;padding:6px 10px;border-radius:8px;">Morning</span>
<span style="background:#FFA500;padding:6px 10px;border-radius:8px;">Evening</span>
<span style="background:#87CEEB;padding:6px 10px;border-radius:8px;">Night</span>
<span style="background:#E0E0E0;padding:6px 10px;border-radius:8px;">OFF</span>

<br><br>

<span style="background:#9c27b0;color:white;padding:6px 10px;border-radius:8px;">🌙 Ramadan</span>
<span style="background:#4caf50;color:white;padding:6px 10px;border-radius:8px;">🎉 Eid Al-Fitr</span>
<span style="background:#2196f3;color:white;padding:6px 10px;border-radius:8px;">🐑 Eid Al-Adha</span>

</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- GROUPS ----------
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

# ---------- FUNCTION ----------
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

        if hijri.month==9:
            title=f"{SHIFT_SHORT[rotation_type]}\n🌙 {hijri_text}"
            color="#9c27b0"

        if hijri.month==10 and hijri.day<=3:
            title=f"🎉 {SHIFT_SHORT[rotation_type]}\n{hijri_text}"
            color="#4caf50"

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

# ---------- TODAY ----------
today=datetime.today()
today_shift=get_shift_for_date(GROUPS[group_selected], today)

st.markdown(f"""
<div style="background:#0f5132;color:white;padding:14px;border-radius:10px;
font-size:20px;font-weight:bold;text-align:center;">
⭐ دوام اليوم: {today_shift}
</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- DATE PICKER ----------
st.markdown("### اعرف دوامك لأي تاريخ")

selected_date=st.date_input("اختر التاريخ")

shift_selected=get_shift_for_date(GROUPS[group_selected], selected_date)

st.success(f"دوامك في هذا اليوم: {shift_selected}")

# ---------- CALENDAR ----------
calendar_options = {
"initialView":"dayGridMonth",
"height":650,
}

calendar(events=events, options=calendar_options)
