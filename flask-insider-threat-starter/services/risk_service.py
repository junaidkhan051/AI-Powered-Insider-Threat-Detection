from models.risk_score import RiskScore
from extensions import db

def calculate_risk_level(score):
    if score <= 30:
        return 'Low'
    elif score <= 70:
        return 'Medium'
    else:
        return 'High'

def update_user_risk_score(username, points_to_add=0):
    risk = RiskScore.query.filter_by(username=username).first()
    if not risk:
        risk = RiskScore(username=username, score=0, risk_level='Low')
        db.session.add(risk)
    
    risk.score = min(100, risk.score + points_to_add)
    risk.risk_level = calculate_risk_level(risk.score)
    
    db.session.commit()
    return risk
