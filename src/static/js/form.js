function mascaraCpf(i) {
	var v = i.value;

	if (isNaN(v[v.length - 1])) { // impede entrar outro caractere que não seja número
		i.value = v.substring(0, v.length - 1);
		return;
	}

	i.setAttribute("maxlength", "14");
	if (v.length == 3 || v.length == 7) i.value += ".";
	if (v.length == 11) i.value += "-";
}

function mascaraTelefone(telefone) {
	let valor = telefone.value;
	
	valor = valor.replace(/\D/g, "")
    valor = valor.replace(/^(\d{2})(\d)/g, "($1) $2")
    valor = valor.replace(/(\d)(\d{4})$/, "$1-$2")
    telefone.value = valor // Insere o(s) valor(es) no campo
}

window.onload = () => { };