import socket, json, argparse as ap

# Constantes do programa
CRLF = '\r\n'
SP = ' '
CR = '\r'
HOST = '127.0.0.1'
PORT = 5000
PATH = '/'

# Configuração de argumentos
parser = ap.ArgumentParser(description='Trabalho pratico 2 - Bruno Oliveira, João Prates, Rafael Costa')
parser.add_argument("host", help="Ip e porta do servidor")
parser.add_argument("opt", help="Opção de análise, \"0\" para IXP por rede e \"1\" para rede por IXP.")

args = parser.parse_args()

# Função de configuração para o header
def header_requisicao(host=HOST, path=PATH):
  # print("Header Requisicao: \n {} - {}".format(host, path))
  return CRLF.join([
      "GET {} HTTP/1.1".format(path), "Host: {}".format(host),
      "Connection: Close\r\n\r\n"
  ])

# Função de parse para headers recebidos
def parse_header(header):
  # print("Quebrando header: \n {}".format(header))
  header_fields = header.split(CR)

  code = header_fields.pop(0).split(' ')[1]
  header = {}
  for field in header_fields:
      key, value = field.split(':', 1)
      header[key.lower()] = value
  return header, code

# Função de envio de requisição para o servidor
def enviar_requisicao(host=HOST, path=PATH, port=PORT):
  sock = socket.socket()
  # Conectar ao servidor.
  sock.connect((host, port))
  # Enviar a requisição.
  sock.send(str.encode(header_requisicao(host, path)))
  # Receber a resposta.
  response = ''
  chuncks = sock.recv(4096)
  while chuncks:
      response += chuncks.decode()
      chuncks = sock.recv(4096)
  # Headers HTTP são separados do corpo por uma linha vazia
  header, _, body = response.partition(CRLF + CRLF)
  header, code = parse_header(header)
  return header, code, body


if __name__ == "__main__":
  # Recebe a configuração dos argumentos
  config = args.host.split(':')
  host_ = config[0]
  port_ = int(config[1])

  # Opção 0: IXP por rede
  if args.opt == "0":
    # Consulta net.json
    header, code, body  = enviar_requisicao(host=host_, port=port_, path=f'/api/net')
    # Isola o corpo da resposta
    body = json.loads(body)['data']['data']

    for net in body:
      # Consulta cada uma das conexões
      header, code, body2  = enviar_requisicao(host=host_, port=port_, path=f'/api/netixs/{net["id"]}')
      body2 = json.loads(body2)['data']
      # Imprime a relação entre o id de cada conexão e o número de elementos de cada uma
      print(f"{net['id']}\t{net['name']}\t{len(body2)}")

  # Opção 1: Rede por IXP
  if args.opt == "1":
    # Consulta ix.json
    header, code, body  = enviar_requisicao(host=host_, port=port_, path=f'/api/ix')
    # Isola o corpo da resposta
    body = json.loads(body)['data']['data']

    for ix in body:
      # Consulta cada um dos ids
      header, code, body2  = enviar_requisicao(host=host_, port=port_, path=f'/api/ixnets/{ix["id"]}')
      body2 = json.loads(body2)['data']
      # Imprime a relação entre cada resposta com o número de elementos de cada uma
      print(f"{ix['id']}\t{ix['name']}\t{len(body2)}")


