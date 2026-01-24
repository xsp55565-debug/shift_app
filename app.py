import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from hijri_converter import convert

st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --- Groups ---
groups = ["A", "B", "C", "D"]
default_group_index = groups.index("B")
group = st.selectbox("Select Group:", groups, index=default_group_index)

# --- Start date ---
start_date = st.date_input("Select Start Date:", datetime.today())
st.write("Selected Group:", group)
st.write("Start Date:", start_date.strftime("%d-%m-%Y"))

# --- Shift schedule creation ---
schedule = []

def add_shifts(start, shift_type, days):
    for i in range(days):
        date = start + timedelta(days=i)
        hijri_date = convert.Gregorian(date.year, date.month, date.day).to_hijri()
        hijri_str = f"{hijri_date.day}-{hijri_date.month}-{hijri_date.year}"
        # Mark Ramadan and Eid
        if hijri_date.month == 9:
            hijri_str += " Ramadan"
        if hijri_date.month == 10 and hijri_date.day in [1, 2]:
            hijri_str += " Eid"
        schedule.append({
            "Date": date,
            "Shift": shift_type,
            "Hijri": hijri_str
        })

# --- Shift cycle ---
current_date = start_date
while current_date < start_date + timedelta(days=365):
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

# --- Convert to DataFrame ---
df = pd.DataFrame(schedule)
df["Date"] = pd.to_datetime(df["Date"])
df_display = df.copy()
df_display["Date"] = df_display["Date"].dt.strftime("%a, %d-%m-%Y")

# --- Color function based on Hijri ---
def color_rows(row):
    if "Ramadan" in row['Hijri']:
        return ["background-color: lightgreen"] * len(row)
    elif "Eid" in row['Hijri']:
        return ["background-color: gold"] * len(row)
    else:
        return [""] * len(row)

# --- Display the table ---
st.dataframe(
    df_display.style.apply(color_rows, axis=1),
    use_container_width=True
)

# --- Check shift for a specific date ---
selected_date = st.date_input("Check your shift on a specific date:")
if selected_date:
    row = df[df['Date'] == pd.to_datetime(selected_date)]
    if not row.empty:
        st.write("Your shift:", row.iloc[0]["Shift"])
        st.write("Hijri date:", row.iloc[0]["Hijri"])
    else:
        st.write("No shift found for this date.")
