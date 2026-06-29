from flask import render_template
from flask_login import login_required
from routes import risk_bp
from models.risk_score import RiskScore
from models.user import User
from models.threat_alert import ThreatAlert
from extensions import db
from sqlalchemy import func
from datetime import datetime, timedelta

@risk_bp.route('/')
@login_required
def index():
    # 1. Risk Distribution Data
    risk_scores = RiskScore.query.all()
    avg_score = sum(r.score for r in risk_scores) / len(risk_scores) if risk_scores else 0
    low_count = sum(1 for r in risk_scores if r.risk_level == 'Low')
    med_count = sum(1 for r in risk_scores if r.risk_level == 'Medium')
    high_count = sum(1 for r in risk_scores if r.risk_level == 'High')
    
    # 2. Department Risk Levels
    # Query: Department, Average Score, High Risk Count
    dept_stats_raw = db.session.query(
        User.department,
        func.avg(RiskScore.score).label('avg_score'),
        func.sum(db.case((RiskScore.risk_level == 'High', 1), else_=0)).label('high_risk_count')
    ).join(RiskScore, User.username == RiskScore.username).group_by(User.department).all()
    
    dept_labels = [d.department for d in dept_stats_raw if d.department]
    dept_avg_scores = [round(d.avg_score, 1) if d.avg_score else 0 for d in dept_stats_raw if d.department]
    dept_high_risks = [d.high_risk_count or 0 for d in dept_stats_raw if d.department]

    # 3. Threat Trends (Last 7 Days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    # Since sqlite doesn't easily format date in group_by across dialects easily without func.date (which works in sqlite/mysql/pg),
    # let's just query last 7 days and process in Python for robustness.
    recent_alerts = ThreatAlert.query.filter(ThreatAlert.timestamp >= seven_days_ago).all()
    trend_data = {}
    for i in range(7):
        day = (datetime.utcnow() - timedelta(days=6-i)).strftime('%b %d')
        trend_data[day] = 0
        
    for alert in recent_alerts:
        day_str = alert.timestamp.strftime('%b %d')
        if day_str in trend_data:
            trend_data[day_str] += 1
            
    trend_labels = list(trend_data.keys())
    trend_counts = list(trend_data.values())

    # 4. Top Risk Users
    top_risk_users = db.session.query(User, RiskScore).join(
        RiskScore, User.username == RiskScore.username
    ).order_by(RiskScore.score.desc()).limit(6).all()

    return render_template(
        'risk_analysis.html', 
        avg_score=round(avg_score, 1),
        risk_data=[low_count, med_count, high_count],
        dept_labels=dept_labels,
        dept_avg_scores=dept_avg_scores,
        dept_high_risks=dept_high_risks,
        trend_labels=trend_labels,
        trend_counts=trend_counts,
        top_risk_users=top_risk_users
    )
