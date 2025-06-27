from flask import Flask, request, render_template_string
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'chave_secreta_ultra_segura')  # Chave por variável de ambiente
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Cookies protegidos
csrf = CSRFProtect(app)  # Ativa proteção global

@app.route("/")
def index():
    return render_template_string('''
        <form action="/transfer" method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
            <label>Valor: <input type="text" name="amount"></label>
            <label>Conta Destino: <input type="text" name="toAccount"></label>
            <button type="submit">Transferir</button>
        </form>
    ''')

@app.route("/transfer", methods=["POST"])  # Aceita apenas POST
def transfer():
    amount = request.form.get("amount")
    to_account = request.form.get("toAccount")
    return f"Transferência segura de {amount} para {to_account}!"

if __name__ == "__main__":
    app.run(debug=True)  # Debug desativado em produção
