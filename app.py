import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

st.set_page_config(page_title="Shift Calendar", layout="wide")

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
    "Night": "#87CEEB",
    "Evening": "#FFA500",
    "Morning": "#FFFF66",
    "OFF": "#DDDDDD"
}


def generate_schedule(start_date, days=365):

    schedule = []

    rotation_index = 0
    rotation_day_count = 0
    rotation_type, rotation_length = ROTATION[rotation_index]

    for i in range(days):

        current_date = start_date + timedelta(days=i)

        schedule.append({
            "Date": current_date,
            "Shift": rotation_type
        })

        rotation_day_count += 1

        if rotation_day_count >= rotation_length:

            rotation_index = (rotation_index + 1) % len(ROTATION)
            rotation_type, rotation_length = ROTATION[rotation_index]
            rotation_day_count = 0

    return pd.DataFrame(schedule)


st.title("📅 Shift Calendar")

group_selected = st.selectbox("Select Group", list(GROUPS.keys()))

df = generate_schedule(GROUPS[group_selected])

today = datetime.today()

today_row = df[df["Date"].dt.date == today.date()]

if not today_row.empty:
    today_shift = today_row.iloc[0]["Shift"]
    st.success(f"⭐ Today's Shift: {today_shift}")

col1, col2 = st.columns(2)

with col1:
    month = st.selectbox("Month", range(1, 13), index=today.month - 1)

with col2:
    year = st.selectbox("Year", [2026, 2027, 2028], index=0)

cal = calendar.monthcalendar(year, month)

html = """
<style>
table {
    width:100%;
    border-collapse: collapse;
}
th {
    background:#222;
    color:white;
    padding:10px;
}
td {
    height:80px;
    text-align:center;
    vertical-align:top;
    font-size:14px;
}
.today {
    border:3px solid red;
}
</style>
"""

html += "<table border=1>"
html += "<tr><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th><th>Sat</th><th>Sun</th></tr>"

for week in cal:

    html += "<tr>"

    for day in week:

        if day == 0:
            html += "<td></td>"

        else:

            date = datetime(year, month, day)

            row = df[df["Date"] == date]

            if not row.empty:

                shift = row.iloc[0]["Shift"]
                color = COLOR_MAP[shift]

                today_class = ""

                if date.date() == today.date():
                    today_class = "today"

                html += f"<td class='{today_class}' style='background:{color}'><b>{day}</b><br>{shift}</td>"

            else:
                html += f"<td>{day}</td>"

    html += "</tr>"

html += "</table>"

st.markdown(html, unsafe_allow_html=True)
