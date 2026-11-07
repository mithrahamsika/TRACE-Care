
import streamlit as st
import pandas as pd

from datetime import date

from database import (
    get_all_patients,
    update_patient_followup
)

st.set_page_config(
    page_title="Follow-up Tracking | TRACE-Care",
    page_icon="📅",
    layout="wide"
)

st.title("📅 Patient Follow-up & Care Completion Tracking")

st.write(
    "Monitor whether patients successfully complete their "
    "follow-up care after screening."
)

st.markdown("---")

# Retrieve patients
patients = get_all_patients()

if not patients:
    st.warning("No patients registered yet.")

else:

    patient_options = {
        f"{p[1]} - {p[2]}": p
        for p in patients
    }

    st.subheader("Select Patient")

    selected_patient = st.selectbox(
        "Choose a patient",
        list(patient_options.keys())
    )

    patient = patient_options[selected_patient]

    patient_id = patient[1]

    st.markdown("---")

    # Patient details
    st.subheader("Patient Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Patient ID:**", patient[1])
        st.write("**Patient Name:**", patient[2])
        st.write("**Screening Type:**", patient[3])

    with col2:
        st.write("**Screening Date:**", patient[4])
        st.write("**Contact:**", patient[5])

    st.markdown("---")

    # Follow-up tracking form
    st.subheader("Update Follow-up Outcome")

    current_status = patient[6] or "Pending"

    status_options = [
        "Pending",
        "Appointment Scheduled",
        "Completed",
        "Unable to Complete"
    ]

    follow_up_status = st.selectbox(
        "Follow-up Status",
        status_options,
        index=(
            status_options.index(current_status)
            if current_status in status_options else 0
        )
    )

    current_date = patient[7] if len(patient) > 7 else None

    if current_date:
        try:
            default_date = date.fromisoformat(current_date)
        except ValueError:
            default_date = date.today()
    else:
        default_date = date.today()

    follow_up_date = st.date_input(
        "Follow-up Date",
        value=default_date
    )

    current_notes = (
        patient[8]
        if len(patient) > 8 and patient[8]
        else ""
    )

    outcome_notes = st.text_area(
        "Outcome Notes",
        value=current_notes,
        placeholder="Enter follow-up outcome details..."
    )

    if st.button("Save Follow-up Details", type="primary"):

        success = update_patient_followup(
            patient_id,
            follow_up_status,
            str(follow_up_date),
            outcome_notes
        )

        if success:
            st.success("Follow-up details saved successfully!")
            st.rerun()
        else:
            st.error("Unable to update patient follow-up details.")

    st.markdown("---")

    # Care completion indicator
    st.subheader("Care Completion Status")

    if follow_up_status == "Completed":
        st.success("Follow-up care completed!")

    elif follow_up_status == "Appointment Scheduled":
        st.info("Appointment scheduled — awaiting completion.")

    elif follow_up_status == "Unable to Complete":
        st.warning("Follow-up care could not be completed.")

    else:
        st.warning("Follow-up care is still pending.")

    st.markdown("---")

# Overview of all patient follow-ups
st.subheader("📋 Follow-up Records Overview")

if patients:

    refreshed_patients = get_all_patients()

    overview = []

    for p in refreshed_patients:
        overview.append({
            "Patient ID": p[1],
            "Patient Name": p[2],
            "Screening Type": p[3],
            "Follow-up Status": p[6],
            "Follow-up Date": p[7],
            "Outcome Notes": p[8]
        })

    df = pd.DataFrame(overview)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    completed = sum(
        1 for p in refreshed_patients
        if p[6] == "Completed"
    )

    total = len(refreshed_patients)

    col1, col2 = st.columns(2)

    col1.metric("Total Patients", total)
    col2.metric("Follow-ups Completed", completed)

    st.progress(completed / total if total else 0)

    st.caption(
        f"{completed} out of {total} patients have completed follow-up care."
    )

else:
    st.info("No follow-up records available.")
