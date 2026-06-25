import os
from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim
from ckanapi import RemoteCKAN

app = Flask(__name__)

@app.route('/listarunidades', methods=['GET'])
def listar_unidades():
    try:
        rc = RemoteCKAN('https://dados.recife.pe.gov.br:443/', apikey=None)
        result = rc.action.datastore_search(
            resource_id="c901459f-f6c7-44dc-bdd5-dd4081e58e69",
            limit=None,
            q="",
        )
        return jsonify(result['records'])
    except:
        return jsonify({"Erro": "erro"}), 404

@app.route('/pegarcoords', methods=['POST'])
def pegar_coords():
    dados = request.get_json()
    print(dados)
    try:
        return jsonify(dados), 201
    except:
        return jsonify({"erro": "Erro ao pegar coordenadas."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
