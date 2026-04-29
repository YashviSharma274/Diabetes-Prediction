from flask import Flask, render_template, request

app = Flask(__name__)


def calculate_risk_score(glucose, bmi, age, hba1c, family_history, blood_pressure, activity_level):
    score = 0

    # Fasting plasma glucose (mg/dL)
    if glucose >= 126:
        score += 4
    elif 100 <= glucose < 126:
        score += 2

    # HbA1c (%)
    if hba1c >= 6.5:
        score += 4
    elif 5.7 <= hba1c < 6.5:
        score += 2

    # BMI
    if bmi >= 30:
        score += 2
    elif 25 <= bmi < 30:
        score += 1

    # Age
    if age >= 45:
        score += 1

    # Family history
    if family_history:
        score += 2

    # Blood pressure
    if blood_pressure >= 140:
        score += 1

    # Activity level (self-reported)
    if activity_level == "low":
        score += 1

    return score


def classify_diabetes_stage(glucose, hba1c, score):
    if glucose >= 200 or hba1c >= 8.0:
        return "Likely Diabetes - Advanced Risk", (
            "Your values suggest likely uncontrolled diabetes. "
            "Please consult a doctor urgently for confirmatory tests and treatment planning."
        )

    if glucose >= 126 or hba1c >= 6.5:
        return "Likely Diabetes", (
            "Your values suggest diabetes-range markers. "
            "Please schedule a clinical evaluation for confirmation and management."
        )

    if (100 <= glucose < 126) or (5.7 <= hba1c < 6.5) or score >= 6:
        return "Prediabetes / High Risk", (
            "You may be at high risk for developing diabetes. "
            "Lifestyle changes and periodic screening are strongly recommended."
        )

    return "Low Risk", (
        "Your current profile indicates low risk. "
        "Maintain healthy habits and continue routine checkups."
    )


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    details = None

    if request.method == "POST":
        glucose = float(request.form["glucose"])
        bmi = float(request.form["bmi"])
        age = int(request.form["age"])
        hba1c = float(request.form["hba1c"])
        blood_pressure = int(request.form["blood_pressure"])
        activity_level = request.form["activity_level"]
        family_history = request.form.get("family_history") == "yes"

        score = calculate_risk_score(
            glucose=glucose,
            bmi=bmi,
            age=age,
            hba1c=hba1c,
            family_history=family_history,
            blood_pressure=blood_pressure,
            activity_level=activity_level,
        )

        result, details = classify_diabetes_stage(glucose=glucose, hba1c=hba1c, score=score)
        details = f"{details} (Risk score: {score})"

    return render_template("index.html", result=result, details=details)


if __name__ == "__main__":
    app.run(debug=True)
