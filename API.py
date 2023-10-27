import os
import json
import time
import math
from pprint import pprint

os.system('pip install --upgrade flask')


from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/Alarmas/listar")
def listar_todas():
    with open("alarmas.json", "r") as f:
        datos = json.load(f)

        return jsonify(datos)

@app.route("/Alarmas/listen/<epoch>")
def get_alarma(epoch):
    with open("alarmas.json", "r") as f:
        datos = json.load(f)
        pprint(datos)

    for registro in datos:
        if registro['creacionEpoch'] == str(epoch):  # Convierte epoch a entero ya que viene como cadena desde la URL
            Respuesta = registro
            break  # Puedes salir del bucle una vez que encuentres el registro
        else:
            Respuesta={
                "Data": "Registro No encontrado"
            }

    return jsonify(Respuesta), 200


@app.route("/Alarmas/agregar/")
def set_alarma():
    query = request.args.to_dict(flat=False)

    # Extraer los primeros elementos de las listas o asignar None si no existen
    hora = query.get('hora', [None])[0]
    minutos = query.get('minutos', [None])[0]
    ampm = query.get('ampm', [None])[0]
    fecha = query.get('fecha', [None])[0]
    tipo = query.get('tipo', [None])[0]

    if None in (hora, minutos, ampm, fecha, tipo):
        print('No hay algún valor')
        return "Error"
    else:
        valores = {
            "hora": hora,
            "minutos": minutos,
            "ampm": ampm,
            "fecha": fecha,
            "tipo": tipo,
            "creacionEpoch": str(math.floor(time.time() * 1000000))
        }

        archivo_json = "alarmas.json"

        # Si el archivo JSON no existe o está vacío, crea una lista con los nuevos datos
        if not os.path.exists(archivo_json) or os.path.getsize(archivo_json) == 0:
            datos = [valores]
        else:
            # Si el archivo JSON tiene datos, cárgalos y agrega los nuevos datos
            with open(archivo_json, "r") as f:
                datos = json.load(f)
            datos.append(valores)

        # Escribe los datos actualizados de vuelta al archivo JSON
        with open(archivo_json, "w") as f:
            json.dump(datos, f)

    print(query)
    return f'done{query}'


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")