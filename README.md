# Symptom Expert System (Flask)

Rule-based expert system that ranks cold, flu, COVID-19 and allergy from a patient's symptoms.
Study project only. It is not medical advice.

## Run
    pip install -r requirements.txt
    python app.py
Open http://127.0.0.1:5000

## API
POST /api/diagnose
    {"answers": {"fever": "yes", "dry_cough": "yes", "sneezing": "no"}}
Answers are "yes", "no" or "unknown". Missing symptoms count as "unknown".

## How it works
- knowledge_base.py: symptoms, diseases, IF-THEN rules with certainty factors, red-flag rules
- engine.py: forward chaining + MYCIN certainty-factor combination + explanation of fired rules
- app.py: Flask routes; templates/index.html: questionnaire UI
