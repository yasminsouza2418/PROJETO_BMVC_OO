# BMVC em Python — Livros

Micro-framework didático no estilo BMVC, em Python 3.8+ puro (só biblioteca padrão:
`http.server`, `sqlite3`, `hashlib`), sem frameworks nem pip.

## Como iniciar

```bash
python3 index.py
```

Abra http://localhost:8000. O `banco.sqlite` é criado na primeira requisição.
As sessões ficam em memória: reiniciar o servidor desloga todo mundo.

**Credenciais:** `admin` / `admin123`

## Rotas

| Método | Rota            | Ação                              |
|--------|-----------------|-----------------------------------|
| GET    | `/`, `/portal`  | Tela de login                     |
| POST   | `/portal/login` | Autentica                         |
| GET    | `/portal/logout`| Encerra a sessão                  |
| GET    | `/banco`        | Lista livros (HTML ou JSON)       |
| GET    | `/banco/{id}`   | Um livro (404 se não existir)     |
| POST   | `/banco`        | Cria livro (201, ou 422 se inválido) |
| DELETE | `/banco/{id}`   | Remove livro (404 se não existir) |

A interface web só lista (READ). CREATE e DELETE são feitos via cURL.

## Exemplos de cURL

```bash
curl -c cookies.txt -d "login=admin&senha=admin123" http://localhost:8000/portal/login
curl -b cookies.txt -d "titulo=Dom Casmurro&autor=Machado de Assis&ano=1899" http://localhost:8000/banco
curl -b cookies.txt -H "Content-Type: application/json" \
     -d '{"titulo":"O Cortiço","autor":"Aluísio Azevedo","ano":1890}' http://localhost:8000/banco
curl -b cookies.txt http://localhost:8000/banco
curl -b cookies.txt http://localhost:8000/banco/1
curl -b cookies.txt -X DELETE http://localhost:8000/banco/1
curl -b cookies.txt http://localhost:8000/portal/logout
```

Demonstração completa: `./crud_curl.sh`
