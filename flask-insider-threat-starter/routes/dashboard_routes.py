# pyrefly: ignore [missing-import]
from flask import render_template
from flask_login import login_required
from routes import dashboard_bp
from models.user import User
from models.activity_log import ActivityLog
from models.threat_alert import ThreatAlert
from models.risk_score import RiskScore
from sqlalchemy import func
from flask import redirect, url_for
from flask_login import current_user

@dashboard_bp.route('/')
def landing():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('landing.html')

@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_users = User.query.count()
    total_activities = ActivityLog.query.count()
    threats_detected = ThreatAlert.query.count()
    high_risk_users = RiskScore.query.filter_by(risk_level='High').count()
    
    recent_alerts = ThreatAlert.query.order_by(ThreatAlert.timestamp.desc()).limit(5).all()
    
    # Data for charts (simplified)
    # Threat trends (count of alerts per severity)
    low_threats = ThreatAlert.query.filter_by(severity='Low').count()
    medium_threats = ThreatAlert.query.filter_by(severity='Medium').count()
    high_threats = ThreatAlert.query.filter_by(severity='High').count()
    threat_trends = [low_threats, medium_threats, high_threats]

    # Risk distribution
    low_risk = RiskScore.query.filter_by(risk_level='Low').count()
    medium_risk = RiskScore.query.filter_by(risk_level='Medium').count()
    high_risk = RiskScore.query.filter_by(risk_level='High').count()
    risk_distribution = [low_risk, medium_risk, high_risk]

    top_risk_users = RiskScore.query.order_by(RiskScore.score.desc()).limit(5).all()

    return render_template('dashboard.html', 
                           total_users=total_users,
                           total_activities=total_activities,
                           threats_detected=threats_detected,
                           high_risk_users=high_risk_users,
                           recent_alerts=recent_alerts,
                           threat_trends=threat_trends,
                           risk_distribution=risk_distribution,
                           top_risk_users=top_risk_users)

@dashboard_bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@dashboard_bp.route('/notifications')
@login_required
def notifications():
    return render_template('notifications.html')

@dashboard_bp.route('/profile')
@login_required
def profile():
    return render_template('admin_profile.html')
