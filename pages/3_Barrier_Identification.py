
import streamlit as st
from database import (
    add_barrier,
    get_all_patients,
    get_all_barriers,
    update_approval
)
from engine import recommend_action

st.set_page_config(
    page_title="Barrier Identification | TRACE-Care",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Barrier Identification")
st.write(
    "Identify follow-up barriers and generate explainable "
    "recommendations for healthcare staff."
)

st.markdown("---")

# Patient selection
patients = get_all_patients()

if not patients:
    st.warning("Please register a patient first.")

else:
    patient_options = {
        f"{patient[1]} - {patient[2]}": patient[1]
        for patient in patients
    }

    st.subheader("Patient Details")

    selected_patient = st.selectbox(
        "Select Patient",
        list(patient_options.keys())
    )

    patient_id = patient_options[selected_patient]

    st.markdown("---")
    st.subheader("Follow-up Barrier")

    barrier = st.selectbox(
        "Select the identified barrier",
        [
            "Select a barrier",
            "Transport Difficulty",
            "Financial Difficulty",
            "Language Barrier",
            "Appointment Unavailable",
            "Unable to Contact Patient",
            "Unclear Instructions",
            "Fear or Anxiety",
            "Other / Unknown"
        ]
    )

    description = st.text_area(
        "Additional Details",
        placeholder="Describe the patient's reported barrier..."
    )

    barrier_status = st.selectbox(
        "Barrier Status",
        ["Unresolved", "In Progress", "Resolved"]
    )

    # Generate recommendation
    recommendation = None

    if barrier != "Select a barrier":
        recommendation = recommend_action(barrier)

        st.markdown("---")
        st.subheader("💡 TRACE-Care Recommendation")

        st.info(
            f"Recommended Action: {recommendation['action']}"
        )

        st.write("**Reason:**", recommendation["reason"])

    # Save barrier and recommendation
    if st.button("Save Barrier & Recommendation", type="primary"):

        if barrier == "Select a barrier":
            st.error("Please select a barrier.")

        else:
            add_barrier(
                patient_id,
                barrier,
                description,
                barrier_status,
                recommendation["action"],
                recommendation["reason"]
            )

            st.success(
                "Barrier and recommendation saved! "
                "Approval status: Pending."
            )

st.markdown("---")

# Human approval section
st.header("👨‍⚕️ Human Approval Workflow")
st.write("Review recommendations before allowing them to proceed.")

all_barriers = get_all_barriers()

pending_barriers = [
    record for record in all_barriers
    if record[7] == "Pending"
]

if not pending_barriers:
    st.info("No recommendations are waiting for approval.")

else:
    approval_options = {
        f"Case #{record[0]} | {record[1]} | {record[2]}": record
        for record in pending_barriers
    }

    selected_case = st.selectbox(
        "Select a recommendation to review",
        list(approval_options.keys())
    )

    record = approval_options[selected_case]

    st.write("**Patient ID:**", record[1])
    st.write("**Barrier:**", record[2])
    st.write("**Recommended Action:**", record[5])
    st.write("**Reason:**", record[6])

    decision = st.radio(
        "Staff Decision",
        ["Approve", "Reject"],
        horizontal=True
    )

    if st.button("Submit Staff Decision"):
        update_approval(record[0], decision)
        st.success(f"Recommendation {decision.lower()}d successfully!")
        st.rerun()

# Display all saved records
st.markdown("---")
st.subheader("📋 Saved Barrier Records")

if all_barriers:
    for record in all_barriers:
        with st.expander(
            f"Case #{record[0]} | {record[1]} | {record[2]}"
        ):
            st.write("**Description:**", record[3])
            st.write("**Barrier Status:**", record[4])
            st.write("**Recommended Action:**", record[5])
            st.write("**Reason:**", record[6])
            st.write("**Approval Status:**", record[7])
else:
    st.info("No barrier records available.")

