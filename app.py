from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()
weights = {
    'savingstoincomescore': 0.08,
    'expensepercentagescore': 0.22,
    'loanpercentagescore': 0.12,
    'creditutilizationscore': 0.33,
    'lifestylescore': 0.25
}

class FamilyInput(BaseModel):
    family_id: str
    savings_to_income: float
    expense_percentage: float
    loan_percentage: float
    credit_utilization_percentage: float
    lavish_to_necessity: float

def calculate_financial_score(data):
    return (
        data['savings_to_income'] * weights['savingstoincomescore'] +
        data['expense_percentage'] * weights['expensepercentagescore'] +
        data['loan_percentage'] * weights['loanpercentagescore'] +
        data['credit_utilization_percentage'] * weights['creditutilizationscore'] +
        data['lavish_to_necessity'] * weights['lifestylescore']
    )

def generate_recommendations(row):
    recommendations = []
    if row['savings_to_income'] < 18:
        recommendations.append('Try saving more of your money wrt income.')
    if row['expense_percentage'] < 17:
        recommendations.append('Attempt reducing your expenses.')
    if row['loan_percentage'] < 20:
        recommendations.append('Perhaps try reducing your debt burden.')
    if row['credit_utilization_percentage'] < 20:
        recommendations.append('Try cutting back on credit card purchases.')
    if row['lavish_to_necessity'] < 47:
        recommendations.append('Try being more mindful of your purchase requirements.')
    return recommendations

@app.get("/")
def hello():
    return {"Crazy": "Frog"}

@app.post("/calculatescore")
def calculate_score(input_data: FamilyInput):

    data = input_data.dict()
    financial_score = calculate_financial_score(data)
    recommendations = generate_recommendations(data)
    return {
        "family_id": input_data.family_id,
        "financial_score": financial_score,
        "recommendations": recommendations
    }
