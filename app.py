from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Servidor del Proyecto Final esta funcionando correctamente"

if __name__ == "__main__":             # Ya quitamos `debug=True'
    app.run(host="0.0.0.0", port=5000) # Con este cambio habilitamos las
                                       # conexiones externas a nuestro servidor