from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin,current_user
from flask_principal import Principal, Identity, AnonymousIdentity, RoleNeed, UserNeed, Permission, identity_changed, identity_loaded

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# configurando o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)
# configurando o Flask-Principal
principal = Principal(app)

# criando um usuário para fins de exemplo
class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f'<User {self.username}>'

# criando uma lista de usuários para fins de exemplo
users = [
    User(id=1, username='admin', password='admin', role='admin'),
    User(id=2, username='user', password='user', role='user')
]

# buscando um usuário pelo ID
def get_user_by_id(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

# buscando um usuário pelo nome de usuário
def get_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))
# verificando se um usuário tem uma permissão
def user_has_permission(user, permission_name):
    if user.role == 'admin':
        return True
    elif user.role == 'user':
        if permission_name == 'view':
            return True
    return False

# criando uma permissão para visualizar conteúdo
view_permission = Permission(RoleNeed('admin'), 'view')

# criando uma página inicial com conteúdo restrito
@app.route('/')
@login_required
@view_permission.require()
def home():
    return render_template('home.html')
# criando uma página de login
@app.route('/login', methods=['GET', 'POST'])
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
            with app.app_context():
                identity_changed.send(app, identity=identity)
            return redirect(request.args.get('next') or url_for('home'))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html')

# criando uma página de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
