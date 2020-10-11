import cv2
import socket
import time
from math import ceil
import pickle
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

vehicle = connect('udp:127.0.0.1:14550',wait_ready=True)
def rescale_frame(frame, percent=10):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_CUBIC)

max_length = 65000
# host = "192.168.43.140"
host = "127.0.0.2"
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
ret, frame=cap.read()
while ret:    
    # compress frame
    frameresc = rescale_frame(frame, 100)

    ret, buffer = cv2.imencode('.jpg', frameresc)

    jumlah_paket=1
    if len(buffer)>max_length:
        jumlah_paket=ceil(len(buffer)/max_length)
    pesanstr = {"paket":jumlah_paket,
                "Roll" : vehicle.attitude.roll,
                "Pitch" : vehicle.attitude.pitch,
                "Yaw" : vehicle.attitude.yaw,
                "Altitude" :  vehicle.location.global_relative_frame.alt}
    sock.sendto(pickle.dumps(pesanstr),(host,port))

    if ret:
        #convert bytes to array
        buffer=buffer.tobytes()

        left = 0
        right = max_length
        for i in range(jumlah_paket):
            # memotong  data untuk dikirim
            data = buffer[left:right]
            left = right
            right += len(data)
            
            print(f"paket {i+1}  : {len(data)} ", end='\n\r')
    
            sock.sendto(data, (host, port))
    ret, frame=cap.read()    
        
    

