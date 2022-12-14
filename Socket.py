#! /usr/bin/env python3

##
# @file nodo.py
# @brief Implementación de las clases  para los servidores
# @author AbrahamRH, Fernanda
# @version 1
# @date 2022-11-16

import socket
import socketserver
import errno

class Socket: 
    def __init__(self, sock = None):
        self.log = [] #Lista con la información del socket
        self.conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.addr = ""
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def sockConnect(self, host, port):
        self.host = host
        self.port = port
        self.sock.connect((host,port))
        self.log.append("conexión en: " + str(host) + " " + str(port))

    def sockBind(self, host, port):
        self.sock.bind((host,port))
        self.sock.listen()
        self.log.append("Socket en escucha en el puerto: " + str(port))
        self.log.append("Socket en escucha con el host: " + host)

    def sockAccept(self):
        tup = tuple()
        tup = self.sock.accept()
        self.conn = tup[0]
        self.addr = tup[1]
        self.log.append("Socket aceptando peticiones en: " + repr(tup))

    def sockSend(self,msg, toClient = None):
        try:
            if toClient is None:
                self.sock.sendall(bytes(msg,'utf-8'))
            else:
                toClient.sendall(bytes(msg,'utf-8'))
            self.log.append("Realizando envio de  mensaje: " + str(msg))
        except BrokenPipeError as e:
            print(e)
            print("No se ha podido enviar mensaje: \"" + str(msg) + "\"" + "\n")

    def sockRecv(self, client = False):
        try:
            if client:
                datos = self.sock.recv(1024)
            else:
                datos = self.conn.recv(1024)
            if not datos: return
            self.log.append("Socket recibiendo datos: " + (datos.decode("utf-8")))
            return datos.decode("utf-8")
        except OSError as e:
            print(e)
            print("No se ha podido recibir mensaje.\n")

    def sockClose(self):
        self.log.append("Cerrando socket.")
        self.conn.close()

    def getNewSocket(self):
        return (self.conn,self.addr)

    def getInfo(self):
        return self.log
    
