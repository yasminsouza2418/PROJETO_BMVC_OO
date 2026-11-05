#!/usr/bin/env python3
# Front controller: servidor HTTP que despacha cada rota ao controller
import re
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit

from controller.banco_controller import banco_controller
from controller.portal_controller import portal_controller
from system.bmvc_config import bmvc_config
from system.controller_base import Resposta

# padrão => {método: (controller, ação)}
ROTAS = [
    (r'/', {'GET': (portal_controller, 'index')}),
    (r'/portal', {'GET': (portal_controller, 'index')}),
    (r'/portal/login', {'POST': (portal_controller, 'login')}),
    (r'/portal/logout', {'GET': (portal_controller, 'logout')}),
    (r'/banco', {'GET': (banco_controller, 'index'), 'POST': (banco_controller, 'criar')}),
    (r'/banco/(\d+)', {'GET': (banco_controller, 'ver'), 'DELETE': (banco_controller, 'remover')}),
]


class Handler(BaseHTTPRequestHandler):
    def despachar(self):
        self.cookies = []  # Set-Cookie gerados pela sessão
        try:
            tamanho = int(self.headers.get('Content-Length') or 0)
            self.corpo = self.rfile.read(tamanho) if tamanho else b''
            url = urlsplit(self.path)
            self.query = parse_qs(url.query)

            base = bmvc_config.get()['base_url']
            caminho = url.path
            if base and caminho.startswith(base):
                caminho = caminho[len(base):]
            caminho = '/' + caminho.strip('/')

            for padrao, metodos in ROTAS:
                m = re.fullmatch(padrao, caminho)
                if not m:
                    continue
                if self.command not in metodos:
                    raise Resposta.json({'erro': 'Método não permitido'}, 405, {'Allow': ', '.join(metodos)})
                classe, acao = metodos[self.command]
                getattr(classe(self), acao)(*m.groups())
                raise RuntimeError(f'{classe.__name__}.{acao} terminou sem resposta')
            raise Resposta.json({'erro': 'Rota não encontrada'}, 404)
        except Resposta as r:
            self.enviar(r)
        except Exception:
            traceback.print_exc()
            self.enviar(Resposta.json({'erro': 'Erro interno'}, 500))

    def enviar(self, r):
        self.send_response(r.status)
        for k, v in r.headers.items():
            self.send_header(k, v)
        for c in self.cookies:
            self.send_header('Set-Cookie', c)
        self.send_header('Content-Length', str(len(r.corpo)))
        self.end_headers()
        self.wfile.write(r.corpo)

    do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = despachar


if __name__ == '__main__':
    cfg = bmvc_config.get()
    print(f"Servidor em http://localhost:{cfg['porta']}")
    # Servidor de uma thread: a conexão SQLite única não é compartilhada entre threads
    HTTPServer(('localhost', cfg['porta']), Handler).serve_forever()
