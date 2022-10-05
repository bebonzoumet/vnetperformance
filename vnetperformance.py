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

    def cria_socket(self, addr, port):
        """
        Virtualização do socket com endereço e porta passados como parâmetro
        """
        socket_novo = socket(AF_INET,SOCK_DGRAM)
        socket_novo.bind((addr,port))
        return socket_novo

    def close_socket(self, socket):
        """
        Fecha o socket passado como parâmetro
        """
        socket.close()

    def send(self, socket, msg, dest):
        """
        Virtualização da chamada de comunicação send
        """
        prob = random.uniform(0,self.config["loss_prob"]*2)
        if prob>=self.config["loss_prob"]:
            time.sleep(random.uniform(0,self.config["delay"]*2))
            with open("vnetperformance.log","a+") as f:
                f.write(str(time.strftime("%d/%m/%Y - %H:%M:%S"))+", "+self.host_id+", send, "+str(sys.getsizeof(msg))+" bytes"+"\n")
            socket.sendto(msg.encode(),dest)
        else:
            print("pacote não enviado")

    def recv(self, socket):
        """
        Virtualização da chamada de comunicação receive
        """
        received = socket.recvfrom(self.bytes_size)
        msg = received[0]
        with open("vnetperformance.log","a+") as f:
            f.write(str(time.strftime("%d/%m/%Y - %H:%M:%S"))+", "+self.host_id+", receive, "+str(sys.getsizeof(msg.decode()))+" bytes"+"\n")
        return msg.decode()

