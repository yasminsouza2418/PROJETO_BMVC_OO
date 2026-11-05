from system.model_base import model_base
from system.seguranca import verificar_senha


class user_account(model_base):
    table = 'user_account'
    fields = ('login', 'senha')

    # Retorna o usuário (sem a senha) ou None
    def autenticar(self, login, senha):
        u = self.db.execute('SELECT * FROM user_account WHERE login = ?', (login,)).fetchone()
        if not u or not verificar_senha(senha, u['senha']):
            return None
        u = dict(u)
        del u['senha']
        return u
