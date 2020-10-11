import socket
import time
import cv2 
import numpy as np
import pickle


udp_ip="127.0.0.2"
# udp_ip="192.168.43.77"
udp_port=5000
max_length=65000


sock = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP
sock.bind((udp_ip, udp_port))

frame=None
buffer=None
print("Menunggu Pesan Masuk")
print("IP : {} : Port : {}".format(udp_ip,udp_port))

while True:  
    data, address = sock.recvfrom(max_length)
    if len(data) < 100:
        frame_info = pickle.loads(data)
        print(
            frame_info["Roll"],
            frame_info["Pitch"],
            frame_info["Yaw"],
            frame_info["Altitude"], end='\r'
            )

        if frame_info:
            jumlah_paket = frame_info["paket"]
            for i in range(jumlah_paket):
                data, addr = sock.recvfrom(max_length) # buffer size
                # p=time.time()
                if i==0:
                    buffer=data
                else :
                    buffer+=data
                frame = np.frombuffer(buffer, dtype=np.uint8)
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                # print(time.time()-p)
            if frame is not None and type(frame) == np.ndarray :
                cv2.imshow("Stream", frame)
                if cv2.waitKey(1) == 27:
                        break
            else:
                print("PACKET LOST")
                 
cv2.destroyAllWindows() 
