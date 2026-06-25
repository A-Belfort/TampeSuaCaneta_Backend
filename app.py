import os
from operator import itemgetter
from flask import Flask, request, jsonify
from geopy.geocoders import Nominatim # nominatim é uma API de geocoding
from geopy.distance import geodesic # parte de cálculo de distância do geopy
from ckanapi import RemoteCKAN # necessário devido ao dados recife

app = Flask(__name__)

# sem banco de dados no momento
usuario = {"latitude": None,"longitude": None}

# app pega e salva todos os dados para efetuar consultas no código
rc = RemoteCKAN('https://dados.recife.pe.gov.br:443/', apikey=None)
result = rc.action.datastore_search(
    resource_id="c901459f-f6c7-44dc-bdd5-dd4081e58e69",
    limit=None,
    q="",
)
unidades = result['records']

# cálculo de distância
def distancia_calc(user,lugar):
    lat_x = float(user["latitude"])
    lon_x = float(user["longitude"])
    lat_y = float(lugar["latitude"])
    lon_y = float(lugar["longitude"])
    distancia = geodesic((lat_x,lon_x),(lat_y,lon_y))
    return distancia.km

# gerar uma lista nova, com a distância inclusa
def gerar_lista_proximidade():
    unidades_distancia = []
    for i in unidades:
        # como não tem banco de dados ainda e o programa só dá conta de um único usuário,
        # modifica a lista-mestre
        try:
            x = i.copy()
            x["distancia"] = distancia_calc(usuario,x)
            unidades_distancia.append(x)
        except:
            pass
    unidades_update = sorted(unidades_distancia,key=itemgetter("distancia"))
    return unidades_update

@app.route('/listarunidades', methods=['GET'])
def listar_unidades():
    try:
        resultado = gerar_lista_proximidade()
        return jsonify(resultado), 201
    except Exception as e:
        return jsonify({"Erro": str(e)}), 404

@app.route('/pegarcoords', methods=['POST'])
def pegar_coords():
    dados = request.get_json()
    try:
        usuario["latitude"] = dados["latitude"]
        usuario["longitude"] = dados["longitude"]
        return jsonify(dados), 201
    except:
        return jsonify({"erro": "Erro ao pegar coordenadas."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
