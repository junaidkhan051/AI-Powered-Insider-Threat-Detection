from flask import render_template
from flask_login import login_required
from routes import reports_bp
from services.report_service import get_daily_stats, get_weekly_stats

@reports_bp.route('/')
@login_required
def index():
    # Example report data aggregation
    daily_stats = get_daily_stats()
    weekly_stats = get_weekly_stats()
    return render_template('reports.html', daily_stats=daily_stats, weekly_stats=weekly_stats)
