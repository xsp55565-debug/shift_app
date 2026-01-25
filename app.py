import streamlit as st
import pandas as pd
from hijri_converter import convert
from datetime import datetime, timedelta

st.set_page_config(page_title="Yearly Shift Schedule", layout="wide")

st.title("Yearly Shift Schedule")

# --- Prepare shift data ---
start_date = datetime(2026, 1, 25)
num_days = 30  # Number of days to display
shifts = ["Morning", "Evening", "Night"]

data = []
for i in range(num_days):
    date = start_date + timedelta(days=i)
    shift = shifts[i % 3]
    hijri_date = convert.Gregorian(date.year, date.month, date.day).to_hijri()
    hijri_str = f"{hijri_date.day}/{hijri_date.month}/{hijri_date.year}H"
    data.append({
        "Gregorian Date": date.strftime("%Y-%m-%d"),
        "Hijri Date": hijri_str,
        "Shift": shift
    })

df = pd.DataFrame(data)

# --- Function to color only the shift words ---
def color_shifts(val):
    if val == "Morning":
        return "color: blue; font-weight: bold"
    elif val == "Evening":
        return "color: orange; font-weight: bold"
    elif val == "Night":
        return "color: purple; font-weight: bold"
    else:
        return ""

# --- Highlight Ramadan and Eid on Hijri dates ---
def highlight_holidays(row):
    hijri_parts = row["Hijri Date"].split("/")
    day, month, year = int(hijri_parts[0]), int(hijri_parts[1]), int(hijri_parts[2].replace("H",""))
    # Ramadan = month 9
    # Eid al-Fitr = 10/1 to 10/3, Eid al-Adha = 12/10 to 12/12
    if month == 9:
        return ["background-color: #FFF2CC" if col in ["Hijri Date","Gregorian Date"] else "" for col in row.index]
    elif month == 10 and 1 <= day <= 3:
        return ["background-color: #FFD966" if col in ["Hijri Date","Gregorian Date"] else "" for col in row.index]
    elif month == 12 and 10 <= day <= 12:
        return ["background-color: #FFD966" if col in ["Hijri Date","Gregorian Date"] else "" for col in row.index]
    else:
        return [""] * len(row)

# --- Display the table ---
st.dataframe(
    df.style.applymap(color_shifts, subset=["Shift"])
           .apply(highlight_holidays, axis=1)
)
