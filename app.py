from flask import Flask
from flask_login import LoginManager
from flask_principal import Principal

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

# Configurando o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# Configurando o Flask-Principal
principal = Principal(app)

# Importando as rotas
from routes.home import home_bp
app.register_blueprint(home_bp)
from routes.login import login_bp
app.register_blueprint(login_bp)

# Iniciando a aplicação
if __name__ == '__main__':
    app.run(debug=True)