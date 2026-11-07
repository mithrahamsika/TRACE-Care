
import streamlit as st
import pandas as pd

from database import get_all_patients, get_all_barriers

st.set_page_config(
    page_title="Analytics | TRACE-Care",
    page_icon="📊",
    layout="wide"
)

st.title("📊 TRACE-Care Analytics & Insights")

st.write(
    "Understand patient follow-up progress, identified barriers, "
    "and healthcare intervention performance."
)

st.markdown("---")

# Retrieve database records
patients = get_all_patients()
barriers = get_all_barriers()

total_patients = len(patients)
total_barriers = len(barriers)

# Patient analytics
completed_followups = sum(
    1 for p in patients if p[6] == "Completed"
)

followup_rate = (
    completed_followups / total_patients * 100
    if total_patients else 0
)

# Barrier analytics
resolved_barriers = sum(
    1 for b in barriers if b[4] == "Resolved"
)

barrier_resolution_rate = (
    resolved_barriers / total_barriers * 100
    if total_barriers else 0
)

# Approval analytics
approved = sum(
    1 for b in barriers if b[7] == "Approve"
)

rejected = sum(
    1 for b in barriers if b[7] == "Reject"
)

pending = sum(
    1 for b in barriers if b[7] == "Pending"
)

# Intervention analytics
assigned = sum(
    1 for b in barriers if b[8]
)

completed_actions = sum(
    1 for b in barriers if b[9] == "Completed"
)

in_progress_actions = sum(
    1 for b in barriers if b[9] == "In Progress"
)

not_started_actions = sum(
    1 for b in barriers if b[9] == "Not Started"
)

# Summary metrics
st.header("📌 Overall Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", total_patients)
col2.metric("Total Barriers", total_barriers)
col3.metric("Resolved Barriers", resolved_barriers)
col4.metric("Completed Follow-ups", completed_followups)

st.markdown("---")

# Care completion
st.header("🎯 Patient Follow-up Analysis")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Follow-up Completion Rate",
        f"{followup_rate:.1f}%"
    )

    st.progress(followup_rate / 100)

with col2:
    st.metric(
        "Barrier Resolution Rate",
        f"{barrier_resolution_rate:.1f}%"
    )

    st.progress(barrier_resolution_rate / 100)

# Follow-up status distribution
if patients:

    followup_data = pd.DataFrame([
        {
            "Follow-up Status": p[6] or "Unknown"
        }
        for p in patients
    ])

    followup_counts = (
        followup_data["Follow-up Status"]
        .value_counts()
    )

    st.subheader("Follow-up Status Distribution")
    st.bar_chart(followup_counts)

else:
    st.info("No patient data available for follow-up analysis.")

st.markdown("---")

# Barrier distribution
st.header("🔍 Barrier Analysis")

if barriers:

    barrier_data = pd.DataFrame([
        {
            "Barrier": b[2],
            "Barrier Status": b[4]
        }
        for b in barriers
    ])

    barrier_counts = barrier_data["Barrier"].value_counts()

    st.subheader("Most Frequently Identified Barriers")
    st.bar_chart(barrier_counts)

    st.subheader("Barrier Resolution Status")

    resolution_counts = (
        barrier_data["Barrier Status"].value_counts()
    )

    st.bar_chart(resolution_counts)

else:
    st.info("No barrier records available.")

st.markdown("---")

# Approval analysis
st.header("👨‍⚕️ Human Approval Analysis")

approval_data = pd.DataFrame({
    "Approval Status": ["Approved", "Rejected", "Pending"],
    "Number of Cases": [approved, rejected, pending]
})

st.bar_chart(
    approval_data.set_index("Approval Status")
)

# Intervention analysis
st.markdown("---")

st.header("⚙️ Intervention Progress Analysis")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Assigned Cases", assigned)
col2.metric("Not Started", not_started_actions)
col3.metric("In Progress", in_progress_actions)
col4.metric("Completed", completed_actions)

action_data = pd.DataFrame({
    "Action Status": [
        "Not Started",
        "In Progress",
        "Completed"
    ],
    "Number of Cases": [
        not_started_actions,
        in_progress_actions,
        completed_actions
    ]
})

st.subheader("Intervention Status Distribution")

st.bar_chart(
    action_data.set_index("Action Status")
)

st.markdown("---")

# Detailed patient pathway table
st.header("📋 Patient Care Pathway Overview")

if patients:

    pathway_records = []

    for p in patients:
        pathway_records.append({
            "Patient ID": p[1],
            "Patient Name": p[2],
            "Screening Type": p[3],
            "Follow-up Status": p[6],
            "Follow-up Date": p[7] or "Not Scheduled"
        })

    pathway_df = pd.DataFrame(pathway_records)

    st.dataframe(
        pathway_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No patient pathway records available.")

st.markdown("---")

st.caption(
    "TRACE-Care | PATHORA | Analytics based on recorded prototype data."
)
