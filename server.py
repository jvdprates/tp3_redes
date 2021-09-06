from flask import Flask
from flask_restful import Api, Resource
import json

# Inicialicação da API
app = Flask(__name__)
api = Api(app)

# Função de leitura de arquivo
def ler_json(file_name):
  with open(file_name, 'r', encoding='utf8') as f:
      return json.load(f)

# Recurso que retorna hello world na porta padrão
class HelloWorld(Resource):
  def get(self):
    return {"mensagem": "Hello World"}

# Recurso que retorna o conteúdo do arquivo ix.json
class Ix(Resource):
  def get(self):
    ixjson = ler_json('ix.json')
    return {"data": ixjson}

# Recurso que retorna a lista de ids de um dado presente no arquivo netixlan.json
class IxNets(Resource):
  def get(self, ix_id):
    netjson = ler_json('netixlan.json')['data']
    res = []
    for ix in netjson:
      if ix['ix_id'] == int(ix_id):
        res.append(ix['net_id'])
    return {"data": res}

# Recurso que retorna os nomes das redes de um dado presente em net.json
class NetName(Resource):
  def get(self, net_id):
    netjson = ler_json('net.json')['data']
    res = []
    for ix in netjson:
      if ix['id'] == int(net_id):
        res.append(ix['name'])
    return {"data": res}

# Recurso que retorna todo o conteúdo de net.json
class Nets(Resource):
  def get(self):
    netjson = ler_json('net.json')
    return {"data": netjson}

api.add_resource(HelloWorld, '/')
api.add_resource(Ix, '/api/ix')
api.add_resource(IxNets, '/api/ixnets/<string:ix_id>')
api.add_resource(Nets, '/api/net')
api.add_resource(NetName, '/api/netname/<string:net_id>')

if __name__ == "__main__":
  app.run(debug=True)