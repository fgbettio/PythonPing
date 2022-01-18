# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 09:28:24 2022

@author: FGBETTIO
"""
#Links:
    #Para gerar executável - https://www.hashtagtreinamentos.com/arquivo-executavel-python?gclid=CjwKCAiA55mPBhBOEiwANmzoQmfQSfSvp4T7iT5L2D-Oq2gSccdTHG6MbVi-q_vGN4EIWGtrKWMnCRoCVUEQAvD_BwE
    #Configurações do grafico - https://www.geeksforgeeks.org/matplotlib-axes-axes-set_adjustable-in-python/
    #Grid - https://www.southampton.ac.uk/~feeg1001/notebooks/Matplotlib.html
    #Exemplo de código usnado matplotlib com botão de zoom - https://qastack.com.br/programming/11874767/how-do-i-plot-in-real-time-in-a-while-loop-using-matplotlib
    
    
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import threading

import subprocess
import platform,re

val =0

def Ping(hostname,timeout):
    #print('Pingando...')
    if platform.system() == "Windows":
        command="ping "+hostname+" -n 1 -w "+str(timeout*1000)
    else:
        command="ping -i "+str(timeout)+" -c 1 " + hostname
    proccess = subprocess.Popen(command, stdout=subprocess.PIPE)
    #print("0=====================")
    saida=proccess.stdout.read().decode('iso_8859_1')
    matches=re.match('.*tempo=([0-9]+)ms.*', saida,re.DOTALL)
    
    if matches is None: 
        print("### Não Conectado!!!!")
        return -1
    else:
        #print(matches.group(1))
        #x = re.findall("<p>.*</p>", txt,re.DOTALL)
        rest= int(matches.group(1),base=10)
        #print(rest)
        return rest

#==============================================================================
#val=Ping('www.google.com.br',3)

class CustomMainWindow(QMainWindow):
    def __init__(self):
        super(CustomMainWindow, self).__init__()
        # Define the geometry of the main window
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("Python Ping")
        # Create FRAME_A
        self.FRAME_A = QFrame(self)
        self.FRAME_A.setStyleSheet("QWidget { background-color: %s }" % QColor(210,210,235,255).name())
        self.LAYOUT_A = QGridLayout()
        self.FRAME_A.setLayout(self.LAYOUT_A)
        self.setCentralWidget(self.FRAME_A)
        # Place the zoom button
        #self.zoomBtn = QPushButton(text = 'zoom')
        #self.zoomBtn.setFixedSize(100, 50)
        #self.zoomBtn.clicked.connect(self.zoomBtnAction)
        #self.LAYOUT_A.addWidget(self.zoomBtn, *(0,0))
        # Place the matplotlib figure
        self.myFig = CustomFigCanvas()
        self.LAYOUT_A.addWidget(self.myFig, *(0,1))
        # Add the callbackfunc to ..
        myDataLoop = threading.Thread(name = 'myDataLoop', target = dataSendLoop, daemon = True, args = (self.addData_callbackFunc,))
        myDataLoop.start()
        #self.labelText.setText("123");
        #self.text.
        
        self.show()
        return

    def addData_callbackFunc(self, value):
        # print("Add data: " + str(value))
        self.myFig.addData(value)
        return

''' End Class '''


class CustomFigCanvas(FigureCanvas, TimedAnimation):
    def __init__(self):
        self.addedData = []
        print("Versão do Matplotlib: "+matplotlib.__version__)
        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
       
        self.y = (self.n * 0.0) + 50
        # The window
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)
        # self.ax1 settings
        self.ax1.set_title("Python Ping - www.google.com.br")
        self.ax1.set_xlabel('tempo')
        self.ax1.set_ylabel('ping (ms)')
        self.line1 = Line2D([], [], color='blue')
        self.line1_tail = Line2D([], [], color='red', linewidth=2)
        self.line1_head = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line1_tail)
        self.ax1.add_line(self.line1_head)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(0, 1000)
        self.ax1.grid(color='b', alpha=0.5, linestyle='dashed', linewidth=0.5)
        #self.ax1.annotate(val, (0,0), (0,0), 'data', None, None, None)
        #self.ax1.text(0, 0, r"$y=x^2$", fontsize=20, color="blue")
        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)
        return

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        lines = [self.line1, self.line1_tail, self.line1_head]
        for l in lines:
            l.set_data([], [])
        return

    def addData(self, value):
        self.addedData.append(value)
        return

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)
            pass
        return

    def _draw_frame(self, framedata):
        margin = 2
        while(len(self.addedData) > 0):
            self.y = np.roll(self.y, -1)
            self.y[-1] = self.addedData[0]
            del(self.addedData[0])

        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y[ 0 : self.n.size - margin ])
        self.line1_tail.set_data(np.append(self.n[-10:-1 - margin], self.n[-1 - margin]), np.append(self.y[-10:-1 - margin], self.y[-1 - margin]))
        self.line1_head.set_data(self.n[-1 - margin], self.y[-1 - margin])
        self._drawn_artists = [self.line1, self.line1_tail, self.line1_head]
        return

''' End Class '''


# You need to setup a signal slot mechanism, to
# send data to your GUI in a thread-safe way.
# Believe me, if you don't do this right, things
# go very very wrong..
class Communicate(QObject):
    data_signal = pyqtSignal(float)

''' End Class '''



def dataSendLoop(addData_callbackFunc):
    # Setup the signal-slot mechanism.
    mySrc = Communicate()
    mySrc.data_signal.connect(addData_callbackFunc)
    i = 0

    while(True):
        if(i > 499):
            i = 0
        #time.sleep(0.1)
        val=(Ping('www.google.com.br',3))
        #print(val)
        mySrc.data_signal.emit(val) # <- Here you emit a signal!
        i += 1
    ###
###

if __name__== '__main__':
    print("Ininiando...")
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Plastique'))
    myGUI = CustomMainWindow()
    sys.exit(app.exec_())