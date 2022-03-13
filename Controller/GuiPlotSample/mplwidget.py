# ------------------------------------------------- ----- 
# --------------------- mplwidget.py -------------------- 
# ------------------------------------------------ ---- 

import sys
import matplotlib
#matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
#import queue
#import numpy as np
#import pdb
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
#from PyQt5.QtCore import pyqtSlot
#from PyQt5.QtMultimedia import QAudioDeviceInfo,QAudio,QCameraInfo

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


    
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()




class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.ui = uic.loadUi('PlotTest.ui', self)
        self.show()

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)

        #self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

        self.ui.gridLayout.addWidget(self.canvas)

        #self.refrence_plot = None

        #self.canvas.plot([0,1,2,3,4],[10,2,40,10,10])
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot([0,1,2,3,4],[10,2,40,10,10])
        xformatter = mdates.DateFormatter('%H:%M')
        plt.gcf().axes[0].xaxis.set_major_formatter(xformatter)
        self.canvas.draw()



app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()