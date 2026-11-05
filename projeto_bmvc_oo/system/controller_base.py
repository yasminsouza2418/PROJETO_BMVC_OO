# Controller genérico: entrada, negociação HTML/JSON e login
import json
from urllib.parse import parse_qs

from system.bmvc_base import bmvc_base
from system.view_base import view_base


class Resposta(Exception):
    """Lançada para encerrar a ação e enviar a resposta (papel do exit do PHP)."""

    def __init__(self, status, corpo, tipo, headers=None):
        super().__init__(status)
        self.status = status
        self.corpo = corpo.encode('utf-8')
        self.headers = {'Content-Type': f'{tipo}; charset=utf-8', **(headers or {})}

    @classmethod
    def json(cls, dados, status=200, headers=None):
        return cls(status, json.dumps(dados, ensure_ascii=False), 'application/json', headers)


class controller_base(bmvc_base):
    def __init__(self, req):
        super().__init__(req)
        self.view = view_base(req)

    # Corpo da requisição: JSON ou formulário
    def entrada(self):
        corpo = self.req.corpo.decode('utf-8', 'replace')
        if 'application/json' in self.req.headers.get('Content-Type', '').lower():
            try:
                dados = json.loads(corpo)
            except ValueError:
                return {}
            return dados if isinstance(dados, dict) else {}
        return {k: v[0] for k, v in parse_qs(corpo, keep_blank_values=True).items()}

    def quer_html(self):
        return 'text/html' in self.req.headers.get('Accept', '').lower()

    def json(self, dados, status=200):
        raise Resposta.json(dados, status)

    def html(self, texto, status=200):
        raise Resposta(status, texto, 'text/html')

    def redirecionar(self, caminho):
        raise Resposta(302, '', 'text/plain', {'Location': self.url(caminho)})

    def exigir_login(self):
        if self.esta_logado():
            return
        if self.quer_html():
            self.redirecionar('portal')
        self.json({'erro': 'Login necessário'}, 401)
