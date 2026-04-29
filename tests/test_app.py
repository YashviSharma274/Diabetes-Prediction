from app import app, calculate_risk_score, classify_diabetes_stage


def test_risk_score_high():
    score = calculate_risk_score(180, 32, 55, 8.2, True, 145, "low")
    assert score >= 10


def test_stage_low_risk():
    stage, _ = classify_diabetes_stage(92, 5.2, 2)
    assert stage == "Low Risk"


def test_index_page_loads():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_prediction_submission():
    client = app.test_client()
    response = client.post(
        "/",
        data={
            "glucose": "130",
            "hba1c": "6.8",
            "bmi": "29",
            "age": "40",
            "blood_pressure": "135",
            "activity_level": "moderate",
            "family_history": "yes",
        },
    )
    assert response.status_code == 200
    assert b"Prediction:" in response.data
