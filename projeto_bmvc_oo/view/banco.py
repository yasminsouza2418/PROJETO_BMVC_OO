from html import escape


def _txt(v):
    return escape('' if v is None else str(v))


def render(base, livros, usuario):
    if livros:
        linhas = ''.join(
            f'<tr><td>{_txt(l["id"])}</td><td>{_txt(l["titulo"])}</td>'
            f'<td>{_txt(l["autor"])}</td><td>{_txt(l["ano"])}</td></tr>\n'
            for l in livros)
        conteudo = ('<table border="1" cellpadding="4">\n'
                    '<tr><th>ID</th><th>Titulo</th><th>Autor</th><th>Ano</th></tr>\n'
                    f'{linhas}</table>')
    else:
        conteudo = '<p>Nenhum livro cadastrado. Use o cURL para cadastrar</p>'
    return f'''<!DOCTYPE html>
<html lang="pt-br">
<head><meta charset="utf-8"><title>Livros</title></head>
<body>
<p>Usuário: <strong>{_txt(usuario)}</strong> |
   <a href="{escape(base)}/portal/logout">Sair</a></p>
<h1>Livros</h1>
{conteudo}
</body>
</html>
'''
