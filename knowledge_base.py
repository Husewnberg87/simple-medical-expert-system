SYMPTOMS = {
    "fever": "Fever (37.8 °C / 100 °F or higher)",
    "high_fever": "High fever (39 °C / 102 °F or higher)",
    "chills": "Chills or shivering",
    "dry_cough": "Dry cough",
    "sore_throat": "Sore throat",
    "runny_nose": "Runny nose",
    "sneezing": "Frequent sneezing",
    "nasal_congestion": "Blocked or stuffy nose",
    "headache": "Headache",
    "body_aches": "Muscle or body aches",
    "fatigue": "Unusual tiredness",
    "loss_smell_taste": "Loss of smell or taste",
    "shortness_of_breath": "Shortness of breath",
    "chest_pain": "Chest pain or pressure",
    "itchy_eyes": "Itchy eyes",
    "watery_eyes": "Watery eyes",
    "itchy_nose_throat": "Itchy nose or throat",
    "sudden_onset": "Symptoms started suddenly (within hours)",
    "gradual_onset": "Symptoms built up slowly (over 1-3 days)",
    "contact_with_sick": "Recent close contact with a sick person",
    "allergen_exposure": "Recent exposure to pollen, dust, or pets",
    "seasonal_pattern": "Similar symptoms happen at the same time every year",
}

DISEASES = {
    "cold": {
        "name": "Common cold",
        "advice": "Rest, drink fluids, and use over-the-counter relief for symptoms. "
                  "It usually clears in 7-10 days.",
    },
    "flu": {
        "name": "Influenza (flu)",
        "advice": "Rest and drink plenty of fluids. See a doctor soon, especially if you are "
                  "elderly, pregnant, or have a chronic condition, because antiviral "
                  "medication works best when started early.",
    },
    "covid": {
        "name": "COVID-19",
        "advice": "Take a COVID-19 test and avoid close contact with others until you know "
                  "the result. Contact a doctor if symptoms worsen.",
    },
    "allergy": {
        "name": "Seasonal / environmental allergy",
        "advice": "Avoid the trigger where possible. Antihistamines often help. "
                  "An allergist can confirm the trigger.",
    },
}

# (rule_id, [conditions], disease, CF, human-readable reason)
RULES = [
    # ---- Common cold ----
    ("C1", ["runny_nose", "sneezing", "sore_throat"], "cold", 0.60,
     "Runny nose, sneezing and sore throat together are the classic cold pattern."),
    ("C2", ["nasal_congestion", "gradual_onset"], "cold", 0.40,
     "A stuffy nose that builds slowly points to a cold."),
    ("C3", ["runny_nose", "!fever"], "cold", 0.30,
     "Nose symptoms without fever fit a mild cold."),
    ("C4", ["sore_throat", "gradual_onset", "!high_fever"], "cold", 0.30,
     "A gradual sore throat without high fever is typical of a cold."),
    ("C5", ["high_fever"], "cold", -0.50,
     "High fever is unusual for a cold."),
    ("C6", ["loss_smell_taste", "!nasal_congestion"], "cold", -0.30,
     "Loss of smell without a blocked nose is not typical of a cold."),

    # ---- Influenza ----
    ("F1", ["high_fever", "body_aches", "sudden_onset"], "flu", 0.80,
     "Sudden high fever with body aches is the hallmark of influenza."),
    ("F2", ["fever", "chills", "fatigue"], "flu", 0.50,
     "Fever, chills and fatigue together are common in flu."),
    ("F3", ["fever", "dry_cough"], "flu", 0.40,
     "Fever with a dry cough is a common flu combination."),
    ("F4", ["headache", "body_aches", "fatigue"], "flu", 0.30,
     "Headache, aches and exhaustion fit flu."),
    ("F5", ["sudden_onset", "fever"], "flu", 0.30,
     "Flu typically starts abruptly."),
    ("F6", ["!fever", "!body_aches"], "flu", -0.50,
     "Flu without fever or body aches is unlikely."),

    # ---- COVID-19 ----
    ("V1", ["loss_smell_taste"], "covid", 0.70,
     "Loss of smell or taste is a strong COVID-19 indicator."),
    ("V2", ["fever", "dry_cough", "fatigue"], "covid", 0.40,
     "Fever, dry cough and fatigue are the common COVID-19 trio."),
    ("V3", ["shortness_of_breath", "fever"], "covid", 0.50,
     "Breathing difficulty with fever raises suspicion of COVID-19."),
    ("V4", ["contact_with_sick", "fever", "dry_cough"], "covid", 0.40,
     "Close contact plus fever and cough raises the chance of an infection."),
    ("V5", ["loss_smell_taste", "!runny_nose"], "covid", 0.20,
     "Loss of smell without a runny nose is more typical of COVID-19."),
    ("V6", ["itchy_eyes", "itchy_nose_throat", "!fever"], "covid", -0.40,
     "Itchy eyes and nose without fever point away from COVID-19."),

    # ---- Allergy ----
    ("A1", ["itchy_eyes", "sneezing"], "allergy", 0.70,
     "Itchy eyes with sneezing are typical of an allergic reaction."),
    ("A2", ["watery_eyes", "itchy_nose_throat"], "allergy", 0.60,
     "Watery eyes and an itchy nose or throat are characteristic of allergy."),
    ("A3", ["seasonal_pattern", "sneezing", "!fever"], "allergy", 0.50,
     "Seasonal recurrence of sneezing without fever strongly suggests allergy."),
    ("A4", ["allergen_exposure", "sneezing"], "allergy", 0.40,
     "Symptoms after exposure to a known trigger suggest allergy."),
    ("A5", ["runny_nose", "!fever", "!body_aches", "!sore_throat"], "allergy", 0.30,
     "A runny nose with no signs of infection fits allergy."),
    ("A6", ["fever"], "allergy", -0.60,
     "Allergies do not cause fever."),
    ("A7", ["body_aches"], "allergy", -0.40,
     "Allergies rarely cause body aches."),
]

# Red-flag rules: if matched, show an urgent warning regardless of the diagnosis.
RED_FLAGS = [
    ("R1", ["shortness_of_breath"],
     "Shortness of breath can be serious. Seek medical care promptly."),
    ("R2", ["chest_pain"],
     "Chest pain or pressure needs urgent medical attention. Call emergency services."),
    ("R3", ["high_fever", "headache", "fatigue", "shortness_of_breath"],
     "This combination of severe symptoms needs medical evaluation today."),
]
