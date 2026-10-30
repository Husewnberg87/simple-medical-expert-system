
from knowledge_base import DISEASES, RED_FLAGS, RULES, SYMPTOMS

VALID_ANSWERS = {"yes", "no", "unknown"}
MIN_CF_TO_REPORT = 0.20  


def normalize(answers):
    clean = {}
    for symptom in SYMPTOMS:
        value = str((answers or {}).get(symptom, "unknown")).lower()
        clean[symptom] = value if value in VALID_ANSWERS else "unknown"
    return clean


def condition_met(condition, facts):
    if condition.startswith("!"):
        return facts.get(condition[1:]) == "no"
    return facts.get(condition) == "yes"


def rule_fires(conditions, facts):
    return all(condition_met(c, facts) for c in conditions)


def combine_cf(cf1, cf2):
    if cf1 >= 0 and cf2 >= 0:
        return cf1 + cf2 * (1 - cf1)
    if cf1 < 0 and cf2 < 0:
        return cf1 + cf2 * (1 + cf1)
    return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))


def diagnose(answers):
    facts = normalize(answers)
    answered_yes = [s for s, v in facts.items() if v == "yes"]

    cf_by_disease = {d: 0.0 for d in DISEASES}
    fired = {d: [] for d in DISEASES}

    for rule_id, conditions, disease, cf, reason in RULES:
        if rule_fires(conditions, facts):
            cf_by_disease[disease] = combine_cf(cf_by_disease[disease], cf)
            fired[disease].append({"id": rule_id, "cf": cf, "reason": reason})

    results = []
    for disease, cf in cf_by_disease.items():
        if cf >= MIN_CF_TO_REPORT:
            results.append({
                "id": disease,
                "name": DISEASES[disease]["name"],
                "confidence": round(cf * 100),
                "advice": DISEASES[disease]["advice"],
                "rules": fired[disease],
            })
    results.sort(key=lambda r: r["confidence"], reverse=True)

    warnings = [msg for _, conds, msg in RED_FLAGS if rule_fires(conds, facts)]

    return {
        "symptoms_reported": [SYMPTOMS[s] for s in answered_yes],
        "results": results,
        "warnings": warnings,
        "inconclusive": len(results) == 0,
    }
