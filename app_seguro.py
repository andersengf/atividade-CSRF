from flask import Flask, request, render_template_string, session
from flask_wtf.csrf import CSRFProtect # Importe a proteção CSRF

app = Flask(__name__)
app.secret_key = 'uma-chave-secreta-diferente-e-segura'

# 1. INICIE A PROTEÇÃO CSRF
csrf = CSRFProtect(app)

usuarios = {
    "joao": {"email": "joao@exemplo.com"}
}

# 2. ADICIONE O CAMPO CSRF AO TEMPLATE
#    O `{{ csrf_token() }}` cria um campo oculto com um token único.
HTML_TEMPLATE_SEGURO = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Meu Perfil Seguro</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }
        h1 { color: #333; }
        p { font-size: 1.1em; }
        input { width: 250px; padding: 8px; margin-top: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { background-color: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 15px; }
        button:hover { background-color: #218838; }
        .message { margin-top: 20px; font-weight: bold; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Olá, {{ session['usuario'] }}! (Versão Segura)</h1>
        <p>Seu e-mail atual é: <strong>{{ email }}</strong></p>

        <form action="/atualizar-email" method="POST">
            <!-- ESTA É A PROTEÇÃO! -->
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">

            <label for="email">Novo e-mail:</label><br>
            <input type="text" id="email" name="email" placeholder="Digite o novo e-mail">
            <br>
            <button type="submit">Atualizar E-mail</button>
        </form>

        {% if mensagem %}
            <p class="message success">{{ mensagem }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def home_segura():
    session['usuario'] = 'joao'
    email_atual = usuarios[session['usuario']]['email']
    return render_template_string(HTML_TEMPLATE_SEGURO, email=email_atual)

@app.route("/atualizar-email", methods=["POST"])
def atualizar_email_seguro():
    # A biblioteca Flask-WTF agora valida o token AUTOMATICAMENTE.
    # Se o token estiver ausente ou for inválido, a requisição será
    # rejeitada com um erro 400 (Bad Request) antes mesmo de entrar nesta função.
    if 'usuario' in session:
        novo_email = request.form.get("email")
        usuario_logado = session['usuario']
        usuarios[usuario_logado]['email'] = novo_email

        mensagem_sucesso = f"E-mail atualizado para {novo_email} com segurança!"
        email_atualizado = usuarios[usuario_logado]['email']

        return render_template_string(HTML_TEMPLATE_SEGURO, email=email_atualizado, mensagem=mensagem_sucesso)

    return "Você precisa estar logado!", 401

if __name__ == "__main__":
    # Vamos usar a porta 5002 para não conflitar com o outro app
    app.run(debug=True, port=5002)