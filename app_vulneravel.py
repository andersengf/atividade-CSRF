from flask import Flask, request, render_template_string, session

app = Flask(__name__)
# Chave secreta para gerenciar sessões (login do usuário)
app.secret_key = 'uma-chave-secreta-qualquer'

# --- MODIFICAÇÃO PARA O LABORATÓRIO ---
# Navegadores modernos têm uma política de cookies 'SameSite' que por padrão
# previne ataques CSRF como este. Para que a vulnerabilidade possa ser
# demonstrada, precisamos explicitamente definir a política como 'Lax',
# que é menos restritiva e permite que o cookie seja enviado neste cenário.
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Simula um "banco de dados" de usuários
# Na vida real, isso estaria em um banco de dados seguro.
usuarios = {
    "joao": {"email": "joao@exemplo.com"}
}

# Template HTML para a página principal
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Meu Perfil</title>
    <style>
        body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center; }
        h1 { color: #333; }
        p { font-size: 1.1em; }
        input { width: 250px; padding: 8px; margin-top: 10px; border-radius: 5px; border: 1px solid #ccc; }
        button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin-top: 15px; }
        button:hover { background-color: #0056b3; }
        .message { margin-top: 20px; font-weight: bold; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Olá, {{ session['usuario'] }}!</h1>
        <p>Seu e-mail atual é: <strong>{{ email }}</strong></p>

        <form action="/atualizar-email" method="POST">
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
def home():
    # Simula que o usuário "joao" já fez login
    session['usuario'] = 'joao'

    email_atual = usuarios[session['usuario']]['email']
    return render_template_string(HTML_TEMPLATE, email=email_atual)

@app.route("/atualizar-email", methods=["POST"])
def atualizar_email():
    # **A VULNERABILIDADE ESTÁ AQUI**
    # O servidor não verifica DE ONDE veio esta solicitação.
    # Ele apenas confia que foi o usuário legítimo que a enviou.
    if 'usuario' in session:
        novo_email = request.form.get("email")
        usuario_logado = session['usuario']
        usuarios[usuario_logado]['email'] = novo_email

        mensagem_sucesso = f"E-mail atualizado para {novo_email} com sucesso!"
        email_atualizado = usuarios[usuario_logado]['email']

        return render_template_string(HTML_TEMPLATE, email=email_atualizado, mensagem=mensagem_sucesso)

    return "Você precisa estar logado!", 401

if __name__ == "__main__":
    # Roda o servidor em modo de desenvolvimento
    app.run(debug=True, port=5001)