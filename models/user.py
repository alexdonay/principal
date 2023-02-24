class User:
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self):
        return f'<User {self.username}>'


# Importando a lista de usuários
from users import users

# Buscando um usuário pelo nome de usuário
def get_user_by_username(username):
    for user in users:
        if user.username == username:
            return user
    return None
