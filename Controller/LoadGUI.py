from PyQt5 import QtWidgets, uic, QtCore
import sys
import socket
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import numpy as np
import threading
from time import sleep
import pickle
import pandas as pd

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
connected = True
SERVER = "192.168.1.11"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


plotChoice = ""

cameraInput = np.empty(1)

Save_DateFrame = pd.DataFrame()
print(Save_DateFrame)


Settings_dict = {'Water_Setting1' : 20,
                'Water_Setting2': 20,
                'Light_Setting': 0,
                'Fan_Setting': 0}


#Send msg to Server
def send(msg):
    message = pickle.dumps(msg)
    msg_length = len(message)

    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    client.send(send_length)
    client.send(message)



#Get msg from Server (Output: pickle(msg))
def get_msg():
    global connected
    retry = 1
    msg_length = client.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    msg = b''
    received_length = msg_length

    while True:
        msg += client.recv(received_length)
        received_length = 2048

        if len(msg) == msg_length:
            break

    msg = pickle.loads(msg)
    #print(f"Pickled recieved: {msg}")
    if str(msg) == DISCONNECT_MESSAGE:
        print(f"[Conn] Get DC")
        connected = False 
    
    return msg


def Update_status():
    global window, Save_DateFrame, cameraInput, Settings_dict

    init = 1
    while connected:
        '''
        Update status
            '''
        send("GetUpdate")
        '''
        Get updateDict
            '''
        Update_dict = get_msg()
        print(f"Update_dict : {Update_dict}")
        templist = [Update_dict['Moisture_Status0'] + "%",
                    Update_dict['Moisture_Status1'] + "%",
                    Update_dict['Moisture_Status2'] + "%",
                    Update_dict['Moisture_Status3'] + "%",
                    Update_dict['RoomTemp_Status'] + " ⁰C",
                    Update_dict['Humidity_Status'] + "%",
                    "On" if int(Update_dict['Light_Status']) else "Auto",
                    "On" if int(Update_dict['Fan_Status']) else "Auto",
                    Update_dict['WG1_Set'] + "%",
                    Update_dict['WG2_Set'] + "%"]
        window.statusUpdateEvent(templist)
        '''
        Get plotData
            '''
        print(f"[Conn] Get DataFrame")
        Save_DateFrame = get_msg()
        
        '''
        Get cameraData
            '''
        print(f"[Conn] Get CameraData")
        cameraInput = get_msg()

        print(f"[Conn] UpdateList : {Update_dict}")
        #print(f"PlotData: {Save_DateFrame}")
        #print(f"CameraData: {type(cameraInput)}")
            
        sleep(0.5)


def PlotUpdate():
    sleep(10)
    while connected:
        sleep(0.5)
        global window

        timelist = pd.to_datetime(Save_DateFrame['Datetime'])

        x = np.array(timelist)
        if plotChoice == "humid":
            y = np.array(Save_DateFrame['Humidity_Status'].values)
            window.plotEvent(x, y, "Humidity (24Hr)", "Humidity (%)")
        elif plotChoice == "soilmoist":
            y = Save_DateFrame[['Moisture_Status0','Moisture_Status1','Moisture_Status2','Moisture_Status3']].astype(float)
            y = np.array(y[['Moisture_Status0','Moisture_Status1','Moisture_Status2','Moisture_Status3']].values)
            #y = pd.to_numeric(Save_DateFrame[['Moisture_Status0','Moisture_Status1','Moisture_Status2','Moisture_Status3']], downcast="float")
            #print(f"Size = {x}, {y}")
            window.plotEvent(x, y, "Soil Moisture (24Hr)", "Soil Moisture (%)", ['Moisture_Status0','Moisture_Status1','Moisture_Status2','Moisture_Status3'])

        elif plotChoice == "roomtemp":
            y = np.array(Save_DateFrame['RoomTemp_Status'].values)
            window.plotEvent(x, y, "Room Temperature (24Hr)", "Room Temperature (C)")
        window.plotCamera()







class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('GreenUI.ui', self)
        self.show()

        self.SetWaterVolumeLevel1 = 0
        self.SetWaterVolumeLevel2 = 0


        ##connect actions widgets Here
        self.WG1SettingLabel.setText(str(self.SetWaterVolumeLevel1))
        self.WG2SettingLabel.setText(str(self.SetWaterVolumeLevel2))
        self.LightOnButton.clicked.connect(self.Event_LightON)
        self.LightAutoButton.clicked.connect(self.Event_LightAuto)
        self.FanOnButton.clicked.connect(self.Event_FanOn)
        self.FanAutoButton.clicked.connect(self.Event_FanAtuo)
        self.WG1M.clicked.connect(self.Event_WaterGroup1Min)
        self.WG1A.clicked.connect(self.Event_WaterGroup1Add)
        self.WG2M.clicked.connect(self.Event_WaterGroup2Min)
        self.WG2A.clicked.connect(self.Event_WaterGroup2Add)
        self.SoilMoisturePlotButton.clicked.connect(lambda: self.setPlot("soilmoist"))
        self.HumidityPlotButton.clicked.connect(lambda: self.setPlot("humid"))
        self.RoomTemperaturePlotButton.clicked.connect(lambda: self.setPlot("roomtemp"))
        #self.CameraPlotButton.clicked.connect(lambda: self.setPlot("camera"))


        ##plot
        self.plotFigure = plt.figure(figsize=(9, 3))
        self.plotCanvas = FigureCanvas(self.plotFigure)
        self.gridLayout_3.addWidget(self.plotCanvas,1,1,1,1)
        self.ax = self.plotFigure.add_subplot(111)
        self.ax.plot([0,1,2,3,4],[10,2,40,10,10])
        self.xformatter = mdates.DateFormatter('%H:%M')
        plt.gcf().axes[0].xaxis.set_major_formatter(self.xformatter)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Plot')
        #plt.tight_layout()
        self.plotCanvas.draw()

        ##Camera
        self.cameraFigure = plt.figure(figsize=(9, 3))
        self.cameraCanvas = FigureCanvas(self.cameraFigure)
        self.gridLayout_4.addWidget(self.cameraCanvas,1,1,1,1)
        self.ax1 = self.cameraFigure.add_subplot(111)
        self.ax1.plot([0,1,2,3,4],[10,2,40,10,10])
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Cam')
        #plt.tight_layout()
        self.cameraCanvas.draw()




    ##write event for widgets Here
    def Event_LightON(self):
        global Settings_dict
        #send("LightSettings = LightON")
        Settings_dict['Light_Setting'] = 1
        #self.LightStatusLabel.setText(Settings_dict['Light_Setting'])
        send(Settings_dict)


    def Event_LightAuto(self):
        global Settings_dict
        #send("LightSettings = LightOFF")
        Settings_dict['Light_Setting'] = 0
        send(Settings_dict)

    def Event_FanOn(self):
        global Settings_dict
        Settings_dict['Fan_Setting'] = 1
        send(Settings_dict)
        

    def Event_FanAtuo(self):
        global Settings_dict
        Settings_dict['Fan_Setting'] = 0
        send(Settings_dict)

    def Event_WaterGroup1Min(self):
        global Settings_dict
        WaterGroupLevel = int(Settings_dict['Water_Setting1'])
        if WaterGroupLevel > 20:
            WaterGroupLevel -= 2
        Settings_dict['Water_Setting1'] = str(WaterGroupLevel)
        send(Settings_dict)

    def Event_WaterGroup1Add(self):
        global Settings_dict
        WaterGroupLevel = int(Settings_dict['Water_Setting1'])
        if WaterGroupLevel < 40:
            WaterGroupLevel += 2
        Settings_dict['Water_Setting1'] = str(WaterGroupLevel)
        send(Settings_dict)

    def Event_WaterGroup2Min(self):
        global Settings_dict
        WaterGroupLevel = int(Settings_dict['Water_Setting2'])
        if WaterGroupLevel > 20:
            WaterGroupLevel -= 2
        Settings_dict['Water_Setting2'] = str(WaterGroupLevel)
        send(Settings_dict)

    def Event_WaterGroup2Add(self):
        global Settings_dict
        WaterGroupLevel = int(Settings_dict['Water_Setting2'])
        if WaterGroupLevel < 40:
            WaterGroupLevel += 2
        Settings_dict['Water_Setting2'] = str(WaterGroupLevel)
        send(Settings_dict)

    def closeEvent(self, event):
        global connected
        connected = False
        send(DISCONNECT_MESSAGE)
        #client.close()

    def setPlot(self, plotChoiceText):
        global plotChoice
        temp = ""
        temp = plotChoiceText
        plotChoice =  temp

    def plotEvent(self, x, y, title, ylabel, legend = []):
        self.ax.clear()
        #self.ax = Save_DateFrame.plot(kind = 'scatter', x = 'Datetime', y = y)
        self.ax.plot(x,y)
        self.ax.xaxis.set_major_formatter(self.xformatter)
        self.ax.set_xlabel('Time(Hr)')
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        self.ax.legend(legend)
        plt.autoscale(enable=True, axis='y', tight=True)
        #plt.tight_layout()
        self.plotCanvas.draw()

    def plotCamera(self):
        self.ax1.clear()
        self.ax1.imshow(cameraInput)
        #plt.tight_layout()
        self.cameraCanvas.draw()

    def statusUpdateEvent(self, UpdateList):
        window_dict = [self.SoilMoistureStatusLabel0,
                self.SoilMoistureStatusLabel1,
                self.SoilMoistureStatusLabel2,
                self.SoilMoistureStatusLabel3,
                self.RoomTempStatusLabel,
                self.HumidityStatusLabel,
                self.LightStatusLabel,
                self.FanStatusLabel,
                self.WG1SettingLabel,
                self.WG2SettingLabel]
        for i ,v in enumerate(UpdateList):
            #print(str(Update_dict[v]))
            window_dict[i].setText(str(v))
            window_dict[i].setAlignment(QtCore.Qt.AlignCenter)
            sleep(0.1)



app = QtWidgets.QApplication(sys.argv)
window = Ui()
GetUpdate_Tread = threading.Thread(target = Update_status)
GetUpdate_Tread.start()

Plot_Tread = threading.Thread(target = PlotUpdate)
Plot_Tread.start()

app.exec_()