from flask import Blueprint, render_template
import requests
from mod_login.login import validaLogin
from settings import getHeadersAPI, ENDPOINT_PRODUTO

bp_produto = Blueprint('produto', __name__, url_prefix="/produto", template_folder='templates')

''' rotas dos formulários '''

@bp_produto.route('/')
def formListaProduto():
	try:
		response = requests.get(ENDPOINT_PRODUTO, headers=getHeadersAPI())
		result = response.json()
		
		if (response.status_code != 200):
			raise Exception(result)

		return render_template('formListaProduto.html', result=result[0])

	except Exception as e:
		return render_template('formListaProduto.html', msgErro=e.args[0])

@bp_produto.route('/novo-produto')
def formProduto():
	return render_template('formProduto.html'), 200