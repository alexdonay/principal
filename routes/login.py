from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_user
from flask_principal import Identity, UserNeed, RoleNeed, identity_changed

login_bp = Blueprint('login', __name__)
from models.user import User, get_user_by_username

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user.password == password:
            login_user(user)
            identity = Identity(user.id)
            identity.provides.add(UserNeed(user.id))
            identity.provides.add(RoleNeed(user.role))
            with login_controller.app_context():
                identity_changed.send(login_controller, identity=identity)
            return redirect(request.args.get('next') or url_for('home_controller.home'))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html')