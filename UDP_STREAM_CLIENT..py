import socket
import numpy as np
import cv2 as cv




### Constants
PEER_ID = 1
UDP_SERVER_PORT = 9000
TCP_SERVER_PORT = 0     #fixed for all peers
UDP_BroadCast_PORT = 2000 #fixed for all peers



client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", UDP_BroadCast_PORT ))


Buffer_size = 512
width = 640
height = 480
code = b'start'
num_of_chunks = width * height * 3 / Buffer_size

if __name__ == '__main__':
    while True:
        chunks = []
        start = False
        while len(chunks) < num_of_chunks:
            chunk, _ = client.recvfrom(Buffer_size)
            if start:
                chunks.append(chunk)
            elif chunk.startswith(code):
                start = True

        byte_frame = b''.join(chunks)

        frame = np.frombuffer(
            byte_frame, dtype=np.uint8).reshape(height, width, 3)

        cv.imshow('recv', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    client.close()
    cv.destroyAllWindows()
