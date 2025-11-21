import json
import streamlit as st

st.set_page_config(page_title="Scholarship Advisory System", layout="centered")

# -----------------------------
# Default rules in JSON (EXACTLY as given)
# -----------------------------
default_rules_json = """
[
 {
  "name": "Top merit candidate",
  "priority": 100,
  "conditions": [
   ["cgpa", ">=", 3.7],
   ["co_curricular_score", ">=", 80],
   ["family_income", "<=", 8000],
   ["disciplinary_actions", "==", 0]
  ],
  "action": {
   "decision": "AWARD_FULL",
   "reason": "Excellent academic & co-curricular performance, with acceptable need"
  }
 },
 {
  "name": "Good candidate - partial scholarship",
  "priority": 80,
  "conditions": [
   ["cgpa", ">=", 3.3],
   ["co_curricular_score", ">=", 60],
   ["family_income", "<=", 12000],
   ["disciplinary_actions", "<=", 1]
  ],
  "action": {
   "decision": "AWARD_PARTIAL",
   "reason": "Good academic & involvement record with moderate need"
  }
 },
 {
  "name": "Need-based review",
  "priority": 70,
  "conditions": [
   ["cgpa", ">=", 2.5],
   ["family_income", "<=", 4000]
  ],
  "action": {
   "decision": "REVIEW",
   "reason": "High need but borderline academic score"
  }
 },
 {
  "name": "Low CGPA – not eligible",
  "priority": 95,
  "conditions": [
   ["cgpa", "<", 2.5]
  ],
  "action": {
   "decision": "REJECT",
   "reason": "CGPA below minimum scholarship requirement"
  }
 },
 {
  "name": "Serious disciplinary record",
  "priority": 90,
  "conditions": [
   ["disciplinary_actions", ">=", 2]
  ],
  "action": {
   "decision": "REJECT",
   "reason": "Too many disciplinary records"
  }
 }
]
"""

# -----------------------------
# Rule engine
# -----------------------------
def evaluate_applicant(applicant, rules, return_rule=False):
    matched_rules = []

    for rule in rules:
        satisfies_all = True
        for field, operator, value in rule["conditions"]:
            applicant_value = applicant.get(field)

            if operator == ">=" and not (applicant_value >= value):
                satisfies_all = False
                break
            elif operator == "<=" and not (applicant_value <= value):
                satisfies_all = False
                break
            elif operator == ">" and not (applicant_value > value):
                satisfies_all = False
                break
            elif operator == "<" and not (applicant_value < value):
                satisfies_all = False
                break
            elif operator == "==" and not (applicant_value == value):
                satisfies_all = False
                break

        if satisfies_all:
            matched_rules.append(rule)

    if not matched_rules:
        action = {"decision": "NO_DECISION", "reason": "No rules matched"}
        return (action, None) if return_rule else action

    matched_rules.sort(key=lambda r: r.get("priority", 0), reverse=True)
    best_rule = matched_rules[0]

    return (best_rule["action"], best_rule) if return_rule else best_rule["action"]


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🎓 Scholarship Advisory Rule-Based System")
st.write("This app evaluates scholarship eligibility using configurable rules.")

# Sidebar – JSON rule editor
st.sidebar.header("Rule Configuration (JSON)")
rules_text = st.sidebar.text_area(
    "Edit rules (JSON format)",
    value=default_rules_json,
    height=400
)

try:
    rules = json.loads(rules_text)
    rules_valid = True
except json.JSONDecodeError as e:
    st.sidebar.error(f"Invalid JSON: {e}")
    rules_valid = False
    rules = []

# Main form – applicant info
st.header("Applicant Information")

cgpa = st.number_input("Cumulative GPA (CGPA)", min_value=0.0, max_value=4.0, value=3.5, step=0.01)
family_income = st.number_input("Monthly family income (RM)", min_value=0, max_value=100000, value=5000, step=100)
co_score = st.slider("Co-curricular involvement score", min_value=0, max_value=100, value=70)
community_hours = st.number_input("Community service hours", min_value=0, max_value=1000, value=10)
semester = st.number_input("Current semester of study", min_value=1, max_value=12, value=3)
disciplinary = st.number_input("Number of disciplinary actions on record", min_value=0, max_value=10, value=0)

if st.button("Evaluate Scholarship"):
    if not rules_valid:
        st.error("Please fix the JSON rules in the sidebar before evaluating.")
    else:
        applicant_data = {
            "cgpa": cgpa,
            "family_income": family_income,
            "co_curricular_score": co_score,
            "community_service_hours": community_hours,
            "current_semester": semester,
            "disciplinary_actions": disciplinary
        }

        action, fired_rule = evaluate_applicant(applicant_data, rules, return_rule=True)

        st.subheader("Decision")
        st.success(f"Decision: {action['decision']}")
        st.write(f"Reason: {action['reason']}")

        if fired_rule:
            st.caption(f"Matched rule: **{fired_rule['name']}** (priority {fired_rule['priority']})")
        else:
            st.caption("No rule matched.")
