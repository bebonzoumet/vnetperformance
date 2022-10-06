from vnetperformance import VnetPerformance
import json
import argparse
import time

with open("conf.json","r") as f:
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
    with open("exe02.res", "a+") as f:
        f.write(f"SIZE -> "+str(config["size"])+", DELAY -> "+str(config["delay"])+", LOSS_PROB -> "+str(config["loss_prob"])+f", LARGURA DE BANDA(Mbps) -> {largura_de_banda/8000000}\n")
    servidor.close_socket(serv_socket)

elif args.metodo_chamado == "cliente":
    cliente = VnetPerformance(config["id_cliente"])
    client_socket = cliente.cria_socket(config["client_addr"], config["client_port"])
    for i in range(20):
        cliente.send(client_socket, cliente.create_dataset(), (config["server_addr"], config["server_port"]))
    cliente.end_connection(client_socket, (config["server_addr"], config["server_port"]))
    cliente.close_socket(client_socket)

