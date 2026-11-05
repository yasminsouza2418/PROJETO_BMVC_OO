from html import escape


def render(base, erro=False):
    msg = '<p style="color:red">Login ou senha inválidos.</p>' if erro else ''
    return f'''<!DOCTYPE html>
<html lang="pt-br">
<head><meta charset="utf-8"><title>Login</title></head>
<body>
<h1>Login</h1>
{msg}
<form method="post" action="{escape(base)}/portal/login">
    <label>Login <input name="login" required></label><br>
    <label>Senha <input name="senha" type="password" required></label><br>
    <button type="submit">Entrar</button>
</form>
</body>
</html>
'''
