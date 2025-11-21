# -----------------------------
# Scholarship Rules
# -----------------------------
rules = [
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

# -------------------------------------------------------
# Function: Evaluate applicant based on rules
# -------------------------------------------------------
def evaluate_applicant(data):
    matched_rules = []

    for rule in rules:
        satisfies_all = True

        for field, operator, value in rule["conditions"]:
            applicant_value = data[field]

            if operator == ">=" and not (applicant_value >= value):
                satisfies_all = False
            elif operator == "<=" and not (applicant_value <= value):
                satisfies_all = False
            elif operator == ">" and not (applicant_value > value):
                satisfies_all = False
            elif operator == "<" and not (applicant_value < value):
                satisfies_all = False
            elif operator == "==" and not (applicant_value == value):
                satisfies_all = False

        if satisfies_all:
            matched_rules.append(rule)

    # If nothing matches
    if not matched_rules:
        return {"decision": "NO_DECISION", "reason": "No rules matched"}

    # Choose the rule with the highest priority
    matched_rules.sort(key=lambda r: r["priority"], reverse=True)
    best_rule = matched_rules[0]

    return best_rule["action"]


# -------------------------------------------------------
# Example test (you can change these values)
# -------------------------------------------------------
applicant = {
    "cgpa": 3.6,
    "co_curricular_score": 70,
    "family_income": 5000,
    "disciplinary_actions": 0
}

result = evaluate_applicant(applicant)
print("Decision:", result["decision"])
print("Reason:", result["reason"])
