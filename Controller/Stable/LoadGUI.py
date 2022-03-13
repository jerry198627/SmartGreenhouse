from PyQt5 import QtWidgets, uic, QtCore
import sys
import socket
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import datetime as dt
import numpy as np
import threading
from time import sleep
import pickle

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
connected = True
SERVER = "192.168.1.15"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

Moisture_Status = [0, 0, 0, 0]

Moisture_Status1 = 1
Moisture_Status2 = 2
Moisture_Status3 = 3
Moisture_Status4 =4
RoomTemp_Status = 5
LightOnOff_Status = 6
Humidity_Status = 7
LightLux_Status = 8

Update_List = [Moisture_Status1,
                Moisture_Status2,
                Moisture_Status3,
                Moisture_Status4, 
                RoomTemp_Status, 
                LightOnOff_Status, 
                Humidity_Status, 
                LightLux_Status]

'''
Update_dict = {'Moisture_Status0': [],
                'Moisture_Status1': [],
                'Moisture_Status2': [],
                'Moisture_Status3': [],
                'RoomTemp_Status': [],
                'Humidity_Status': [],
                'LightOnOff_Status':[],
                'LightLux_Status':[]}
'''
#Send msg to Server
def send(msg):
    #message = pickle.dumps(msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    #recieveMsg = client.recv(2048).decode(FORMAT)
    #print(f"Get: {recieveMsg}")

#Get msg from Server (Output: pickle(msg))
def get_msg():
    global connected
    msg_length = client.recv(HEADER).decode(FORMAT)
    print(f"MasLength: {msg_length}")
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length)
        #print(f"Message Receive: {msg}")
        msg = pickle.loads(msg)
        #print(f"{msg}")
        if str(msg) == DISCONNECT_MESSAGE:
            connected = False 
        return msg
        
    return msg_length

def Update_status():
    global Moisture_Status, window, connected
    window_dict = [window.SoilMoistureStatusLabel0,
                    window.SoilMoistureStatusLabel1,
                    window.SoilMoistureStatusLabel2,
                    window.SoilMoistureStatusLabel3,
                    window.RoomTempStatusLabel,
                    window.HumidityStatusLabel,
                    window.LightStatusLabel,
                    window.LightLuxStatusLabel]

    while connected:
        try:

            send("GetUpdate")
            recieveMsg = get_msg()
            print(f"StatUpdate: {recieveMsg}")
            
            for i ,v in enumerate(recieveMsg):
                #print(str(recieveMsg[v]))
                window_dict[i].setText(str(recieveMsg[v]))
                window_dict[i].setAlignment(QtCore.Qt.AlignCenter)
                sleep(0.1)

            print(f"Get plot")
            recieveMsg = get_msg()
            print(f"PlotData: {recieveMsg})")

            
            

            sleep(2)
        except:
            break





class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GreenUI.ui', self)
        self.show()

        self.SetWaterVolumeLevel = 0
        self.SetTempatureLevel = 0
        self.SetHumidityLevel = 0


        ##connect actions widgets Here
        self.WaterVolumeLabel.setText(str(self.SetWaterVolumeLevel))
        self.TempatureLevelLabel.setText(str(self.SetTempatureLevel))
        self.HumidityLevelLabel.setText(str(self.SetHumidityLevel))
        self.LightOnButton.clicked.connect(self.Event_LightON)
        self.LightOffButton.clicked.connect(self.Event_LightOFF)
        self.AddWaterButton.clicked.connect(self.Event_AddWater)
        self.MinWaterButton.clicked.connect(self.Event_MinWater)
        self.AddTempButton.clicked.connect(self.Event_AddTemp)
        self.MinTempButton.clicked.connect(self.Event_MinTemp)
        self.AddHumiButton.clicked.connect(self.Event_AddHumi)
        self.MInHumiButton.clicked.connect(self.Event_MinHumi)


        ##plot
        self.canvas = FigureCanvas(plt.Figure(figsize=(15,6)))


    ##write event for widgets Here
    def Event_LightON(self):
        send("LightON")

    def Event_LightOFF(self):
        send("LightOFF")

    def Event_AddWater(self):
        self.SetWaterVolumeLevel = self.SetWaterVolumeLevel + 1
        self.WaterVolumeLabel.setText(str(self.SetWaterVolumeLevel))
        send("Water: " + str(self.SetWaterVolumeLevel))

    
    def Event_MinWater(self):
        self.SetWaterVolumeLevel = self.SetWaterVolumeLevel - 1
        self.WaterVolumeLabel.setText(str(self.SetWaterVolumeLevel))
        send("Water: " + str(self.SetWaterVolumeLevel))

    def Event_AddTemp(self):
        self.SetTempatureLevel = self.SetTempatureLevel + 1
        self.TempatureLevelLabel.setText(str(self.SetTempatureLevel))
        send("Temp: " + str(self.SetTempatureLevel))

    def Event_MinTemp(self):
        self.SetTempatureLevel = self.SetTempatureLevel - 1
        self.TempatureLevelLabel.setText(str(self.SetTempatureLevel))
        send("Temp: " + str(self.SetTempatureLevel))

    def Event_AddHumi(self):
        self.SetHumidityLevel = self.SetHumidityLevel + 1
        self.HumidityLevelLabel.setText(str(self.SetHumidityLevel))
        send("Humid: " + str(self.SetHumidityLevel))

    def Event_MinHumi(self):
        self.SetHumidityLevel = self.SetHumidityLevel - 1
        self.HumidityLevelLabel.setText(str(self.SetHumidityLevel))
        send("Humid: " + str(self.SetHumidityLevel))


    def closeEvent(self, event):
        send(DISCONNECT_MESSAGE)



app = QtWidgets.QApplication(sys.argv)
window = Ui()
GetUpdate_Tread = threading.Thread(target = Update_status)
GetUpdate_Tread.start()
app.exec_()