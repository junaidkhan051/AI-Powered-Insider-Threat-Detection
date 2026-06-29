from extensions import db
from datetime import datetime

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False)
    files_accessed = db.Column(db.Integer, default=0)
    usb_used = db.Column(db.Integer, default=0)
    failed_logins = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<ActivityLog {self.username} at {self.timestamp}>'
