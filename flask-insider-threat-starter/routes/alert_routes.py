from flask import render_template
from flask_login import login_required
from routes import alerts_bp
from models.threat_alert import ThreatAlert
from extensions import db

@alerts_bp.route('/')
@login_required
def index():
    # Fetch all alerts for the live feed
    alerts = ThreatAlert.query.order_by(ThreatAlert.timestamp.desc()).limit(100).all()
    
    # Latest alerts for the right panel ticker
    latest_alerts = alerts[:8] if alerts else []
    
    # Statistics
    critical_count = ThreatAlert.query.filter_by(severity='Critical').count()
    high_count = ThreatAlert.query.filter_by(severity='High').count()
    medium_count = ThreatAlert.query.filter_by(severity='Medium').count()
    low_count = ThreatAlert.query.filter_by(severity='Low').count()
    
    # Threat Categories breakdown for charts/feed
    categories_raw = db.session.query(ThreatAlert.threat_type, db.func.count(ThreatAlert.id)).group_by(ThreatAlert.threat_type).all()
    category_labels = [c[0] for c in categories_raw]
    category_data = [c[1] for c in categories_raw]

    return render_template('alerts.html', 
                           alerts=alerts,
                           latest_alerts=latest_alerts,
                           critical_count=critical_count,
                           high_count=high_count,
                           medium_count=medium_count,
                           low_count=low_count,
                           category_labels=category_labels,
                           category_data=category_data)

@alerts_bp.route('/<int:alert_id>/investigate')
@login_required
def investigate(alert_id):
    from models.user import User
    from models.risk_score import RiskScore
    from models.activity_log import ActivityLog
    
    alert = ThreatAlert.query.get_or_404(alert_id)
    user = User.query.filter_by(username=alert.username).first()
    risk = RiskScore.query.filter_by(username=alert.username).first()
    
    # Fetch recent activities for this user around the time of the alert
    # For a simple timeline, just get the user's latest 10 activities or activities before the alert.
    recent_activities = ActivityLog.query.filter_by(username=alert.username).order_by(ActivityLog.timestamp.desc()).limit(10).all()
    
    return render_template('threat_investigation.html', 
                           alert=alert, 
                           user=user, 
                           risk=risk, 
                           recent_activities=recent_activities)
