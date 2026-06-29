from models.activity_log import ActivityLog
from models.threat_alert import ThreatAlert
from datetime import datetime, timedelta

def get_daily_stats():
    today = datetime.utcnow().date()
    start_of_day = datetime(today.year, today.month, today.day)
    
    activities_today = ActivityLog.query.filter(ActivityLog.timestamp >= start_of_day).count()
    alerts_today = ThreatAlert.query.filter(ThreatAlert.timestamp >= start_of_day).count()
    
    return {
        'activities': activities_today,
        'alerts': alerts_today
    }

def get_weekly_stats():
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    activities_week = ActivityLog.query.filter(ActivityLog.timestamp >= week_ago).count()
    alerts_week = ThreatAlert.query.filter(ThreatAlert.timestamp >= week_ago).count()
    
    return {
        'activities': activities_week,
        'alerts': alerts_week
    }
