import streamlit as st
import pandas as pd
from datetime import date, timedelta
from hijri_converter import convert

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Shift Schedule", layout="wide")
st.title("Shift Schedule")

# ---------------- GROUP SETTINGS ----------------
GROUP_START = {
    "A": date(2026, 1, 23),
    "B": date(2026, 1, 18),
    "C": date(2026, 1, 25),  # Today night
    "D": date(2026, 1, 30),
}

SHIFT_CYCLE = (
    ["Night"] * 7 +
    ["Off"] * 2 +
    ["Evening"] * 7 +
    ["Off"] * 2 +
    ["Morning"] * 7 +
    ["Off"] * 3
)

SHIFT_COLORS = {
    "Morning": "#FFF59D",
    "Evening": "#FFCC80",
    "Night": "#90CAF9",
    "Off": "#E0E0E0",
}

RAMADAN_COLOR = "#CE93D8"
EID_COLOR = "#A5D6A7"

# ---------------- USER INPUT ----------------
group = st.selectbox("Select Group", ["A", "B", "C", "D"], index=2)
selected_date = st.date_input("Select Date", date.today())

# ---------------- CALCULATE SHIFT ----------------
start_date = GROUP_START[group]
days_diff = (selected_date - start_date).days
shift = SHIFT_CYCLE[days_diff % len(SHIFT_CYCLE)]

# ---------------- HIJRI DATE ----------------
hijri = convert.Gregorian(
    selected_date.year,
    selected_date.month,
    selected_date.day
).to_hijri()

hijri_text = f"{hijri.day}-{hijri.month}-{hijri.year}"

# Ramadan & Eid detection
is_ramadan = hijri.month == 9
is_eid = hijri.month == 10 and hijri.day <= 4

# ---------------- DISPLAY RESULT ----------------
color = SHIFT_COLORS[shift]
label = "Shift"

if is_ramadan:
    color = RAMADAN_COLOR
    label = "Ramadan Shift"

if is_eid:
    color = EID_COLOR
    label = "Eid Shift"

st.markdown(
    f"""
    <div style="
        background-color:{color};
        padding:20px;
        border-radius:12px;
        text-align:center;
        font-size:24px;
        font-weight:bold;
    ">
        {label}: {shift}<br>
        Hijri Date: {hijri_text}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- FULL YEAR TABLE ----------------
st.divider()
st.subheader("Full Year Schedule")

rows = []
for i in range(365):
    d = start_date + timedelta(days=i)
    s = SHIFT_CYCLE[i % len(SHIFT_CYCLE)]
    h = convert.Gregorian(d.year, d.month, d.day).to_hijri()

    special = ""
    bg = SHIFT_COLORS[s]

    if h.month == 9:
        special = "Ramadan"
        bg = RAMADAN_COLOR
    if h.month == 10 and h.day <= 4:
        special = "Eid"
        bg = EID_COLOR

    rows.append({
        "Date": d.strftime("%Y-%m-%d"),
        "Hijri": f"{h.day}-{h.month}-{h.year}",
        "Shift": s,
        "Special": special,
        "bg": bg
    })

df = pd.DataFrame(rows)

def style_rows(row):
    return [f"background-color:{row.bg}"] * len(row)

st.dataframe(
    df.drop(columns=["bg"]).style.apply(style_rows, axis=1),
    use_container_width=True
)
