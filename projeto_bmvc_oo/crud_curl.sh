#!/usr/bin/env bash
# Demonstração do CRUD via cURL. Requer o servidor: python3 index.py
URL="${URL:-http://localhost:8000}"
JAR="$(mktemp)"
trap 'rm -f "$JAR"' EXIT

passo() { printf '\n== %s\n' "$1"; }
# -w imprime o status HTTP depois do corpo
req() { curl -s -w '\n[HTTP %{http_code}]\n' "$@"; }

passo "1. Acesso sem login (espera 401)"
req "$URL/banco"

passo "2. Login com senha errada (espera 401)"
req -d "login=admin&senha=errada" "$URL/portal/login"

passo "3. Login (grava cookie em $JAR)"
req -c "$JAR" -d "login=admin&senha=admin123" "$URL/portal/login"

passo "4. CREATE por formulário (espera 201)"
req -b "$JAR" -d "titulo=Dom Casmurro&autor=Machado de Assis&ano=1899" "$URL/banco"

passo "5. CREATE por JSON (espera 201)"
CRIADO=$(req -b "$JAR" -H "Content-Type: application/json" \
  -d '{"titulo":"O Cortiço","autor":"Aluísio Azevedo","ano":1890}' "$URL/banco")
echo "$CRIADO"
ID=$(echo "$CRIADO" | sed -n 's/.*"id": *\([0-9]*\).*/\1/p')

passo "6. CREATE inválido (espera 422)"
req -b "$JAR" -H "Content-Type: application/json" -d '{"titulo":"","ano":"abc"}' "$URL/banco"

passo "7. READ da lista"
req -b "$JAR" "$URL/banco"

passo "8. READ do registro $ID"
req -b "$JAR" "$URL/banco/$ID"

passo "9. READ em HTML (Accept: text/html)"
req -b "$JAR" -H "Accept: text/html" "$URL/banco"

passo "10. DELETE do registro $ID"
req -b "$JAR" -X DELETE "$URL/banco/$ID"

passo "11. READ do registro removido (espera 404)"
req -b "$JAR" "$URL/banco/$ID"

passo "11b. Rota inexistente (espera 404) e método não permitido (espera 405)"
req -b "$JAR" "$URL/nada"
req -b "$JAR" -X PUT "$URL/banco"

passo "12. Logout"
req -b "$JAR" "$URL/portal/logout"

passo "13. Acesso após logout (espera 401)"
req -b "$JAR" "$URL/banco"
