from flask import Flask, request, render_template_string

app = Flask(__name__)

# Página inicial com formulário vulnerável
@app.route("/")
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Transferência Bancária</title>
            <link rel="stylesheet" href="/static/styles.css">
        </head>
        <body>
            <div class="container">
                <h1>Transferência Bancária</h1>
                <form action="/transfer" method="POST">
                    <label for="amount">Valor:</label>
                    <input type="text" name="amount" id="amount" placeholder="Digite o valor">
                    <label for="toAccount">Conta de Destino:</label>
                    <input type="text" name="toAccount" id="toAccount" placeholder="Digite a conta de destino">
                    <button type="submit">Transferir</button>
                </form>
            </div>
        </body>
        </html>
    ''')

# Endpoint de transferência (aceita POST e GET)
@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if request.method == "POST":
        amount = request.form.get("amount")
        to_account = request.form.get("toAccount")
    elif request.method == "GET":
        amount = request.args.get("amount")
        to_account = request.args.get("toAccount")

    return f"Transferência de {amount} para a conta {to_account} realizada!"

if __name__ == "__main__":
    app.run(debug=True)
