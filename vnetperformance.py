import json
from socket import *
import time
import sys
import random

class VnetPerformance:

    def __init__(self, host_id):
        """
        Método construtor da classe VnetPerformance
        """
        self.host_id = host_id
        with open("vnetperformance.json","r") as f:
            self.config = json.load(f)
        self.bytes_size = self.config["size"]
        if self.host_id == "Servidor":
            self.addr = self.config["server_addr"]
            self.port = self.config["server_port"]
        elif self.host_id == "Cliente":
            self.addr = self.config["client_addr"]
            self.port = self.config["client_port"]

    def create_dataset(self):
        """
        Cria um dataset de tamanho size
        """
        data=""
        data_encoded = data.encode()
        if self.bytes_size<33:
            pass
        elif sys.getsizeof(data_encoded) == self.bytes_size:
            pass
        else:
            adicional = self.bytes_size - sys.getsizeof(data_encoded)
            data = "a"*adicional
        return data

    def cria_socket(self):
        """
        Virtualização do socket com endereço e porta passados como parâmetro
        """
        self.socket = socket(AF_INET,SOCK_DGRAM)
        self.socket.bind((self.addr,self.port))

    def close_socket(self):
        """
        Fecha o socket passado como parâmetro
        """
        self.socket.close()

    def send(self, msg, dest):
        """
        Virtualização da chamada de comunicação send
        """
        prob = random.uniform(0,self.config["loss_prob"]*2)
        if prob>=self.config["loss_prob"]:
            time.sleep(random.uniform(0,self.config["delay"]*2))
            with open("vnetperformance.log","a+") as f:
                f.write(str(time.strftime("%d/%m/%Y - %H:%M:%S"))+", "+self.host_id+", send, "+str(sys.getsizeof(msg))+" bytes"+"\n")
            self.socket.sendto(msg.encode(),dest)
        else:
            print("pacote não enviado")

    def recv(self):
        """
        Virtualização da chamada de comunicação receive
        """
        received = self.socket.recvfrom(self.bytes_size)
        msg = received[0]
        with open("vnetperformance.log","a+") as f:
            f.write(str(time.strftime("%d/%m/%Y - %H:%M:%S"))+", "+self.host_id+", receive, "+str(sys.getsizeof(msg.decode()))+" bytes"+"\n")
        return msg.decode()

