from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange, Optional

class MetaForm(FlaskForm):
    nome = StringField('Nome da Meta', validators=[DataRequired()])
    valor_total = FloatField('Valor Total', validators=[DataRequired(), NumberRange(min=0.01)])
    valor_atual = FloatField('Valor Atual', validators=[NumberRange(min=0.0, message="O valor atual não pode ser negativo")])
    prioridade = IntegerField('Prioridade (1-5)', validators=[NumberRange(min=1, max=5, message="A prioridade deve estar entre 1 e 5")])
    submit = SubmitField('Salvar')

class ContaPagarForm(FlaskForm):
    descricao = StringField('Descrição', validators=[DataRequired()])
    valor = FloatField('Valor', validators=[DataRequired(), NumberRange(min=0.01)])
    data_vencimento = DateField('Data de Vencimento', validators=[DataRequired()])
    pago = BooleanField('Pago', default=False, validators=[Optional()])
    submit = SubmitField('Salvar')
