from flask import render_template, Blueprint
from flask_principal import Permission, RoleNeed


home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template('home.html')

