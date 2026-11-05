# Hash de senha (equivalente a password_hash / password_verify)
import hashlib
import hmac
import os

ITERACOES = 200_000


def hash_senha(senha):
    sal = os.urandom(16)
    h = hashlib.pbkdf2_hmac('sha256', senha.encode(), sal, ITERACOES)
    return f'pbkdf2_sha256${ITERACOES}${sal.hex()}${h.hex()}'


def verificar_senha(senha, guardado):
    try:
        _, it, sal, h = guardado.split('$')
        calc = hashlib.pbkdf2_hmac('sha256', senha.encode(), bytes.fromhex(sal), int(it))
    except ValueError:
        return False
    return hmac.compare_digest(calc.hex(), h)
