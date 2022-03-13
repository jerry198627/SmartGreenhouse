import socket 
import threading
import serial
from time import sleep
import pickle
import pandas as pd
import numpy as np
import datetime as dt
import picamera
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates


#Init Server
HEADER = 64
PORT = 5050
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.1.15"
connected = True

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
NEWLINE = "\n"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

#Init serial UART
ser = serial.Serial("/dev/serial0", 9600, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout = 0.5)

#list on input from UART

Update_dict = {'Moisture_Status0': 1,
                'Moisture_Status1': 2,
                'Moisture_Status2': 3,
                'Moisture_Status3': 4,
                'RoomTemp_Status': 5,
                'Humidity_Status': 6,
                'Light_Status':7,
                'Fan_Status':8,
                'WG1_Set':9,
                'WG2_Set':10}

Settings_dict = {'Water_Setting1' : 20,
                'Water_Setting2': 20,
                'Light_Setting': 0,
                'Fan_Setting': 0}

#

#Init pandas for save data
Save_DateFrame = pd.read_csv('csv_save.csv')
#.DataFrame()
#


CameraData = np.empty((240, 320, 3), dtype=np.uint8)


#Get msg from client
def get_msg(conn):
    global connected
    msg_length = conn.recv(HEADER).decode(FORMAT)
    #print(f"MasLength: {msg_length}")
    if msg_length:
        msg_length = int(msg_length)
        msg = b''
        while msg_length > 10:
            #print(f"{msg_length}   {len(msg)}")
            msg = msg + conn.recv(10)
            msg_length = msg_length - 10
        if msg_length:
            #print(f"{msg_length}   {len(msg)}")
            msg = msg + conn.recv(msg_length)
            msg_length -= msg_length
            #print(f"{msg_length}   {len(msg)}")
        #print(f"TCPRecieve len: {len(msg)}")
        msg = pickle.loads(msg)
        #print(f"Pickled recieved: {msg}")
        if str(msg) == DISCONNECT_MESSAGE:
            print(f"[Conn] Get DC")
            connected = False 
        return msg
        
    return msg_length



#Send msg to client
def send(conn, msg):
    message = pickle.dumps(msg)
    #message = msg.encode(FORMAT)
    #temp = pickle.loads(message)
    print(f"Sending Type: {type(message)}")
    msg_length = len(message)
    print(f"Sending lenght: {len(message)}")
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    #print(f"Msg: Length={msg_length}   Msg={message}")
    conn.send(send_length)
    conn.send(message)
    #recieveMsg = client.recv(2048).decode(FORMAT)
    #print(f"Get: {recieveMsg}")


#handle each clients update status and uart update
def handle_client(conn, addr):          #Socket(Rx/Tx), UART(Tx)
    global connected, Settings_dict
    print("[NEW CONNECTION]", addr," connected.")
    connected = True
    while connected:
        msg = get_msg(conn)
        if msg:
            print(f"[{addr}] {msg}")
            if msg == "GetUpdate":
                
                send(conn, Update_dict)
                temp = Save_DateFrame[['Datetime','Moisture_Status0','Moisture_Status1','Moisture_Status2','Moisture_Status3','RoomTemp_Status','Humidity_Status']]
                print(f"DataframeSending: {temp}")
                send(conn, temp)
                
                #print(f"CameraSending: {type(temp)}")
                send(conn, CameraData)
                
                '''
                for i, v in enumerate(Update_List):
                    print(f"[Sending] Update: {v}")
                    send(conn, int(v))  
                '''
                tempmsg = get_msg(conn)
                print(type(tempmsg))
                if type(tempmsg) == type(Settings_dict):
                    Settings_dict = tempmsg
                print(f"[Conn] Setting List : {Settings_dict}")
                '''
                Update_dict['Light_Status'] = Settings_dict['Light_Setting']
                Update_dict['Fan_Status'] = Settings_dict['Fan_Setting']
                Update_dict['WG1_Set'] = Settings_dict['Water_Setting1']
                Update_dict['WG2_Set'] = Settings_dict['Water_Setting2']
                '''
                print(f"[Conn] Update_dict : {Update_dict}")

            #conn.send("Msg received".encode(FORMAT))

    conn.close()

def GUIPlot():
    time = Save_DateFrame['Datetime'].values
    for i, v in enumerate(time):
        time[i] = dt.datetime.strptime(v,'%c')
        print(f"Time : {type(time[i])}")
    x = np.array(time)
    y = np.array(Save_DateFrame['Moisture_Status0'].values)

    print(f"{x}  {y}")
    #print(result)
    #xformatter = mdates.DateFormatter('%H:%M')
    #plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
    Plot_data = plt.plot(x,y)
    return Plot_data


    #plt.show()


def getCamera():
    global CameraData
    while True:
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)
            camera.framerate = 24
            sleep(5)
            CameraOuput = np.empty((240, 320, 3), dtype=np.uint8)
            camera.capture(CameraOuput, 'rgb')

            #output = np.array([[100, 1123],[4324, 5010]])
            
        #print(f"getCam: {CameraOuput.shape}\n")
        CameraData = CameraOuput
    #return CameraOuput







#Get Data from K64F & Store to Variable
def UART():
    global CameraData
    #sent_data = "GetM\n"[::-1]
    '''
    for i in range(10):
        UART_Update()
        '''
    while True:
        
        UART_Update()

        #print(f"Update_dict = {Update_dict}\n")

        
        #sleep(10)
        


def UART_Update():
    global Update_dict
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.flush()
    #ser.writelines("Get\n"[::-1].encode('utf-8'))
    ser.write("\nget\r"[::-1].encode('utf-8'))

    #Send Update to UART
    for i , v in enumerate(Settings_dict):
        sleep(0.01)
        ser.reset_output_buffer()
        ser.reset_input_buffer()
        ser.flush()
        #print(f"[UART] Sending setting_dist : {v}  {Settings_dict[v]}")
        ser.write(f"\r{Settings_dict[v]}\n".encode('utf-8'))

    #Get update from uart to sent to client
    for i, v in enumerate(Update_dict):
        result = UART_Read()   
        #result = list of string input (ex. ['MoisLevel', '10'])
        #print(f"[UART] Result : {len(result)}    {result}")
        if result[0] == v and len(result) == 2:
            #print("Get: ",result)
            try:
                Update_dict[v] = "{:g}".format(float(result[1].rstrip("\n")))
            except:
                print(f"[UART] Cannot Update_dict")
                pass

    print(f"[UART] Update_dict = {Update_dict}\n")
    print(f"[UART] Settings_dict = {Settings_dict}\n")






def UART_Read():
    read = 1
    strdata = ""
    while read:
        #sleep(0.01)
        received_data = ser.read()
        try:
            received_data = received_data.decode(FORMAT)
        except:
            print(f"[UART Error] Cannot Decode")
            #ser.write("\r\n"[::-1].encode(FORMAT))
            #received_data = ''
            break
        if received_data == '\n' or received_data == '':
            #print(f"UART Stop Read")
            read = 0
        else:
            strdata = strdata + received_data
    '''
    if ser.timeout:
        #print("UART Skipping: Timeout")
        #ser.write("\r\n"[::-1].encode(FORMAT))
        #print(f"Reads: {received_data}")
        '''
    received_data = strdata
    #print(f"{len(received_data)}      {received_data}")
    if len(received_data)<40:
        #print ("UART Receive:   ",received_data.split(" = "))
        return received_data.split(" = ")
    else:
        print("UART Skipping: exit")

    return "Nan"


#Save Date to file.csv
def Start_Save_data():
    global Save_DateFrame

    #Start Repeat Thread
    SaveData_Thread = threading.Timer(60, Start_Save_data)
    SaveData_Thread.start()

    Current_datetime = dt.datetime.now()
    Current_datetime_str = Current_datetime.strftime("%c")
    Save_dict = {'Datetime' : Current_datetime_str}
    Save_dict.update(Update_dict)
    #print(f"Time: {Save_dict}")

    if len(Save_DateFrame) >= 1440:
        Save_DateFrame = Save_DateFrame.drop([0])
    #print(f"Daretime {Current_datetime.strftime('%S')}")

    #if int(Current_datetime.strftime('%S')) == 1:
    Save_DateFrame = Save_DateFrame.append(Save_dict, ignore_index = True)
    #print(f"Save_DateFrame: {Save_DateFrame}")
    Save_DateFrame.to_csv('csv_save.csv',index = False )
    

        

def Server_Start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        print(f"Server {conn}")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
        


print("[STARTING] server is starting...")

UART_Thread = threading.Thread(target=UART)
UART_Thread.start()

Camera_Thread = threading.Thread(target = getCamera)
Camera_Thread.start()

sleep(5)
Start_Save_data()
Server_Start()




