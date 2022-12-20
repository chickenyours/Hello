import socket
from computerManager import *


if __name__ == "__main__":
    a = ComputerManager()
    ip = socket.gethostname()
    port = 12348
    a.SetTCPService((ip,port))
    a.TCPLaunchConnect()
