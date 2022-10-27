from vnetperformance import VnetPerformance
import json
import argparse
import time

with open("vnetperformance.json","r") as f:
    config = json.load(f)

"""
Fazendo o parsing dos argumentos de chamada dos script
"""
parser = argparse.ArgumentParser()

parser.add_argument("metodo_chamado", type=str)

args = parser.parse_args()


if args.metodo_chamado!="servidor" and args.metodo_chamado!="cliente":
    print("O método passado não é correspondente, ou não foi chamado nenhum método")

elif args.metodo_chamado == "servidor":
    servidor = VnetPerformance(config["id_servidor"])
    servidor.cria_socket()
    print("Servido pronto para receber!")
    tempo_total=0
    cont=0
    tempo_inicial = time.time()
    while True:
        if servidor.recv() == "end":
            break
        else:
            tempo_final = time.time()
            tempo_total+=tempo_final-tempo_inicial
            tempo_inicial = tempo_final
            cont+=1
    largura_de_banda = cont*config["size"]/tempo_total
    print(f"A largura de banda é de {largura_de_banda} Bps")
    servidor.close_socket()

elif args.metodo_chamado == "cliente":
    cliente = VnetPerformance(config["id_cliente"])
    cliente.cria_socket()
    for i in range(100):
        cliente.send(cliente.create_dataset(), (config["server_addr"], config["server_port"]))
    cliente.send("end", (config["server_addr"], config["server_port"]))
    cliente.close_socket()

