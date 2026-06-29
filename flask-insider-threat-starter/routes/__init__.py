from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')
alerts_bp = Blueprint('alerts', __name__, url_prefix='/alerts')
reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
users_bp = Blueprint('users', __name__, url_prefix='/users')
risk_bp = Blueprint('risk', __name__, url_prefix='/risk')
