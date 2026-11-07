
import streamlit as st
import pandas as pd

from database import get_all_patients, get_all_barriers

st.set_page_config(
    page_title="TRACE-Care Dashboard",
    page_icon="🏥",
    layout="wide"
)

# Retrieve live database records
patients = get_all_patients()
barriers = get_all_barriers()

# Patient metrics
total_patients = len(patients)

completed_followups = sum(
    1 for p in patients if p[6] == "Completed"
)

pending_followups = total_patients - completed_followups

completion_rate = (
    completed_followups / total_patients
    if total_patients > 0 else 0
)

# Barrier and intervention metrics
total_barriers = len(barriers)

approved_cases = sum(
    1 for b in barriers if b[7] == "Approve"
)

pending_approvals = sum(
    1 for b in barriers if b[7] == "Pending"
)

assigned_cases = sum(
    1 for b in barriers if b[8]
)

completed_interventions = sum(
    1 for b in barriers if b[9] == "Completed"
)

# Dashboard heading
st.title("🏥 TRACE-Care")
st.subheader(
    "Transparent Recovery & Action Coordination Engine for Care"
)

st.write(
    "A barrier-aware healthcare coordination platform "
    "designed to support patients from screening to completed follow-up care."
)

st.markdown("---")

st.header("📊 Care Pathway Dashboard")

# Main metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Patients",
    total_patients
)

col2.metric(
    "Follow-ups Not Completed",
    pending_followups
)

col3.metric(
    "Barriers Identified",
    total_barriers
)

col4.metric(
    "Care Completed",
    completed_followups
)

st.markdown("---")

# Workflow metrics
st.subheader("⚙️ Intervention Workflow")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Approved Recommendations",
    approved_cases
)

col2.metric(
    "Pending Approvals",
    pending_approvals
)

col3.metric(
    "Staff-Assigned Cases",
    assigned_cases
)

col4.metric(
    "Completed Interventions",
    completed_interventions
)

st.markdown("---")

# Care completion progress
st.subheader("🎯 Patient Care Completion")

st.write(
    f"**{completed_followups} out of {total_patients} patients "
    "have completed follow-up care.**"
)

st.progress(completion_rate)

st.metric(
    "Care Completion Rate",
    f"{completion_rate * 100:.1f}%"
)

st.markdown("---")

# Patient records preview
st.subheader("👥 Recent Patient Records")

if patients:

    patient_data = []

    for p in patients:
        patient_data.append({
            "Patient ID": p[1],
            "Patient Name": p[2],
            "Screening Type": p[3],
            "Follow-up Status": p[6],
            "Follow-up Date": p[7] or "Not Scheduled"
        })

    patient_df = pd.DataFrame(patient_data)

    st.dataframe(
        patient_df.head(5),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No patients registered yet.")

st.markdown("---")

# Barrier records preview
st.subheader("🔍 Recent Barrier Cases")

if barriers:

    barrier_data = []

    for b in barriers:
        barrier_data.append({
            "Case ID": b[0],
            "Patient ID": b[1],
            "Barrier": b[2],
            "Approval Status": b[7],
            "Assigned To": b[8] or "Not Assigned",
            "Action Status": b[9] or "Not Started"
        })

    barrier_df = pd.DataFrame(barrier_data)

    st.dataframe(
        barrier_df.head(5),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No barriers identified yet.")

st.markdown("---")

st.caption(
    "TRACE-Care | PATHORA | Healthcare Follow-up Coordination Prototype"
)

