
import streamlit as st
from datetime import date
from database import add_patient

st.set_page_config(
    page_title="Patient Registration | TRACE-Care",
    page_icon="🏥",
    layout="wide"
)

st.title("📝 Patient Registration")
st.write("Register a patient for screening-to-care follow-up.")

st.markdown("---")

with st.form("patient_registration_form"):

    st.subheader("Patient Information")

    patient_id = st.text_input("Patient ID", placeholder="Example: TC001")
    patient_name = st.text_input("Patient Name")

    col1, col2 = st.columns(2)

    with col1:
        screening_type = st.selectbox(
            "Screening Type",
            [
                "Diabetic Retinopathy Screening",
                "Breast Cancer Screening",
                "Cervical Cancer Screening",
                "Other"
            ]
        )

    with col2:
        screening_date = st.date_input(
            "Screening Date",
            value=date.today()
        )

    contact = st.text_input(
        "Contact Number",
        placeholder="Enter a demo contact number"
    )

    follow_up_status = st.selectbox(
        "Follow-up Status",
        [
            "Pending",
            "Appointment Scheduled",
            "Completed"
        ]
    )

    submitted = st.form_submit_button("Register Patient")

    if submitted:
        if not patient_id.strip() or not patient_name.strip():
            st.error("Please enter both Patient ID and Patient Name.")
        else:
            success = add_patient(
                patient_id.strip(),
                patient_name.strip(),
                screening_type,
                str(screening_date),
                contact.strip(),
                follow_up_status
            )

            if success:
                st.success("Patient registered and saved successfully!")
                st.write("Patient ID:", patient_id)
                st.write("Patient Name:", patient_name)
            else:
                st.error("This Patient ID already exists. Please use a unique ID.")
