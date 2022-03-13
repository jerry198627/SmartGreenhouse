import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates

Save_DateFrame = pd.read_csv('csv_save.csv')
print(Save_DateFrame)

time = Save_DateFrame['Datetime'].values
timelist = []
for i, v in enumerate(time):
	timelist.append(dt.datetime.strptime(v,'%c'))
	print(f"Time : {type(timelist[i])}")
x = np.array(timelist)
y = np.array(Save_DateFrame['RoomTemp_Status'].values)

print(Save_DateFrame[['Datetime',
                        'Moisture_Status0',
                        'Moisture_Status1',
                        'Moisture_Status2',
                        'Moisture_Status3',
                        'RoomTemp_Status',
                        'Humidity_Status']])
#print(result)
result = plt.scatter(x,y)
xformatter = mdates.DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)

'''
ax = Save_DateFrame.plot(kind = 'scatter', x = 'Datetime', y = 'RoomTemp_Status')
xformatter = mdates.DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
ax.tick_params(axis ='x', rotation = 45)
#plt.xticks(np.arange(0, 51, 5))
'''
plt.show()