import serial
from time import sleep

FORMAT = 'utf-8'
ser = serial.Serial("/dev/serial0", 9600, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, timeout = 0.5)

def UART_Read():
    global ser
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
            print(f"UART Stop Read")
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

while True:
    #ser.close()
    #ser.open()
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    #ser.flush()
    #received_data = ser.read()
    #print(received_data)
    #ser.write(received_data)
    print(f'In Writing: {ser.in_waiting}')
    print(f'Out Writing: {ser.out_waiting}')
    print(f'is open: {ser.is_open}')
    ser.flush()
    sleep(0.5)
    ser.write("\rget\n"[::-1].encode('utf-8'))
    
    templist = [41,213,1,0]
    for i , v in enumerate(templist):
        sleep(0.1)
        ser.reset_output_buffer()
        ser.reset_input_buffer()
        ser.flush()
        ser.write(f"\r{v}\n".encode('utf-8'))
        

    '''
    sleep(1)
    ser.reset_output_buffer()
    ser.reset_input_buffer()
    ser.flush()
    ser.write(f"\r63\n".encode('utf-8'))
        '''

    #sleep(1)


    for i in range(10):
        strdata = UART_Read()
        print(f"Data: {strdata}")
        
'''
        if len(received_data)<30:
            print ("UART Receive:   ",received_data.decode('utf-8').split(" = "))
            temp = received_data.decode('utf-8').split(" = ")
            print(temp)
        else:
            print("UART Skipping: exit")
'''            

        #print(received_data)
    #ser.write("Get\n"[::-1].encode('utf-8'))

#ser.close()

