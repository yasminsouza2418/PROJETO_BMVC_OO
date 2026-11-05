from system.model_base import model_base


class livro(model_base):
    table = 'livro'
    fields = ('titulo', 'autor', 'ano')

    # Dicionário de erros; vazio se os dados forem válidos
    def validar(self, d):
        erros = {}
        if not str(d.get('titulo') or '').strip():
            erros['titulo'] = 'Título é obrigatório'
        if not str(d.get('autor') or '').strip():
            erros['autor'] = 'Autor é obrigatório'
        ano = d.get('ano')
        if ano not in (None, '') and not str(ano).isdigit():
            erros['ano'] = 'Ano deve ser numérico'
        return erros
