# TRACE-Care
### Transparent Recovery & Action Coordination Engine for Care

**A barrier-aware patient care coordination platform designed to help close the gap between healthcare screening and completed follow-up care.**

Developed by **PATHORA** | HealthTech Innovation Prototype

---

## 1. Problem Statement

Many patients do not complete the follow-up care recommended after a healthcare screening. Barriers such as transportation difficulties, financial constraints, language differences and appointment unavailability can interrupt the journey from screening to care.

Healthcare teams may identify missed follow-ups without having a structured way to identify the underlying barriers, coordinate suitable interventions and monitor whether patients successfully return to care.

## 2. Our Solution

TRACE-Care is a digital care coordination prototype that helps healthcare teams identify follow-up barriers, generate explainable operational recommendations, obtain human approval, assign responsibilities and monitor patient care progress.

Instead of relying only on generic appointment reminders, TRACE-Care connects **barrier identification, recommended action, staff accountability and follow-up outcome tracking** in one workflow.

## 3. Key Features

- **Patient Registration:** Register and maintain patient screening records.
- **Patient Records:** View registered patient information and follow-up details.
- **Barrier Identification:** Record barriers affecting follow-up care.
- **Explainable Recommendation Engine:** Generate rule-based operational recommendations with reasons.
- **Human Approval Workflow:** Allow healthcare staff to approve or reject recommendations.
- **Staff Assignment:** Assign approved cases to responsible staff members.
- **Intervention Tracking:** Monitor intervention progress from Not Started to In Progress and Completed.
- **Follow-up Tracking:** Record follow-up status, dates and outcome notes.
- **Care Pathway Monitoring:** View the patient's journey across the care coordination workflow.
- **Analytics & Insights:** Monitor patient counts, barriers, approvals, interventions and follow-up completion.
- **Audit Trail:** Maintain a record of important workflow activities.

## 4. How It Works

```text
Patient Registration
        |
        v
Barrier Identification
        |
        v
Explainable Recommendation
        |
        v
Human Approval / Rejection
        |
        v
Staff Assignment
        |
        v
Intervention Progress Tracking
        |
        v
Patient Follow-up Tracking
        |
        v
Care Pathway Monitoring
        |
        v
Analytics and Audit Trail
```

## 5. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web interface |
| SQLite | Local database |
| Pandas | Data processing and analytics |
| Git & GitHub | Version control and project hosting |

## 6. Recommendation Engine

TRACE-Care uses a transparent rule-based recommendation engine.

| Identified Barrier | Suggested Operational Action |
|---|---|
| Transport Difficulty | Navigator-assisted transport support |
| Financial Difficulty | Financial assistance support referral |
| Language Barrier | Arrange language assistance or interpreter |
| Appointment Unavailable | Find an alternative appointment or provider |
| Unable to Contact Patient | Verify contact details and approved alternative channel |
| Unclear Instructions | Staff-assisted clarification |
| Fear or Anxiety | Supportive patient navigator conversation |
| Other / Unknown | Manual staff review |

Recommendations are operational suggestions and require human review. The system does not independently make clinical decisions.

## 7. System Architecture

```text
             Streamlit User Interface
                       |
          +------------+------------+
          |            |            |
      Patient       Workflow      Analytics
      Modules        Modules       Modules
          |            |            |
          +------------+------------+
                       |
              Python Application
                       |
          +------------+------------+
          |                         |
    Recommendation              Database
       Engine                    Layer
          |                         |
          +------------+------------+
                       |
                  SQLite DB
```

## 8. Project Structure
## 8. Project Structure

```text
PATHORA/
│
├── app.py
├── database.py
├── engine.py
├── audit.py
├── ARCHITECTURE.md
├── README.md
├── requirements.txt
├── TESTING_CHECKLIST.md
├── .gitignore
│
└── pages/
    ├── 1_Patient_Registration.py
    ├── 2_Patient_Records.py
    ├── 3_Barrier_Identification.py
    ├── 4_Case_Management.py
    ├── 5_Follow_Up_Tracking.py
    ├── 6_Analytics.py
    ├── 7_Care_Pathway_Monitoring.py
    └── 8_Audit_Trail.py
```


## 9. Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Git
- Visual Studio Code (recommended)

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd PATHORA
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

## 10. Testing

A dedicated `TESTING_CHECKLIST.md` is included to verify:

- Patient registration and record consistency.
- Barrier identification and recommendation accuracy.
- Human approval and staff assignment.
- Intervention and follow-up tracking.
- Care pathway monitoring.
- Analytics and database consistency.
- Audit trail integrity.
- Application stability.

Only tests that have actually passed should be marked as completed.

## 11. Privacy and Responsible Use

- Use synthetic demonstration data only.
- Do not upload real patient names, contact details or medical records.
- Recommendations are operational suggestions, not diagnoses or treatment instructions.
- Human approval is required before recommendations are acted upon.
- TRACE-Care is an academic innovation prototype and is not a certified clinical system.

## 12. Current Scope and Future Enhancements

**Current prototype scope**
- Local SQLite database.
- Rule-based explainable recommendations.
- Human-in-the-loop approval.
- Staff assignment and intervention tracking.
- Follow-up monitoring and analytics.

**Potential future enhancements**
- FHIR-based healthcare interoperability.
- Integration with hospital information systems.
- Community support and resource directories.
- Multilingual patient communication.
- Secure deployment and role-based access.
- Advanced intervention effectiveness and equity analytics.

## 13. Project Vision

TRACE-Care aims to make the transition from screening to follow-up care more transparent, coordinated and accountable by helping healthcare teams understand barriers and organize appropriate support.

**Identify the barrier. Coordinate the action. Track the outcome. Close the care loop.**

---

**Developed by PATHORA**  
HealthTech Innovation | 2026
