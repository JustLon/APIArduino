import os
import json
import time
import math
from pprint import pprint

os.system('pip install --upgrade flask')


from flask import Flask, request, jsonify


app = Flask(__name__)



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
    #Ejemplo = /Alarmas/agregar/?fecha=20-2-2002&hora=12:00&tipo=1
    #{
        #"hora": 12,
        #"minutos": 0,
        #"ampm": "PM",
        #"fecha": "02/10/2023",
        #"tipo": 2,
        #"creacionEpoch": 100000
    #}
    hora = None
    minutos = None
    ampm = None
    fecha= None
    tipo= None
    creacionEpoch = None

    #Metodo para crear Json
    if 'hora' in query:
        hora = query['hora']
    else:
        hora = None

    if 'minutos' in query:
        minutos = query['minutos']
    else:
        minutos = None

    if 'ampm' in query:
        ampm = query['ampm']
    else:
        ampm = None

    if 'fecha' in query:
        fecha = query['fecha']
    else:
        fecha = None

    if 'tipo' in query:
        tipo = query['tipo']
    else:
        tipo = None

    if((hora or minutos or ampm or fecha or tipo) == None):
        print('No hay algun valor')
    else:
        valores ={
            "hora": hora,
            "minutos": minutos,
            "ampm": ampm,
            "fecha": fecha,
            "tipo": tipo,
            "creacionEpoch": str(math.floor( time.time() *1000000))
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