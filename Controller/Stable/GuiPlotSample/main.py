# ------------------------------------------------- ----- 
# ---------------------- main.py ---------------- ----- 
# --------------------------------------------- --------- 
from  PyQt5.QtWidgets  import * 
from  PyQt5.uic  import  loadUi
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
import matplotlib.pyplot as plt
from  matplotlib.backends.backend_qt5agg  import  FigureCanvas
from  matplotlib.backends.backend_qt5agg  import  ( NavigationToolbar2QT  as  NavigationToolbar )
import  numpy  as  np 
import  random
     
class  MatplotlibWidget ( QMainWindow ):
    # constructor
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        loadUi ( "PlotTest.ui" , self )

        self . setWindowTitle ( "PyQt5 & Matplotlib Example GUI" )

        self.figure = plt.figure()
        
        self.MplWidget.update(self.figure)

    def plot(self):
        data = [random.random() for i in range(10)]

        self.figure.clear()

        ax = self.figure.add.subplot(111)

        ax.plot(data, '*-')

        self.canvas.draw()

app  =  QApplication([]) 
window  =  MatplotlibWidget() 
window.show() 
app.exec_()
