
import streamlit as st
import pandas as pd

from database import get_all_patients, get_all_barriers

st.set_page_config(
    page_title="Care Pathway Monitoring | TRACE-Care",
    page_icon="🛤️",
    layout="wide"
)

st.title("🛤️ Patient Care Pathway Monitoring")

st.write(
    "Monitor each patient's journey from screening "
    "to completed follow-up care."
)

st.markdown("---")

patients = get_all_patients()
barriers = get_all_barriers()

if not patients:
    st.warning("No patients registered yet.")

else:

    patient_options = {
        f"{p[1]} - {p[2]}": p[1]
        for p in patients
    }

    selected_patient = st.selectbox(
        "Select Patient",
        list(patient_options.keys())
    )

    patient_id = patient_options[selected_patient]

    patient = next(
        p for p in patients if p[1] == patient_id
    )

    # Find all barriers belonging to this patient
    patient_barriers = [
        b for b in barriers if b[1] == patient_id
    ]

    completed_followup = patient[6] == "Completed"

    st.markdown("---")
    st.header("👤 Patient Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Patient ID:**", patient[1])
        st.write("**Patient Name:**", patient[2])
        st.write("**Screening Type:**", patient[3])

    with col2:
        st.write("**Screening Date:**", patient[4])
        st.write("**Follow-up Status:**", patient[6])

    st.markdown("---")
    st.header("📍 Care Journey")

    # Stage 1: Screening record
    st.subheader("1. Screening Registration")
    st.success(
        f"Screening record registered: {patient[3]}"
    )
    st.caption(f"Recorded screening date: {patient[4]}")

    # Stage 2: Barrier identification
    st.subheader("2. Barrier Identification")

    if patient_barriers:
        st.success(
            f"{len(patient_barriers)} barrier record(s) identified."
        )

        for b in patient_barriers:
            with st.expander(
                f"Case #{b[0]} — {b[2]}"
            ):
                st.write("**Description:**", b[3] or "Not provided")
                st.write("**Barrier Status:**", b[4])

    else:
        st.info("No barrier has been recorded for this patient.")

    # Stage 3: Recommendation and approval
    st.subheader("3. Recommendation & Human Approval")

    if patient_barriers:
        for b in patient_barriers:
            with st.expander(f"Recommendation — Case #{b[0]}"):
                st.write("**Recommended Action:**", b[5] or "Not available")
                st.write("**Reason:**", b[6] or "Not available")
                st.write("**Approval Status:**", b[7])

    else:
        st.info("No recommendation is available yet.")

    # Stage 4: Staff assignment
    st.subheader("4. Staff Assignment")

    assigned_count = sum(1 for b in patient_barriers if b[8])

    if assigned_count:
        st.success(f"{assigned_count} case(s) assigned to staff.")

        for b in patient_barriers:
            if b[8]:
                st.write(
                    f"Case #{b[0]} — Assigned to: **{b[8]}**"
                )
                st.caption(
                    f"Assignment date: {b[10] or 'Not recorded'}"
                )
    else:
        st.warning("No staff assignment recorded yet.")

    # Stage 5: Intervention progress
    st.subheader("5. Intervention Progress")

    completed_actions = sum(
        1 for b in patient_barriers if b[9] == "Completed"
    )

    in_progress_actions = sum(
        1 for b in patient_barriers if b[9] == "In Progress"
    )

    if patient_barriers:
        st.write(f"**Completed interventions:** {completed_actions}")
        st.write(f"**In-progress interventions:** {in_progress_actions}")

        for b in patient_barriers:
            st.write(
                f"Case #{b[0]} — {b[9] or 'Not Started'}"
            )
    else:
        st.info("No intervention records available.")

    # Stage 6: Patient follow-up completion
    st.subheader("6. Patient Follow-up & Care Completion")

    if completed_followup:
        st.success("Patient follow-up care completed!")

    elif patient[6] == "Appointment Scheduled":
        st.info("Appointment scheduled — awaiting completion.")

    elif patient[6] == "Unable to Complete":
        st.warning("Follow-up care could not be completed.")

    else:
        st.warning("Patient follow-up is still pending.")

    st.write(
        "**Follow-up Date:**",
        patient[7] or "Not recorded"
    )

    st.write(
        "**Outcome Notes:**",
        patient[8] or "No outcome notes recorded"
    )

    # Overall pathway summary
    st.markdown("---")
    st.header("📊 Patient Journey Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Barrier Cases", len(patient_barriers))
    col2.metric("Assigned Cases", assigned_count)
    col3.metric("Completed Interventions", completed_actions)

    if completed_followup:
        st.success(
            "CARE PATHWAY OUTCOME: Follow-up completed."
        )
    else:
        st.info(
            "CARE PATHWAY OUTCOME: Follow-up completion is still pending."
        )

st.markdown("---")

st.caption(
    "TRACE-Care | PATHORA | Patient-level care pathway monitoring"
)
