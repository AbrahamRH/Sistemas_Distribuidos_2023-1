from Socket import Socket
import random

class Maestro:
    def __init__(self, host, port):
        self.chunkIndex = 0
        self.con = Socket()
        self.namespace = {}  # [ind] = (handler, ubicación)
        self.con.sockBind(host, port)
        self.con.sockAccept()

    def listenRequests(self):
        return self.con.sockRecv()

    def addFile(self, file):
        self.namespace[self.chunkIndex] = (random.randint(1,1000000),"/ruta/" + file)
        self.chunkIndex = self.chunkIndex + 1

    def getChunkInfo(self, index):
        return self.namespace[index]

    def processData(self, data):
        name, index = data.split(",")
        chunk = self.getChunkInfo(int(index))
        if name in chunk[1].split("/"):
            return chunk


if __name__ == "__main__":
    servidor = Maestro("", 65000)
    servidor.addFile("pedidos.txt")
    while True:
        d = servidor.listenRequests()
        if d is not None:
            newData = servidor.processData(d)
        else:
            break

    servidor.con.printSockInfo()



