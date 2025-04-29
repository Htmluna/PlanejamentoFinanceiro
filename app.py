from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import MetaForm, ContaPagarForm
from models import db, Meta, ContaPagar
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_super_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    metas = Meta.query.order_by(Meta.prioridade).all()
    return render_template('index.html', metas=metas)

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar():
    form = MetaForm()
    if form.validate_on_submit():
        nova_meta = Meta(
            nome=form.nome.data,
            valor_total=form.valor_total.data,
            valor_atual=form.valor_atual.data or 0.0,
            prioridade=form.prioridade.data
        )
        db.session.add(nova_meta)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('adicionar.html', form=form)

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    meta = Meta.query.get_or_404(id)
    form = MetaForm(obj=meta)
    if form.validate_on_submit():
        meta.nome = form.nome.data
        meta.valor_total = form.valor_total.data
        meta.valor_atual = form.valor_atual.data
        meta.prioridade = form.prioridade.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editar.html', form=form, meta=meta)

@app.route('/excluir/<int:id>')
def excluir(id):
    meta = Meta.query.get_or_404(id)
    db.session.delete(meta)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/contas', methods=['GET'])
def listar_contas():
    contas = ContaPagar.query.order_by(ContaPagar.data_vencimento).all()
    return render_template('contas/listar.html', contas=contas)

@app.route('/contas/adicionar', methods=['GET', 'POST'])
def adicionar_conta():
    form = ContaPagarForm()
    if form.validate_on_submit():
        nova_conta = ContaPagar(
            descricao=form.descricao.data,
            valor=form.valor.data,
            data_vencimento=form.data_vencimento.data,
            pago=form.pago.data
        )
        db.session.add(nova_conta)
        db.session.commit()
        return redirect(url_for('listar_contas'))
    return render_template('contas/adicionar.html', form=form)

@app.route('/contas/editar/<int:id>', methods=['GET', 'POST'])
def editar_conta(id):
    conta = ContaPagar.query.get_or_404(id)
    form = ContaPagarForm(obj=conta)
    if form.validate_on_submit():
        conta.descricao = form.descricao.data
        conta.valor = form.valor.data
        conta.data_vencimento = form.data_vencimento.data
        conta.pago = form.pago.data
        db.session.commit()
        return redirect(url_for('listar_contas'))
    return render_template('contas/editar.html', form=form, conta=conta)

@app.route('/contas/marcar_pago/<int:id>', methods=['POST'])
def marcar_pago(id):
    conta = ContaPagar.query.get_or_404(id)
    conta.pago = True
    db.session.commit()
    return redirect(url_for('listar_contas'))

@app.route('/contas/excluir/<int:id>')
def excluir_conta(id):
    conta = ContaPagar.query.get_or_404(id)
    db.session.delete(conta)
    db.session.commit()
    return redirect(url_for('listar_contas'))

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Usando a porta 5001
