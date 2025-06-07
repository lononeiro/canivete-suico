import random
import string
import os
import json
from flask import Blueprint, render_template, redirect, request, url_for

encurtadorRoute = Blueprint('encurtador', __name__)
urls_encurtadas = {}

# Carrega URLs existentes do arquivo JSON, se existir
if os.path.exists("urls.json"):
    with open("urls.json", "r") as f:
        urls_encurtadas = json.load(f)

def gerar_url_curta(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@encurtadorRoute.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url_longa = request.form.get('url_longa')
        if not url_longa:
            return render_template("encurtador.html", erro="URL inválida")

        # Gera URL curta única
        url_curta = gerar_url_curta()
        while url_curta in urls_encurtadas:
            url_curta = gerar_url_curta()

        urls_encurtadas[url_curta] = url_longa

        # Salva no arquivo JSON
        with open("urls.json", "w") as f:
            json.dump(urls_encurtadas, f)

        # Gera a URL encurtada
        url_encurtada = request.url_root.strip('/') + url_for('encurtador.redirecionar_url', url_curta=url_curta)

        return render_template("encurtador.html", url_encurtada=url_encurtada)

    return render_template("encurtador.html")

@encurtadorRoute.route("/<url_curta>")
def redirecionar_url(url_curta):
    url_longa = urls_encurtadas.get(url_curta)
    if url_longa:
        return redirect(url_longa)
    else:
        return "URL não encontrada", 404