import datetime as dt
import pandas as pd

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

Update_dict = {'Moisture_Status0': [1, 2],
                'Moisture_Status1': [2, 3],
                'Moisture_Status2': [3, 4],
                'Moisture_Status3': [4, 5],
                'RoomTemp_Status': [5, 6],
                'Humidity_Status': [6, 7],
                'LightOnOff_Status':[7, 8],
                'LightLux_Status':[8, 9]}

def CodeTest():
	'''
	print(list(Update_dict.keys())[0])
	df = pd.DataFrame(data = Update_dict)
	print(df)
	df.to_csv('csv_save.csv')
	'''
	'''
	for key, value in Update_dict.items():
		if key =='Moisture_Status1':
			print("Match")
		print(value)
		Update_dict[key] = "100"
	#print(list(Update_dict.keys())[0])
	df = pd.DataFrame()
	df = df.append(Update_dict, ignore_index = True)
	print(df)
	df.to_csv('csv_save.csv')
	'''
	'''
	current_datetime = dt.datetime.now()
	print(current_datetime)
	saved_datetime = current_datetime.strftime("%c")
	print(saved_datetime)
	'''
	df = pd.DataFrame()
	df = df.append(Update_dict, ignore_index = True)
	df = df.append(Update_dict, ignore_index = True)
	df = df.append(Update_dict, ignore_index = True)
	print(df)
	df = df.drop([0])
	print(df)




CodeTest()