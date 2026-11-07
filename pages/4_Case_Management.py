
import streamlit as st
import pandas as pd

from database import (
    get_approved_barriers,
    assign_case,
    update_action_status
)

st.set_page_config(
    page_title="Case Management | TRACE-Care",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Staff Assignment & Action Tracking")

st.write(
    "Assign approved recommendations to healthcare staff "
    "and monitor intervention progress."
)

st.markdown("---")

# Retrieve approved cases
approved_cases = get_approved_barriers()

if not approved_cases:
    st.info(
        "No approved cases available. "
        "Approve a recommendation in Barrier Identification first."
    )

else:
    st.subheader("Approved Cases")

    case_options = {
        f"Case #{r[0]} | {r[1]} | {r[2]}": r
        for r in approved_cases
    }

    selected_case = st.selectbox(
        "Select a case",
        list(case_options.keys())
    )

    record = case_options[selected_case]

    # Display case information
    st.markdown("### Case Details")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Patient ID:**", record[1])
        st.write("**Barrier:**", record[2])
        st.write("**Barrier Status:**", record[4])

    with col2:
        st.write("**Recommended Action:**", record[5])
        st.write("**Recommendation Reason:**", record[6])
        st.write("**Approval Status:**", record[7])

    st.markdown("---")

    # Staff assignment
    st.subheader("Assign Healthcare Staff")

    staff_name = st.text_input(
        "Staff Member Name",
        value=record[8] or ""
    )

    if st.button("Assign Case", type="primary"):
        if not staff_name.strip():
            st.error("Please enter a staff member name.")
        else:
            assign_case(record[0], staff_name.strip())
            st.success("Case assigned successfully!")
            st.rerun()

    st.write("**Currently Assigned To:**",
             record[8] if record[8] else "Not Assigned")

    st.write("**Assignment Date:**",
             record[10] if record[10] else "Not Assigned")

    st.markdown("---")

    # Action progress
    st.subheader("Update Action Progress")

    current_status = record[9] or "Not Started"

    status_options = [
        "Not Started",
        "In Progress",
        "Completed"
    ]

    selected_status = st.selectbox(
        "Action Status",
        status_options,
        index=status_options.index(current_status)
        if current_status in status_options else 0
    )

    if st.button("Update Action Status"):
        if not record[8]:
            st.error("Please assign a staff member first.")
        else:
            update_action_status(
                record[0],
                selected_status
            )
            st.success("Action status updated successfully!")
            st.rerun()

    st.markdown("---")

    # All approved cases overview
    st.subheader("📋 Approved Case Overview")

    overview = []

    for r in approved_cases:
        overview.append({
            "Case ID": r[0],
            "Patient ID": r[1],
            "Barrier": r[2],
            "Assigned To": r[8] or "Not Assigned",
            "Action Status": r[9] or "Not Started",
            "Assigned Date": r[10] or "Not Assigned"
        })

    df = pd.DataFrame(overview)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
