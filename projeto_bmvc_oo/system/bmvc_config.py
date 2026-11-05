# Configuração central do sistema
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class bmvc_config:
    @staticmethod
    def get():
        return {
            'banco': os.path.join(RAIZ, 'banco.sqlite'),
            # Para MySQL: instale o pymysql e, em db_connection.py, troque sqlite3.connect(...) por
            # pymysql.connect(host='localhost', user='root', password='secret', database='bmvc')
            'base_url': '',  # prefixo da URL; vazio = app na raiz
            'porta': 8000,
        }
