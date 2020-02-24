import socket
import numpy as np
import cv2 as cv


### Constants
PEER_ID = 1
UDP_SERVER_PORT = 9000
TCP_SERVER_PORT = 0     #fixed for all peers
UDP_BroadCast_PORT = 2000 #fixed for all peers


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)


# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.bind(("", UDP_SERVER_PORT))
message = "done".encode('utf-8')


Buffer_size = 512
width = 640
height = 480
cap = cv.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
code = 'start'
code = ('start' + (Buffer_size - len(code)) * 'a').encode('utf-8')


if __name__ == '__main__':
 
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            server.sendto(code, ('<broadcast>', UDP_BroadCast_PORT))
            data = frame.tostring()
            for i in range(0, len(data), Buffer_size):
                server.sendto(data[i:i+Buffer_size],  ('<broadcast>', UDP_BroadCast_PORT))
          
        else:
            break
  
