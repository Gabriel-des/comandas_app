from flask import Blueprint, jsonify, redirect, render_template, request, send_file, url_for
import requests
from funcoes import Funcoes
from mod_login.login import validaToken
from settings import getHeadersAPI, ENDPOINT_CLIENTE

bp_cliente = Blueprint('cliente', __name__, url_prefix="/cliente", template_folder='templates')
cli_data = []

''' rotas dos formulários '''

@bp_cliente.route('/')
@validaToken
def formListaCliente():
	try:
		response = requests.get(ENDPOINT_CLIENTE, headers=getHeadersAPI())
		result = response.json()
		
		if (response.status_code != 200):
			raise Exception(result)

		cli_data.append(result[0])
		return render_template('formListaCliente.html', result=result[0])

	except Exception as e:
		return render_template('formListaCliente.html', msgErro=e.args[0])

@bp_cliente.route('/novo-cliente')
@validaToken
def formCliente():
	return render_template('formCliente.html'), 200

@bp_cliente.route('/insert', methods=['POST'])
@validaToken
def insert():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']

        # monta o JSON para envio a API
        payload = {'id_cliente': id_cliente, 'nome': nome, 'cpf': cpf, 'telefone': telefone}

        # executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_CLIENTE, headers=getHeadersAPI(), json=payload)
        result = response.json()

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)

        return redirect(url_for('cliente.formListaCliente', msg=result[0]))

    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route("/form-edit-cliente", methods=['POST'])
@validaToken
def formEditCliente():
    try:
        # ID enviado via FORM
        id_cliente = request.form['id']
        
        # executa o verbo GET da API buscando somente o cliente selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json()
        
        if (response.status_code != 200):
            raise Exception(result)
        
        # renderiza o form passando os dados retornados
        return render_template('formCliente.html', result=result[0])
    
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route("/edit", methods=['POST'])
@validaToken
def edit():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        nome = request.form['nome']
        cpf = request.form['cpf']
        telefone = request.form['telefone']
        
        # monta o JSON para envio a API
        payload = {
            'id_cliente': id_cliente,
            'nome': nome,
            'cpf': cpf,
            'telefone': telefone
        }
        
        # executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        return redirect(url_for('cliente.formListaCliente', msg=result[0]))
    
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route("/delete", methods=["POST"])
@validaToken
def delete():
    try:
        # dados enviados via FORM
        id_cliente = request.form['id']
        
        # executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_CLIENTE + id_cliente, headers=getHeadersAPI())
        result = response.json()

        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        
        return jsonify(erro=False, msg=result[0])
    
    except Exception as e:
        return render_template('formListaCliente.html', msgErro=e.args[0])
    
@bp_cliente.route('/gera-pdf', methods=['GET', 'POST'])
@validaToken
def geraPdf():
	try:
		pdf_file = Funcoes.generate_pdf_file(cli_data[0], "Clientes")
		
		return send_file(pdf_file, as_attachment=True, download_name='cliente.pdf')
	except Exception as e:
		return jsonify(erro=True, msgErro=e.args[0])