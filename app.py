import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- Google Sheets setup ---
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

# 🟢 Replace this with the name of your JSON key file
creds = Credentials.from_service_account_file("training-tracker-app-483413-c4d72f4a26f9.json", scopes=scope)
client = gspread.authorize(creds)

# 🟢 Replace this with the exact name of your Google Sheet
sheet = client.open("Training Records").sheet1

# --- Streamlit App ---
st.set_page_config(page_title="Training Tracker", page_icon="📋")

st.title("📋 Company Training Tracker")

menu = ["Training Input", "Training Records"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Training Input":
    st.subheader("Add New Training Record")

    name = st.text_input("Staff Name")
    staff_id = st.text_input("Staff ID")
    department = st.text_input("Department")
    training_name = st.text_input("Training Name")
    training_date = st.date_input("Training Date")
    training_hours = st.number_input("Training Hours", min_value=0.0, step=0.01)

    if st.button("Submit"):
        if name and staff_id and training_name and training_date:
            sheet.append_row([name, staff_id, department, training_name, str(training_date), training_hours])
            st.success("✅ Training record added successfully!")
        else:
            st.warning("⚠️ Please fill in all fields.")

elif choice == "Training Records":
    st.subheader("📚 View Your Training History")

    staff_id = st.text_input("Enter Your Staff ID")

    if st.button("Search"):
        records = sheet.get_all_records()
        df = pd.DataFrame(records)

        if not df.empty and "Staff ID" in df.columns:
            filtered = df[df["Staff ID"].astype(str) == staff_id]

            if not filtered.empty:
                st.success(f"Showing records for Staff ID: {staff_id}")
                st.dataframe(filtered)

                # Calculate total training hours
                if "Training Hours" in filtered.columns:
                    total_hours = filtered["Training Hours"].sum()
                    st.info(f"**Total Training Hours:** {total_hours} hours")
            else:
                st.warning("No records found for this Staff ID.")
        else:
            st.error("⚠️ No data found in Google Sheet or column names are missing.")
