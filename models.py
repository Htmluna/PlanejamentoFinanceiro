from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    valor_atual = db.Column(db.Float, default=0.0)
    prioridade = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Meta {self.nome}>'

    def progresso(self):
        if self.valor_total == 0:
            return 0
        return (self.valor_atual / self.valor_total) * 100

class ContaPagar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    pago = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ContaPagar {self.descricao}>'
