from flask import redirect, url_for
from flask_login import logout_user, login_required

from controllers.logout_controller import logout_controller

@logout_controller.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_controller.login'))
