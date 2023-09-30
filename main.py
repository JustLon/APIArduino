import os
import json
os.system('pip install --upgrade flask')

from flask import Flask, request, jsonify

app = Flask(__name__)

ArchivoJson = open('alarmas.json')

datos = json.load(ArchivoJson)


@app.route("/Alarmas/<epoch>")
def get_user(epoch):
    for registro in datos:
        if registro['epoch'] == int(epoch):  # Convierte epoch a entero ya que viene como cadena desde la URL
            Respuesta = registro
            break  # Puedes salir del bucle una vez que encuentres el registro
        else:
            Respuesta={
                "Data": "Registro No encontrado"
            }

    return jsonify(Respuesta), 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")