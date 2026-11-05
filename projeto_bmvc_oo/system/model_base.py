# Model genérico: CRUD com consultas parametrizadas
from system.bmvc_base import bmvc_base


class model_base(bmvc_base):
    table = ''
    fields = ()  # campos permitidos em create()

    def all(self):
        return [dict(r) for r in self.db.execute(f'SELECT * FROM {self.table} ORDER BY id')]

    def find(self, id):
        r = self.db.execute(f'SELECT * FROM {self.table} WHERE id = ?', (id,)).fetchone()
        return dict(r) if r else None

    def create(self, dados):
        # Só aceita colunas declaradas em fields (equivale ao array_intersect_key)
        dados = {k: v for k, v in dados.items() if k in self.fields}
        cols = ', '.join(dados)
        marcas = ', '.join('?' * len(dados))
        cur = self.db.execute(f'INSERT INTO {self.table} ({cols}) VALUES ({marcas})', tuple(dados.values()))
        self.db.commit()
        return self.find(cur.lastrowid)

    def delete(self, id):
        cur = self.db.execute(f'DELETE FROM {self.table} WHERE id = ?', (id,))
        self.db.commit()
        return cur.rowcount > 0
