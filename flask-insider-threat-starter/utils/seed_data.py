import random
from app import create_app
from extensions import db
from models.user import User
from models.activity_log import ActivityLog
from models.threat_alert import ThreatAlert
from models.risk_score import RiskScore
from services.ai_service import evaluate_user_activity
from services.risk_service import update_user_risk_score
from datetime import datetime, timedelta

def seed_database():
    app = create_app()
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        print("Creating admin and dummy users...")
        # Admin user
        admin = User(username='admin', email='admin@gmail.com', role='admin')
        admin.set_password('1234')
        db.session.add(admin)

        # 50 users
        users = []
        departments = ['Engineering', 'Finance', 'Human Resources', 'Sales', 'Operations', 'Marketing']
        for i in range(1, 51):
            status = random.choices(['Active', 'Isolated', 'Suspended'], weights=[92, 5, 3])[0]
            dept = random.choice(departments)
            user = User(
                username=f'employee{i}',
                email=f'employee{i}@gmail.com',
                department=dept,
                status=status
            )
            user.set_password('abcd')
            db.session.add(user)
            users.append(user)
        
        db.session.commit()

        print("Generating 500 activity logs and checking for threats...")
        # 500 activity logs
        threat_types = ['Abnormal File Access', 'Multiple Failed Logins', 'Suspicious USB Activity', 'Data Exfiltration Attempt']
        
        for _ in range(500):
            user = random.choice(users)
            
            # Mostly normal behavior, some anomalies
            is_anomaly_injection = random.random() < 0.1
            
            if is_anomaly_injection:
                files = random.randint(50, 200)
                usb = random.randint(2, 10)
                failed = random.randint(3, 10)
            else:
                files = random.randint(0, 20)
                usb = random.choice([0, 0, 0, 1])
                failed = random.choice([0, 0, 0, 0, 1])

            timestamp = datetime.utcnow() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))

            log = ActivityLog(
                username=user.username,
                files_accessed=files,
                usb_used=usb,
                failed_logins=failed,
                timestamp=timestamp
            )
            db.session.add(log)
            db.session.commit() # commit to get log saved

            # Evaluate with AI
            activity_data = {
                'files_accessed': files,
                'usb_used': usb,
                'failed_logins': failed
            }
            
            is_threat = evaluate_user_activity(activity_data)
            
            if is_threat:
                # Add threat alert
                severity = random.choice(['Medium', 'High'])
                threat_type = random.choice(threat_types)
                
                alert = ThreatAlert(
                    username=user.username,
                    threat_type=threat_type,
                    severity=severity,
                    description=f"AI detected anomalous behavior: {files} files, {usb} USB uses, {failed} failed logins.",
                    timestamp=timestamp
                )
                db.session.add(alert)
                
                # Update risk score
                points = 10 if severity == 'Medium' else 25
                update_user_risk_score(user.username, points)
            else:
                update_user_risk_score(user.username, 0) # Just to ensure risk record exists

        db.session.commit()
        print("Database seeded successfully with users, logs, alerts, and risk scores!")

if __name__ == '__main__':
    seed_database()
