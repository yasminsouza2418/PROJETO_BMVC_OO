from model.user_account import user_account
from system.controller_base import controller_base


class portal_controller(controller_base):
    def index(self):
        if self.esta_logado():
            self.redirecionar('banco')
        self.html(self.view.render('login', {'erro': 'erro' in self.req.query}))

    def login(self):
        d = self.entrada()
        user = user_account(self.req).autenticar(str(d.get('login', '')), str(d.get('senha', '')))

        if not user:
            if self.quer_html():
                self.redirecionar('portal?erro=1')
            self.json({'erro': 'Credenciais inválidas'}, 401)

        self.regenerar_sessao()  # evita fixação de sessão
        self.sessao['user_id'] = user['id']
        self.sessao['user_login'] = user['login']

        if self.quer_html():
            self.redirecionar('banco')
        self.json({'mensagem': 'Login realizado', 'usuario': user['login']})

    def logout(self):
        self.destruir_sessao()
        if self.quer_html():
            self.redirecionar('portal')
        self.json({'mensagem': 'Logout realizado'})
