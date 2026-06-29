from extensions import db
from datetime import datetime

class ThreatAlert(db.Model):
    __tablename__ = 'threat_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False)
    threat_type = db.Column(db.String(120), nullable=False) # e.g., 'Abnormal File Access', 'Multiple Failed Logins'
    severity = db.Column(db.String(64), nullable=False) # e.g., 'Low', 'Medium', 'High'
    description = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f'<ThreatAlert {self.severity} for {self.username}>'
