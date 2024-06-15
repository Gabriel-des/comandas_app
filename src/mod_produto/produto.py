from flask import send_file
from flask import Blueprint, render_template, request, jsonify
import requests
import base64
from mod_login.login import validaToken
from settings import getHeadersAPI, ENDPOINT_PRODUTO
from funcoes import Funcoes

bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

prod_data = []

''' rotas dos formulários '''

@bp_produto.route('/', methods=['GET', 'POST'])
@validaToken
def formListaProduto():
	try:
		response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
		result = response.json()
		
		if (response.status_code != 200):
			raise Exception(result)

		prod_data.append(result[0])
		return render_template('formListaProduto.html', result=result[0])

	except Exception as e:
		return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/novo-produto', methods=['GET', 'POST'])
@validaToken
def formProduto():
	return render_template('formProduto.html'), 200

@bp_produto.route("/form-edit-produto", methods=['POST','GET'])
@validaToken
def formEditProduto():
    try:
        # ID enviado via FORM
        id_produto = request.form['id']
        
        # Executa o verbo GET da API buscando somente o funcionário selecionado,
        # obtendo o JSON do retorno
        response = requests.get(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        result = response.json()
        
        if (response.status_code != 200):
            raise Exception(result)
        
        # Renderiza o form passando os dados retornados
        return render_template('formProduto.html', result=result[0])
    
    except Exception as e:
        return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/insert', methods=['POST'])
@validaToken
def insert():
    try:
        # Dados enviados via FORM
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = request.form['valor_unitario']
        
        # Converte em base64
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        
        # Monta o JSON para envio a API
        payload = {'id_produto': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario}
        
        # Executa o verbo POST da API e armazena seu retorno
        response = requests.post(ENDPOINT_PRODUTO, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        
        return jsonify(erro=False, msg=result[0])
    
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_produto.route('/edit', methods=['POST'])
@validaToken
def edit():
    try:
        # Dados enviados via FORM
        id_produto = request.form['id']
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor_unitario = request.form['valor_unitario']
        
        # Converte em base64
        foto = "data:" + request.files['foto'].content_type + ";base64," + str(base64.b64encode(request.files['foto'].read()), "utf-8")
        
        # Monta o JSON para envio a API
        payload = {'id_produto': id_produto, 'nome': nome, 'descricao': descricao, 'foto': foto, 'valor_unitario': valor_unitario}
        
        # Executa o verbo PUT da API e armazena seu retorno
        response = requests.put(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI(), json=payload)
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        
        return jsonify(erro=False, msg=result[0])
    
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])

@bp_produto.route('/delete', methods=['POST'])
@validaToken
def delete():
    try:
        # Dados enviados via FORM
        id_produto = request.form['id_produto']
        
        # Executa o verbo DELETE da API e armazena seu retorno
        response = requests.delete(ENDPOINT_PRODUTO + id_produto, headers=getHeadersAPI())
        result = response.json()
        
        if (response.status_code != 200 or result[1] != 200):
            raise Exception(result)
        
        return jsonify(erro=False, msg=result[0])
    
    except Exception as e:
        return jsonify(erro=True, msgErro=e.args[0])
    
@bp_produto.route('/gera-pdf', methods=['GET', 'POST'])
@validaToken
def geraPdf():
	try: 
		pdf_file = Funcoes.generate_pdf_file(prod_data[0], "Produtos")
		
		return send_file(pdf_file, as_attachment=True, download_name='produto.pdf')
	except Exception as e:
		return jsonify(erro=True, msgErro=e.args[0])