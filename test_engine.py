from engine import combine_cf, diagnose


def top(answers):
    r = diagnose(answers)
    return r["results"][0]["id"] if r["results"] else None


def test_combine_cf():
    assert abs(combine_cf(0.6, 0.4) - 0.76) < 1e-9
    assert abs(combine_cf(0.8, -0.5) - 0.6) < 1e-9


def test_flu():
    assert top({"high_fever": "yes", "fever": "yes", "body_aches": "yes", "sudden_onset": "yes",
                "chills": "yes", "fatigue": "yes"}) == "flu"


def test_allergy():
    assert top({"itchy_eyes": "yes", "sneezing": "yes", "fever": "no", "seasonal_pattern": "yes"}) == "allergy"


def test_covid():
    assert top({"loss_smell_taste": "yes", "fever": "yes", "dry_cough": "yes", "fatigue": "yes"}) == "covid"


def test_cold():
    assert top({"runny_nose": "yes", "sneezing": "yes", "sore_throat": "yes", "fever": "no"}) == "cold"


def test_unknown_creates_no_evidence():
    assert diagnose({})["inconclusive"] is True


def test_red_flag():
    assert diagnose({"chest_pain": "yes"})["warnings"]
