from flask import render_template, request
from flask_login import login_required
from routes import users_bp
from models.user import User
from models.risk_score import RiskScore
from models.activity_log import ActivityLog
from models.threat_alert import ThreatAlert
from extensions import db
from sqlalchemy import func

@users_bp.route('/')
@login_required
def index():
    # Query parameters
    search_query = request.args.get('q', '').strip()
    dept_filter = request.args.get('dept', '').strip()
    risk_filter = request.args.get('risk', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Base query combining User and RiskScore
    query = db.session.query(User, RiskScore).outerjoin(RiskScore, User.username == RiskScore.username)
    query = query.filter(User.role != 'admin')

    if search_query:
        query = query.filter(User.username.ilike(f'%{search_query}%') | User.email.ilike(f'%{search_query}%'))

    if dept_filter:
        query = query.filter(User.department == dept_filter)

    if risk_filter:
        query = query.filter(RiskScore.risk_level == risk_filter)

    # Global Quick Statistics (unfiltered overall stats)
    total_users = User.query.filter(User.role != 'admin').count()
    isolated_users = User.query.filter_by(status='Isolated').count()
    high_risk_users = RiskScore.query.filter_by(risk_level='High').count()
    
    avg_score_raw = db.session.query(func.avg(RiskScore.score)).scalar()
    avg_score = round(avg_score_raw, 1) if avg_score_raw is not None else 0.0

    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    users_data = []
    for user, risk in pagination.items:
        # Fetch the user's latest activity log
        last_log = ActivityLog.query.filter_by(username=user.username).order_by(ActivityLog.timestamp.desc()).first()
        last_activity = last_log.timestamp.strftime('%b %d, %H:%M') if last_log else 'No Activity'

        users_data.append({
            'user': user,
            'risk_level': risk.risk_level if risk else 'Low',
            'score': round(risk.score, 1) if risk else 0.0,
            'last_activity': last_activity
        })

    # Fetch unique departments for filter dropdown
    depts = [d[0] for d in db.session.query(User.department).filter(User.department != None).distinct().all()]

    return render_template('users.html',
                           users_data=users_data,
                           pagination=pagination,
                           depts=depts,
                           selected_dept=dept_filter,
                           selected_risk=risk_filter,
                           search_query=search_query,
                           total_users=total_users,
                           isolated_users=isolated_users,
                           high_risk_users=high_risk_users,
                           avg_score=avg_score)


@users_bp.route('/<username>/activity')
@login_required
def activity_logs(username):
    logs = ActivityLog.query.filter_by(username=username).order_by(ActivityLog.timestamp.desc()).all()
    return render_template('activity_logs.html', username=username, logs=logs)

@users_bp.route('/activity')
@login_required
def all_activity_logs():
    q_user = request.args.get('user', '').strip()
    q_dept = request.args.get('dept', '').strip()
    q_type = request.args.get('type', '').strip()
    
    query = db.session.query(ActivityLog, User).outerjoin(User, ActivityLog.username == User.username)
    
    if q_user:
        query = query.filter(ActivityLog.username.ilike(f'%{q_user}%'))
    if q_dept:
        query = query.filter(User.department == q_dept)
    if q_type == 'file':
        query = query.filter(ActivityLog.files_accessed > 0)
    elif q_type == 'usb':
        query = query.filter(ActivityLog.usb_used > 0)
    elif q_type == 'login':
        query = query.filter(ActivityLog.failed_logins > 0)
        
    logs_data = query.order_by(ActivityLog.timestamp.desc()).limit(100).all()
    
    depts = [d[0] for d in db.session.query(User.department).filter(User.department != None).distinct().all()]
    users_list = [u[0] for u in db.session.query(User.username).filter(User.role != 'admin').distinct().all()]

    return render_template('activity_logs.html', 
                           username='All Users', 
                           logs_data=logs_data,
                           depts=depts,
                           users_list=users_list,
                           selected_user=q_user,
                           selected_dept=q_dept,
                           selected_type=q_type)

@users_bp.route('/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    risk = RiskScore.query.filter_by(username=username).first()
    
    # Activity and alert history
    recent_activities = ActivityLog.query.filter_by(username=username).order_by(ActivityLog.timestamp.desc()).limit(10).all()
    threat_history = ThreatAlert.query.filter_by(username=username).order_by(ThreatAlert.timestamp.desc()).all()
    
    # Calculate behavior statistics
    total_files = db.session.query(func.sum(ActivityLog.files_accessed)).filter_by(username=username).scalar() or 0
    avg_files = db.session.query(func.avg(ActivityLog.files_accessed)).filter_by(username=username).scalar() or 0.0
    total_usb = db.session.query(func.sum(ActivityLog.usb_used)).filter_by(username=username).scalar() or 0
    total_failed_logins = db.session.query(func.sum(ActivityLog.failed_logins)).filter_by(username=username).scalar() or 0
    threats_count = len(threat_history)
    
    stats = {
        'total_files': total_files,
        'avg_files': round(avg_files, 1),
        'total_usb': total_usb,
        'total_failed_logins': total_failed_logins,
        'threats_count': threats_count
    }
    
    return render_template('user_profile.html',
                           user=user,
                           risk=risk,
                           recent_activities=recent_activities,
                           threat_history=threat_history,
                           stats=stats)


