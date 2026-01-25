import streamlit as st
import pandas as pd
from hijri_converter import convert
from datetime import datetime, timedelta

st.set_page_config(page_title="Yearly Shift Schedule", layout="wide")
st.title("Yearly Shift Schedule")

# --- Prepare shift data ---
start_date = datetime(2026, 1, 25)
num_days = 30
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

# --- Color shifts ---
def color_shifts(val):
    if val == "Morning":
        return "color: blue; font-weight: bold"
    elif val == "Evening":
        return "color: orange; font-weight: bold"
    elif val == "Night":
        return "color: purple; font-weight: bold"
    else:
        return ""

# --- Color Hijri date for Ramadan and Eid ---
def color_hijri(val):
    try:
        parts = val.split("/")
        day = int(parts[0])
        month = int(parts[1])
        # Ramadan
        if month == 9:
            return "color: green; font-weight: bold"
        # Eid al-Fitr: 1 Shawwal
        elif month == 10 and day == 1:
            return "color: red; font-weight: bold"
        # Eid al-Adha: 10 Dhu al-Hijjah
        elif month == 12 and day == 10:
            return "color: red; font-weight: bold"
        else:
            return ""
    except:
        return ""

# --- Display dataframe ---
st.dataframe(
    df.style.applymap(color_shifts, subset=["Shift"])
           .applymap(color_hijri, subset=["Hijri Date"])
)
