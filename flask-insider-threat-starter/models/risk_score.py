from extensions import db

class RiskScore(db.Model):
    __tablename__ = 'risk_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    score = db.Column(db.Float, default=0.0) # 0 to 100
    risk_level = db.Column(db.String(64), default='Low') # 'Low', 'Medium', 'High'

    def __repr__(self):
        return f'<RiskScore {self.username}: {self.score} ({self.risk_level})>'
