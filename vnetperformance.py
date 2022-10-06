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

    def close_socket(self, socket):
        """
        Fecha o socket passado como parâmetro
        """
        socket.close()

    def send(self, socket, msg, dest):
        """
        Virtualização da chamada de comunicação send
        """
        prob = random.uniform(0,1)
        file = open('vnetperformance.json', "w")
        self.config["send_counter"] += 1
        json.dump(self.config, file)
        file.close()
        if prob>=self.config["loss_prob"]:
            time.sleep(random.uniform(0,self.config["delay"]*2))
            with open('vnetperformance.json', "w") as file:
                self.config["bytes_send"]+=sys.getsizeof(msg.encode())
                json.dump(self.config, file)
            with open("vnetperformance.log","a+") as f:
                f.write(str(time.strftime("%d/%m/%Y - %H:%M:%S.%f"))+", "+self.host_id+", "+str(self.config["send_counter"])+" de chamadas send totais, "+str(self.config["bytes_send"])+" bytes enviados totais"+"\n")
            socket.sendto(msg.encode(),dest)
        else:
            with open("vnetperformance.log","a+") as f:
                #f.write(str(time.strftime("%d/%m/%Y - %H:%M:%S.%f"))+", "+self.host_id+", "+str(self.config["send_counter"])+" de chamadas send totais, "+"pacote perdido"+"\n")
                f.write(str(time.time())+", "+self.host_id+", "+str(self.config["send_counter"])+" de chamadas send totais, "+"pacote perdido"+"\n")
            print("pacote não enviado")

    def recv(self, socket):
        """
        Virtualização da chamada de comunicação receive
        """
        received = socket.recvfrom(self.bytes_size)
        msg = received[0]
        file = open('vnetperformance.json', "w")
        self.config["recv_counter"] += 1
        self.config["bytes_recv"] += sys.getsizeof(msg)
        json.dump(self.config, file)
        file.close()
        with open("vnetperformance.log","a+") as f:
            f.write(str(time.strftime("%d/%m/%Y - %H:%M:%S"))+", "+self.host_id+", "+str(self.config["recv_counter"])+" de chamadas receive totais, "+str(self.config["bytes_recv"])+" bytes recebidos totais"+"\n")
        return msg.decode()

    def end_connection(self, socket, dest):
        socket.sendto("end".encode(),dest)
