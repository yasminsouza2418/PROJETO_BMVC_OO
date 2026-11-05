# Singleton da conexão: uma única conexão para todo o processo
import sqlite3

from system.seguranca import hash_senha


class db_connection:
    _conexao = None

    @classmethod
    def get(cls, config):
        if cls._conexao is None:
            cls._conexao = sqlite3.connect(config['banco'])
            cls._conexao.row_factory = sqlite3.Row  # linhas viram dict nos models
            cls._instalar(cls._conexao)
        return cls._conexao

    # Cria as tabelas e o usuário admin na primeira execução
    @staticmethod
    def _instalar(db):
        db.execute('''CREATE TABLE IF NOT EXISTS user_account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR(100) NOT NULL UNIQUE,
            senha VARCHAR(255) NOT NULL)''')
        db.execute('''CREATE TABLE IF NOT EXISTS livro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo VARCHAR(255) NOT NULL,
            autor VARCHAR(255) NOT NULL,
            ano INTEGER NULL)''')
        if not db.execute('SELECT COUNT(*) FROM user_account').fetchone()[0]:
            db.execute('INSERT INTO user_account (login, senha) VALUES (?, ?)',
                       ('admin', hash_senha('admin123')))
        db.commit()
