import streamlit as st
import pandas as pd
from datetime import date, timedelta
from hijri_converter import convert

st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# -------------------------------
# GROUP START DATES (FIXED)
# -------------------------------
group_start_dates = {
    "A": date(2026, 1, 11),
    "B": date(2026, 1, 18),
    "C": date(2026, 1, 25),  # Sunday 25
    "D": date(2026, 2, 1)
}

groups = ["A", "B", "C", "D"]
group = st.selectbox("Select Group", groups, index=groups.index("C"))

start_date = group_start_dates[group]

st.write("Group:", group)
st.write("Cycle Start Date:", start_date.strftime("%d-%m-%Y"))

# -------------------------------
# BUILD SHIFT SCHEDULE
# -------------------------------
schedule = []

def add_shifts(start, shift_type, days):
    for i in range(days):
        d = start + timedelta(days=i)
        hijri = convert.Gregorian(d.year, d.month, d.day).to_hijri()
        schedule.append({
            "Date": d,
            "Hijri Date": f"{hijri.day}-{hijri.month}-{hijri.year}",
            "Shift": shift_type
        })

current_date = start_date
end_date = start_date + timedelta(days=365)

while current_date < end_date:
    add_shifts(current_date, "Night", 7)
    current_date += timedelta(days=7)

    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)

    add_shifts(current_date, "Evening", 7)
    current_date += timedelta(days=7)

    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)

    add_shifts(current_date, "Morning", 7)
    current_date += timedelta(days=7)

    add_shifts(current_date, "Off", 3)
    current_date += timedelta(days=3)

df = pd.DataFrame(schedule)
df["Date"] = pd.to_datetime(df["Date"])

# -------------------------------
# CHECK SHIFT BY DATE
# -------------------------------
st.divider()
st.subheader("Check Shift by Date")

selected_date = st.date_input("Select a date", date.today())

result = df[df["Date"] == pd.to_datetime(selected_date)]

if not result.empty:
    row = result.iloc[0]
    st.success(
        f"Date: {selected_date.strftime('%d-%m-%Y')}  |  "
        f"Hijri: {row['Hijri Date']}  |  "
        f"Shift: **{row['Shift']}**"
    )
else:
    st.warning("Date is outside the schedule range")

# -------------------------------
# DISPLAY FULL TABLE
# -------------------------------
st.divider()
st.subheader("Full Year Schedule")

df_display = df.copy()
df_display["Date"] = df_display["Date"].dt.strftime("%a %d-%m-%Y")

st.dataframe(df_display, use_container_width=True)
