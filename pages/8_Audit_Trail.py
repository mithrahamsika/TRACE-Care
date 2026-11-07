import streamlit as st
import pandas as pd
from audit import get_audit_logs
from database import get_all_patients

st.set_page_config(
    page_title="Audit Trail | TRACE-Care",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Audit Trail & Case History")

st.write(
    "Track important activities and maintain a transparent "
    "history of patient care coordination."
)

st.markdown("---")

patients = get_all_patients()

if not patients:
    st.info("No patient records available.")
    st.stop()

patient_options = {
    "All Patients": None
}

for patient in patients:
    patient_options[
        f"{patient[1]} - {patient[2]}"
    ] = patient[1]

selected_patient = st.selectbox(
    "Select Patient",
    list(patient_options.keys())
)

patient_id = patient_options[selected_patient]

logs = get_audit_logs(patient_id)

st.subheader("📊 Audit Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Total Recorded Events", len(logs))

if logs:
    event_types = set(log[3] for log in logs)
    col2.metric("Event Categories", len(event_types))

    latest_event = logs[0][6]
    col3.metric("Latest Activity", latest_event)
else:
    col2.metric("Event Categories", 0)
    col3.metric("Latest Activity", "None")

st.markdown("---")
st.subheader("📋 Activity History")

if logs:
    columns = [
        "Log ID",
        "Patient ID",
        "Case ID",
        "Event Type",
        "Event Details",
        "Performed By",
        "Event Time"
    ]

    df = pd.DataFrame(logs, columns=columns)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.subheader("🔎 Event Category Filter")

    categories = sorted(df["Event Type"].unique().tolist())

    selected_categories = st.multiselect(
        "Filter by event type",
        categories,
        default=categories
    )

    filtered_df = df[
        df["Event Type"].isin(selected_categories)
    ]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Audit History as CSV",
        data=csv_data,
        file_name="tracecare_audit_history.csv",
        mime="text/csv"
    )

else:
    st.info(
        "No audit events recorded for this patient yet. "
        "New activities will appear here automatically."
    )

st.markdown("---")

st.caption(
    "TRACE-Care | Audit records support transparency "
    "and accountability. They do not replace official "
    "hospital records."
)
