import streamlit as st
from datetime import datetime, timedelta
from streamlit_calendar import calendar
from hijri_converter import Gregorian

st.markdown("""
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#1c3d8f">
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Hadeed Shift",
    page_icon="📅",
    layout="wide"
)

# ---------- LOGO ----------
st.markdown("""
<div style="text-align:center;padding:15px;border-radius:18px;background:white;
width:220px;margin:auto;box-shadow:0px 4px 12px rgba(0,0,0,0.15);">
<div style="font-size:48px;color:#1c3d8f;font-weight:bold;">حديد</div>
<div style="font-size:24px;color:#f39200;font-weight:bold;">hadeed</div>
</div>
""", unsafe_allow_html=True)

# ---------- LEGEND ----------
st.markdown("""
<div style="text-align:center;padding:10px;border-radius:12px;background:white;
width:220px;margin:auto;margin-top:10px;
box-shadow:0px 3px 10px rgba(0,0,0,0.1);font-size:12px;">

<b>Legend</b><br><br>

<span style="background:#FFF176;padding:4px 8px;border-radius:6px;">Morning</span><br><br>
<span style="background:#FFA500;padding:4px 8px;border-radius:6px;">Evening</span><br><br>
<span style="background:#87CEEB;padding:4px 8px;border-radius:6px;">Night</span><br><br>
<span style="background:#E0E0E0;padding:4px 8px;border-radius:6px;">OFF</span><br><br>

<span style="background:#9c27b0;color:white;padding:4px 8px;border-radius:6px;">Ramadan</span><br><br>
<span style="background:#4caf50;color:white;padding:4px 8px;border-radius:6px;">Eid Al-Fitr</span><br><br>
<span style="background:#2196f3;color:white;padding:4px 8px;border-radius:6px;">Eid Al-Adha</span>

</div>
""", unsafe_allow_html=True)

st.write("")

# ---------- GROUPS ----------
GROUPS = {
    "A": {
        "start_date": datetime(2026, 9, 1),
        "start_shift": "E"
    },

    "B": {
        "start_date": datetime(2026, 1, 18),
        "start_shift": "N"
    },

    "C": {
        "start_date": datetime(2026, 1, 25),
        "start_shift": "N"
    },

    "D": {
        "start_date": datetime(2026, 9, 3),
        "start_shift": "M"
    }
}

group_selected = st.selectbox(
    "Select Group",
    list(GROUPS.keys())
)

# ---------- ROTATION ----------
ROTATION = [
    ("N", 7),
    ("OFF", 2),
    ("E", 7),
    ("OFF", 2),
    ("M", 7),
    ("OFF", 3),
]

COLOR_MAP = {
    "N": "#79CCED",
    "E": "#FFA500",
    "M": "#FDEB4E",
    "OFF": "#A1A0A0"
}

# ---------- GET START ROTATION ----------
def get_start_index(start_shift):
    if start_shift == "N":
        return 0
    elif start_shift == "E":
        return 2
    elif start_shift == "M":
        return 4


# ---------- SHIFT FUNCTION ----------
def get_shift_for_date(start_date, start_shift, target_date):

    if isinstance(target_date, datetime):
        target_date = target_date.date()

    start_date = start_date.date()

    rotation_index = get_start_index(start_shift)
    rotation_day = 0

    rotation_type, rotation_length = ROTATION[rotation_index]

    # التاريخ يساوي أو بعد تاريخ البداية
    if target_date >= start_date:

        days_difference = (target_date - start_date).days

        for _ in range(days_difference):

            rotation_day += 1

            if rotation_day >= rotation_length:
                rotation_index = (rotation_index + 1) % len(ROTATION)
                rotation_type, rotation_length = ROTATION[rotation_index]
                rotation_day = 0

        return rotation_type

    # التاريخ قبل تاريخ البداية
    else:

        days_difference = (start_date - target_date).days

        for _ in range(days_difference):

            rotation_day -= 1

            if rotation_day < 0:
                rotation_index = (rotation_index - 1) % len(ROTATION)
                rotation_type, rotation_length = ROTATION[rotation_index]
                rotation_day = rotation_length - 1

        return rotation_type


# ---------- GENERATE CALENDAR ----------
def generate_schedule(start_date, start_shift, days=365):

    events = []

    rotation_index = get_start_index(start_shift)
    rotation_day = 0

    rotation_type, rotation_length = ROTATION[rotation_index]

    for i in range(days):

        current_date = start_date + timedelta(days=i)

        hijri = Gregorian(
            current_date.year,
            current_date.month,
            current_date.day
        ).to_hijri()

        hijri_text = f"{hijri.day}/{hijri.month}"

        title = f"{rotation_type}{hijri_text}"
        color = COLOR_MAP[rotation_type]

        # Ramadan
        if hijri.month == 9:
            title = f"{rotation_type}{hijri_text}"
            color = "#9c27b0"

        # Eid Fitr
        if hijri.month == 10 and hijri.day <= 3:
            title = f"{rotation_type}{hijri_text}"
            color = "#4caf50"

        # Eid Adha
        if hijri.month == 12 and 10 <= hijri.day <= 13:
            title = f"{rotation_type}{hijri_text}"
            color = "#2196f3"

        events.append({
            "title": title,
            "start": current_date.strftime("%Y-%m-%d"),
            "color": color
        })

        rotation_day += 1

        if rotation_day >= rotation_length:
            rotation_index = (rotation_index + 1) % len(ROTATION)
            rotation_type, rotation_length = ROTATION[rotation_index]
            rotation_day = 0

    return events


# ---------- CURRENT GROUP ----------
group_data = GROUPS[group_selected]

events = generate_schedule(
    group_data["start_date"],
    group_data["start_shift"]
)


# ---------- TODAY SHIFT ----------
today = datetime.today()

today_shift = get_shift_for_date(
    group_data["start_date"],
    group_data["start_shift"],
    today
)

st.markdown(f"""
<div style="background:#0f5132;color:white;padding:12px;border-radius:10px;
font-size:18px;font-weight:bold;text-align:center;">
Today Shift: {today_shift}
</div>
""", unsafe_allow_html=True)

st.write("")


# ---------- CHECK DATE ----------
st.markdown("### Check Shift")

selected_date = st.date_input("Select Date")

shift_selected = get_shift_for_date(
    group_data["start_date"],
    group_data["start_shift"],
    selected_date
)

st.success(f"Shift: {shift_selected}")


# ---------- CALENDAR ----------
calendar_options = {
    "initialView": "dayGridMonth",
    "height": 750,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": ""
    }
}

calendar(
    events=events,
    options=calendar_options
)