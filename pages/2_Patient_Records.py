
import streamlit as st
import pandas as pd

from database import get_all_patients

st.set_page_config(
    page_title="Patient Records | TRACE-Care",
    page_icon="🏥",
    layout="wide"
)

st.title("📋 Patient Records")
st.write("View all patients registered in TRACE-Care.")

st.markdown("---")

patients = get_all_patients()

if patients:

    columns = [
        "Database ID",
        "Patient ID",
        "Patient Name",
        "Screening Type",
        "Screening Date",
        "Contact",
        "Follow-up Status",
        "Follow-up Date",
        "Outcome Notes"
    ]

    df = pd.DataFrame(
        patients,
        columns=columns
    )

    st.metric(
        "Total Registered Patients",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        "No patient records found. Register a patient first."
    )
