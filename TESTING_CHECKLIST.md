# TRACE-Care — Prototype Testing Checklist

## 1. Patient Registration
- [ ] Register a new synthetic patient.
- [ ] Verify patient details appear in Patient Records.
- [ ] Verify duplicate patient IDs are rejected.
- [ ] Verify registration is recorded in the Audit Trail.

## 2. Barrier Identification
- [ ] Select a registered patient.
- [ ] Record a transport barrier.
- [ ] Verify the recommendation matches the selected barrier.
- [ ] Verify the recommendation reason is displayed.
- [ ] Verify the barrier appears in saved records.
- [ ] Verify the event appears in the Audit Trail.

## 3. Human Approval
- [ ] Approve a pending recommendation.
- [ ] Reject another pending recommendation.
- [ ] Verify approval status is saved correctly.
- [ ] Verify both decisions appear in the Audit Trail.

## 4. Staff Assignment
- [ ] Assign an approved case to a staff member.
- [ ] Verify the staff name and assignment date.
- [ ] Verify the assignment appears in the Audit Trail.

## 5. Intervention Progress
- [ ] Change an assigned case to In Progress.
- [ ] Change an intervention to Completed.
- [ ] Verify the updated status is saved.
- [ ] Verify status changes appear in the Audit Trail.

## 6. Patient Follow-up
- [ ] Update a patient's follow-up status.
- [ ] Record a follow-up date and outcome note.
- [ ] Verify the updated details in Patient Records.
- [ ] Verify the event appears in the Audit Trail.

## 7. Care Pathway Monitoring
- [ ] Select a patient with multiple workflow records.
- [ ] Verify barrier cases are displayed.
- [ ] Verify approval and assignment information.
- [ ] Verify intervention progress.
- [ ] Verify follow-up completion status.
- [ ] Check that patient follow-up and intervention completion are shown separately.

## 8. Analytics
- [ ] Verify patient and barrier counts.
- [ ] Verify approval statistics.
- [ ] Verify intervention progress statistics.
- [ ] Verify follow-up completion rate.
- [ ] Check that displayed metrics match the database.

## 9. Audit Trail
- [ ] Verify patient-specific event history.
- [ ] Verify event timestamps and case IDs.
- [ ] Test event category filtering.
- [ ] Test CSV export.
- [ ] Confirm older actions are not falsely represented as historical audit events.

## 10. Final Application Checks
- [ ] All pages open without errors.
- [ ] No Python syntax errors.
- [ ] Existing database records remain available.
- [ ] Navigation works correctly.
- [ ] Only synthetic demonstration data is used.
- [ ] README and architecture documentation are present.

---

## Testing Notes

Record any failed test, error message and correction here.

**Important:** This checklist is a testing plan. A checkbox should only be marked after the corresponding test has actually passed.
