from model.livro import livro
from system.controller_base import controller_base


class banco_controller(controller_base):
    def __init__(self, req):
        super().__init__(req)
        self.exigir_login()
        self.livro = livro(req)

    # READ (lista)
    def index(self):
        livros = self.livro.all()
        if self.quer_html():
            self.html(self.view.render('banco', {'livros': livros, 'usuario': self.sessao['user_login']}))
        self.json(livros)

    # READ (um registro)
    def ver(self, id):
        l = self.livro.find(int(id))
        if not l:
            self.json({'erro': 'Livro não encontrado'}, 404)
        self.json(l)

    # CREATE
    def criar(self):
        d = self.entrada()
        erros = self.livro.validar(d)
        if erros:
            self.json({'erros': erros}, 422)
        d['ano'] = None if d.get('ano') in (None, '') else int(d['ano'])
        self.json(self.livro.create(d), 201)

    # DELETE
    def remover(self, id):
        if not self.livro.delete(int(id)):
            self.json({'erro': 'Livro não encontrado'}, 404)
        self.json({'mensagem': 'Livro removido', 'id': int(id)})
