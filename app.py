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


# ---------- GROUPS ----------
GROUPS = {
    "A": {
        "start_date": datetime(2026, 9, 1),
        "start_shift": "E",
        "reverse_cycle": True
    },

    "B": {
        "start_date": datetime(2026, 1, 18),
        "start_shift": "N",
        "reverse_cycle": False
    },

    "C": {
        "start_date": datetime(2026, 1, 25),
        "start_shift": "N",
        "reverse_cycle": False
    },

    "D": {
        "start_date": datetime(2026, 9, 3),
        "start_shift": "M",
        "reverse_cycle": True
    }
}


# ---------- SELECT GROUP ----------
group_selected = st.selectbox(
    "Select Group",
    list(GROUPS.keys())
)


# ---------- GET START INDEX ----------
def get_start_index(start_shift):

    if start_shift == "N":
        return 0

    if start_shift == "E":
        return 2

    if start_shift == "M":
        return 4


# ---------- SHIFT FUNCTION ----------
def get_shift_for_date(group_name, target_date):

    group = GROUPS[group_name]

    start_date = group["start_date"].date()

    if isinstance(target_date, datetime):
        target_date = target_date.date()

    # =========================================================
    # A و D
    # نحسب الدورة للخلف والأمام من تاريخ البداية
    # =========================================================
    if group["reverse_cycle"]:

        start_index = get_start_index(group["start_shift"])

        # مجموع الدورة = 28 يوم
        cycle_length = sum(
            length for shift, length in ROTATION
        )

        days_difference = (
            target_date - start_date
        ).days

        # اليوم داخل الدورة
        cycle_day = days_difference % cycle_length

        rotation_index = start_index

        while True:

            shift_type, shift_length = ROTATION[
                rotation_index
            ]

            if cycle_day < shift_length:
                return shift_type

            cycle_day -= shift_length

            rotation_index = (
                rotation_index + 1
            ) % len(ROTATION)

    # =========================================================
    # B و C
    # نفس نظام الكود الأصلي
    # =========================================================

    if target_date < start_date:
        return None

    rotation_index = 0
    rotation_day = 0

    rotation_type, rotation_length = ROTATION[
        rotation_index
    ]

    days_difference = (
        target_date - start_date
    ).days

    for _ in range(days_difference):

        rotation_day += 1

        if rotation_day >= rotation_length:

            rotation_index = (
                rotation_index + 1
            ) % len(ROTATION)

            rotation_type, rotation_length = ROTATION[
                rotation_index
            ]

            rotation_day = 0

    return rotation_type


# ---------- GENERATE CALENDAR ----------
def generate_schedule(group_name, days=730):

    events = []

    # نبدأ من بداية 2026
    # عشان A و D يظهر لهم الماضي
    calendar_start = datetime(2026, 1, 1)

    for i in range(days):

        current_date = calendar_start + timedelta(days=i)

        shift = get_shift_for_date(
            group_name,
            current_date
        )

        # B و C قبل بداية الجدول
        if shift is None:
            continue

        # ---------- HIJRI ----------
        hijri = Gregorian(
            current_date.year,
            current_date.month,
            current_date.day
        ).to_hijri()

        hijri_text = f"{hijri.day}/{hijri.month}"

        title = f"{shift}{hijri_text}"
        color = COLOR_MAP[shift]

        # ---------- RAMADAN ----------
        if hijri.month == 9:

            title = f"{shift}{hijri_text}"
            color = "#9c27b0"

        # ---------- EID AL-FITR ----------
        if hijri.month == 10 and hijri.day <= 3:

            title = f"{shift}{hijri_text}"
            color = "#4caf50"

        # ---------- EID AL-ADHA ----------
        if hijri.month == 12 and 10 <= hijri.day <= 13:

            title = f"{shift}{hijri_text}"
            color = "#2196f3"

        events.append({
            "title": title,
            "start": current_date.strftime("%Y-%m-%d"),
            "color": color
        })

    return events


# ---------- CURRENT GROUP ----------
events = generate_schedule(
    group_selected
)


# ---------- TODAY SHIFT ----------
today = datetime.today()

today_shift = get_shift_for_date(
    group_selected,
    today
)

if today_shift is None:
    today_shift = "N/A"

st.markdown(f"""
<div style="background:#0f5132;color:white;padding:12px;border-radius:10px;
font-size:18px;font-weight:bold;text-align:center;">
Today Shift: {today_shift}
</div>
""", unsafe_allow_html=True)

st.write("")


# =========================================================
# CHECK SHIFT
# =========================================================
st.markdown("### Check Shift")

# ---------- ENGLISH DATE SELECTOR ----------
MONTHS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

# تاريخ اليوم
today_date = datetime.today().date()

col1, col2, col3 = st.columns(3)

with col1:

    selected_year = st.selectbox(
        "Year",
        list(range(2025, 2031)),
        index=list(range(2025, 2031)).index(
            today_date.year
        )
    )

with col2:

    selected_month = st.selectbox(
        "Month",
        list(MONTHS.keys()),
        format_func=lambda x: MONTHS[x],
        index=today_date.month - 1
    )

with col3:

    # عدد أيام الشهر
    if selected_month == 12:
        next_month = datetime(
            selected_year + 1,
            1,
            1
        )
    else:
        next_month = datetime(
            selected_year,
            selected_month + 1,
            1
        )

    days_in_month = (
        next_month -
        datetime(
            selected_year,
            selected_month,
            1
        )
    ).days

    selected_day = st.selectbox(
        "Day",
        list(range(1, days_in_month + 1)),
        index=min(
            today_date.day - 1,
            days_in_month - 1
        )
    )


selected_date = datetime(
    selected_year,
    selected_month,
    selected_day
).date()


# ---------- SHOW SELECTED DATE ----------
st.caption(
    f"Selected Date: "
    f"{MONTHS[selected_month]} "
    f"{selected_day}, "
    f"{selected_year}"
)


# ---------- CHECK SHIFT ----------
shift_selected = get_shift_for_date(
    group_selected,
    selected_date
)

if shift_selected is None:

    st.success("Shift: N/A")

else:

    st.success(
        f"Shift: {shift_selected}"
    )


# =========================================================
# CALENDAR
# =========================================================
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