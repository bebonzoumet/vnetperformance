from vnetperformance import VnetPerformance
import json
import argparse
import sys
import time

"""
Fazendo o parsing dos argumentos de chamada dos script
"""
parser = argparse.ArgumentParser()

parser.add_argument("metodo_chamado", type=str)
parser.add_argument("--size", type=int)

args = parser.parse_args()


with open("vnetperformance.json","r") as f:
    config = json.load(f)

def create_dataset():
        """
        Cria um dataset de tamanho size
        """
        data=""
        data_encoded = data.encode()
        if config["size"]<33:
            pass
        elif sys.getsizeof(data_encoded) == config["size"]:
            pass
        else:
            adicional = config["size"] - sys.getsizeof(data_encoded)
            data = "a"*adicional
        return data


if args.metodo_chamado!="servidor" and args.metodo_chamado!="cliente":
    print("O método passado não é correspondente, ou não foi chamado nenhum método")

elif args.metodo_chamado == "servidor":
    servidor = VnetPerformance(config["id_servidor"])
    serv_socket = servidor.cria_socket(config["server_addr"], config["server_port"])
    print("Servido pronto para receber!")
    tempo_total=0
    cont=0
    tempo_inicial = time.time()
    while True:
        if servidor.recv(serv_socket) == "end":
            break
        else:
            tempo_final = time.time()
            tempo_total+=tempo_final-tempo_inicial
            tempo_inicial = tempo_final
            cont+=1
    largura_de_banda = cont*config["size"]/tempo_total
    print(f"A largura de banda é de {largura_de_banda} Bps")

elif args.metodo_chamado == "cliente":
    cliente = VnetPerformance(config["id_cliente"])
    client_socket = cliente.cria_socket(config["client_addr"], config["client_port"])
    for i in range(100):
        cliente.send(client_socket, create_dataset(), (config["server_addr"], config["server_port"]))
    cliente.send(client_socket, "end", (config["server_addr"], config["server_port"]))



