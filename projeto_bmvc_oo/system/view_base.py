# Renderiza um template de view/ com as variáveis informadas
import importlib

from system.bmvc_base import bmvc_base


class view_base(bmvc_base):
    def render(self, nome, dados=None):
        modulo = importlib.import_module(f'view.{nome}')
        return modulo.render(base=self.config['base_url'], **(dados or {}))
