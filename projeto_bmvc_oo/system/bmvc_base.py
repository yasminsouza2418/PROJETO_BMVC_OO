# Classe-mãe de todas as classes MVC: config, banco e sessão
import secrets
from http.cookies import SimpleCookie

from system.bmvc_config import bmvc_config
from system.db_connection import db_connection

COOKIE = 'BMVCSESSID'
# Sessões ficam na memória do processo e somem ao reiniciar o servidor
_SESSOES = {}


class bmvc_base:
    def __init__(self, req):
        self.req = req  # requisição atual (o handler HTTP)
        self.config = bmvc_config.get()
        self.db = db_connection.get(self.config)
        self.iniciar_sessao()

    def iniciar_sessao(self):
        if hasattr(self.req, 'sessao'):
            return  # já iniciada nesta requisição
        cookie = SimpleCookie(self.req.headers.get('Cookie', ''))
        sid = cookie[COOKIE].value if COOKIE in cookie else None
        if sid not in _SESSOES:  # modo estrito: id desconhecido gera sessão nova
            sid = self._novo_id({})
        self.req.sid = sid
        self.req.sessao = _SESSOES[sid]

    def _novo_id(self, dados):
        sid = secrets.token_urlsafe(32)
        _SESSOES[sid] = dados
        self.req.cookies.append(f'{COOKIE}={sid}; Path=/; HttpOnly; SameSite=Lax')
        return sid

    def regenerar_sessao(self):
        # Novo id com os mesmos dados (evita fixação de sessão)
        dados = _SESSOES.pop(self.req.sid)
        self.req.sid = self._novo_id(dados)

    def destruir_sessao(self):
        _SESSOES.pop(self.req.sid, None)
        self.req.sessao.clear()
        self.req.cookies.append(f'{COOKIE}=; Path=/; Max-Age=0')

    @property
    def sessao(self):
        return self.req.sessao

    def esta_logado(self):
        return bool(self.sessao.get('user_id'))

    def url(self, caminho=''):
        return self.config['base_url'] + '/' + caminho.lstrip('/')
