from flask import Flask, render_template, request, redirect, url_for, session
from config import IDIOMAS, SECRET_KEY
from game_logic import obtener_palabra_aleatoria, ocultar_palabra

from translations import texts


def create_app():
    app = Flask(__name__, template_folder="../templates")
    app.secret_key = SECRET_KEY

    @app.route("/", methods=["GET", "POST"])
    def index():
        idioma = session.get('idioma', 'es')  # Usamos 'es' como idioma por defecto

        if request.method == "POST":
            idioma = request.form.get("idioma")
            if idioma in IDIOMAS:
                session['idioma'] = idioma
                return redirect(url_for('categorias'))

        return render_template("index.html", idiomas=IDIOMAS, texts=texts.get(idioma, texts["es"]))



    @app.route("/categorias", methods=["GET", "POST"])
    def categorias():
        idioma = session.get('idioma', 'es')
        if not idioma:
            return redirect(url_for('index'))

        if request.method == "POST":
            categoria = request.form.get("categoria")
            if categoria:
                session['categoria'] = categoria
                return redirect(url_for('jugar'))

        return render_template("categorias.html", texts=texts.get(idioma, texts["es"]))


    @app.route("/jugar", methods=["GET", "POST"])
    def jugar():
        idioma = session.get('idioma', 'es')
        categoria = session.get('categoria')

        if not idioma or not categoria:
            return redirect(url_for('index'))

        if 'palabra' not in session:
            palabra = obtener_palabra_aleatoria(idioma, categoria)
            session['palabra'] = palabra
            session['oculta'] = "_ " * len(palabra)
            session['usadas'] = []
            session['intentos'] = 0
        else:
            palabra = session['palabra']
            session['oculta'] = session.get('oculta', "_ " * len(palabra))
            session['usadas'] = session.get('usadas', [])
            session['intentos'] = session.get('intentos', 0)

        if request.method == "POST":
            letra = request.form.get("letra")
            if letra and letra not in session['usadas']:
                session['usadas'].append(letra)

                nueva_oculta = ""
                for p, o in zip(palabra, session['oculta'].replace(" ", "")):
                    if p == letra or o != "_":
                        nueva_oculta += p + " "
                    else:
                        nueva_oculta += "_ "

                if letra not in palabra:
                    session['intentos'] += 1

                session['oculta'] = nueva_oculta.strip()

        letras = list("abcdefghijklmnopqrstuvwxyz")

        # Aquí agregas esta parte:
        # Verificar si ganó
        if "_" not in session['oculta']:
            return render_template("ganaste.html", palabra=session['palabra'], texts=texts.get(idioma, texts["es"]))


        # Verificar si perdió
        if session['intentos'] >= 6:
            return render_template("perdiste.html", palabra=session['palabra'], texts=texts.get(idioma, texts["es"]))


        return render_template("jugar.html",
                       palabra_oculta=session['oculta'],
                       letras=letras,
                       usadas=session['usadas'],
                       intentos=session['intentos'],
                       texts=texts.get(idioma, texts["es"]))

    
    @app.route("/reiniciar")
    def reiniciar():
        session.pop('palabra', None)
        session.pop('oculta', None)
        session.pop('usadas', None)
        session.pop('intentos', None)
        session.pop('categoria', None)
        # Opcional: también idioma, si quieres que lo elija de nuevo
        # session.pop('idioma', None)
        return redirect(url_for('index'))  # <--- esto debe estar dentro de la función


    

    return app  # Muy importante que esté al final


