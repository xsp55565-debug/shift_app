import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Shift Schedule App", layout="wide")
st.title("Shift Schedule App")

# --- اختيار المجموعة وبداية الدورة ---
groups = ["A", "B", "C", "D"]
default_group_index = groups.index("B")  # B افتراضي
group = st.selectbox("Select Group:", groups, index=default_group_index)

start_date = st.date_input("Select Start Date:", datetime(2026, 1, 18))
st.write("Selected Group:", group)
st.write("Start Date:", start_date.strftime("%d-%m-%Y"))

# --- إنشاء الجدول السنوي ---
schedule = []

# دورة الورديات
def add_shifts(start, shift_type, days):
    for i in range(days):
        date = start + timedelta(days=i)
        schedule.append({
            "Date": date,
            "Shift": shift_type,
            "Color": {
                "Morning": "yellow",
                "Evening": "orange",
                "Night": "lightblue",
                "Off": "lightgray"   # <-- أضفت اللون للـ Off
            }[shift_type]
        })

current_date = start_date
while current_date < start_date + timedelta(days=365):
    # First Night: 7 أيام 10 مساء - 6 صباح
    add_shifts(current_date, "Night", 7)
    current_date += timedelta(days=7)
    # Off: يومين
    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)
    # Second Night / Evening: 7 أيام 2 ظهراً - 10 مساء
    add_shifts(current_date, "Evening", 7)
    current_date += timedelta(days=7)
    # Off: يومين
    add_shifts(current_date, "Off", 2)
    current_date += timedelta(days=2)
    # Morning: 7 أيام 6 صباحاً - 2 ظهراً
    add_shifts(current_date, "Morning", 7)
    current_date += timedelta(days=7)
    # Off: 3 أيام
    add_shifts(current_date, "Off", 3)
    current_date += timedelta(days=3)

# تحويل إلى DataFrame
df = pd.DataFrame(schedule)
df["Date"] = pd.to_datetime(df["Date"])
df_display = df.copy()
df_display["Date"] = df_display["Date"].dt.strftime("%a, %d-%m-%Y")

# --- تلوين الصفوف حسب النوع ---
def color_rows(row):
    return [f"background-color: {row['Color']}"] * len(row)

# إظهار الجدول
st.dataframe(
    df_display.style.apply(color_rows, axis=1),
    use_container_width=True
)
