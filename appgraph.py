from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget

import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import pyqtgraph as pg
import sys
import numpy as np

def newwindow():
    LoadW = QtGui.QWindow()
    LoadW.show()

def plotClicked(pos):
    print('woot')
    print(pos)
    return pos


def imageHoverEvent(event, data):
    """Show the position, pixel, and value under the mouse cursor.
    """
    if event.isExit():
        p1.setTitle("")
        return
    pos = event.pos()
    i, j = pos.y(), pos.x()
    i = int(np.clip(i, 0, data.shape[0] - 1))
    j = int(np.clip(j, 0, data.shape[1] - 1))
    val = data[i, j]
    ppos = img.mapToParent(pos)
    x, y = ppos.x(), ppos.y()
    p1.setTitle("pos: (%0.1f, %0.1f)  pixel: (%d, %d)  value: %g" % (x, y, i, j, val))

def mouseMoved(evt):
    pos = evt[0]  ## using signal proxy turns original arguments into a tuple
    if p3.sceneBoundingRect().contains(pos):
        mousePoint = p3.vb.mapSceneToView(evt[0])
        print(mousePoint)
        #index = int(mousePoint.x())
        #if index > 0 and index < len(data1):
        #       label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
        #vLine.setPos(mousePoint.x())
        #hLine.setPos(mousePoint.y())
        #print(mousePoint.x())
        #print(mousePoint.y())

class MainW(QtGui.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self):
        super(MainW, self).__init__()
        self.setGeometry(50,50,1600,1000)
        self.setWindowTitle('suite2p')
        #self.setStyleSheet("QMainWindow {background: 'black';}")
        self.selectionMode = False
        self.masks = np.random.random((512,512,3))
        self.resized.connect(self.windowsize)
        ### menu bar options
        # load processed data
        loadProc = QtGui.QAction('&Load processed data', self)
        loadProc.setShortcut('Ctrl+L')
        loadProc.setStatusTip('load processed data in suite2p format')
        loadProc.triggered.connect(self.load_proc)
        # load masks
        loadMask = QtGui.QAction('&Load masks and extract traces', self)
        loadMask.setShortcut('Ctrl+L')
        loadMask.setStatusTip('load mask pixels in suite2p format')
        # save file
        saveFile = QtGui.QAction('&Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.triggered.connect(self.file_save)
        # make menuBar!
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(loadProc)
        file_menu.addAction(loadMask)
        file_menu.addAction(saveFile)

        x = np.linspace(-50, 50, 1000)
        y = np.sin(x) / x

        ### main widget with plots
        #self.main_widget = QtGui.QWidget(self)
        #self.main_widget.resize(500,500)
        #self.main_widget.move(300,300)
        #wid = QtGui.QWidget(self)
        win = pg.GraphicsView()
        self.setCentralWidget(win)
        l = pg.GraphicsLayout(border=(100,100,100))
        win.setCentralItem(l)
        win.show()
        l.addLabel('Buttons for views',row=0,col=0)
        p0 = l.addLabel('F*.npy',row=0,col=1,colspan=2)
        p1 = l.addViewBox(lockAspect=True,name='plot1',row=1,col=1)
        #p1.setLimits(xMin=-10, xMax=522,
             #minXRange=20, maxXRange=522,
             #yMin=-10, yMax=522,
             #minYRange=20, maxYRange=522)
        img = pg.ImageItem()
        p1.scene().sigMouseClicked.connect(plotClicked)

        data = np.random.random((512,512,3))
        img.setImage(data)
        p1.addItem(img)

        #pos = p1.scene().sigMouseMoved.connect(plotClicked)
        #pos = p1.mapSceneToView(pos)
        #p1.autoRange()
        p2 = l.addViewBox(lockAspect=True,name='plot2',row=1,col=2)
        #p2.setLimits(xMin=-10, xMax=522,
            #minXRange=20, maxXRange=522,
            #yMin=-10, yMax=522,
            #minYRange=20, maxYRange=522)

        img = pg.ImageItem()#np.random.random((512,512,3)),clickable=True)
        img.setImage(data)
        p2.addItem(img)
        img.setImage = np.random.random((512,512,3))
        #pos = p2.scene().sigMouseMoved.connect(plotClicked)
        #print(p2.mapSceneToView(pos))
        p2.autoRange()
        p2.setXLink('plot1')
        p2.setYLink('plot1')

        l.nextRow()
        p3 = l.addPlot(row=2,col=1,colspan=2)
        plot = p3.plot(x,y,pen='y')
        p3.setMouseEnabled(x=True,y=False)
        p3.enableAutoRange(x=False,y=True)

        proxy = pg.SignalProxy(p3.scene().sigMouseMoved, rateLimit=60 ,slot=mouseMoved)
        pg.QtGui.QApplication.processEvents()

        #print(proxy)

        #p2 = l.addPlot(x=x,y=y,name='plot2')
        #l.addItem(p1)
        #vb.addItem(p1)
        #l.addItem(vb, 0, 1)
        #win.addLabel("linked views",colspan=2)
        #win.nextRow()
        #win.resize(1500,900)
        #p1=win.addPlot(x=x,y=y,name="plot1")
        #p2=win.addPlot(x=x,y=y,name="plot2")
        #p2.setYLink('plot1')
        #p2.setXLink('plot1')



        #self.setCentralWidget(wid)
        #l = QtGui.QVBoxLayout()
        #wid.setLayout(l)
        #self.plot = pg.GraphicsView()
        #self.plot = PlotCells(self, dpi=100)
        #self.toolbar = NavigationToolbar(self.plot,self)
        #self.toolbar.Realize()
        #tw,th=self.toolbar.GetSizeTuple()
        #fw,fh=self.plot.GetSizeTuple()
        #self.toolbar.resize(500,30)
        #self.toolbar.move(300,0)

        #cid = self.plot.mpl_connect('button_press_event', self.plot.onclick)
        #self.toolbar = NavigationToolbar(self.sc, self.main_widget)
        #dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        #l.addWidget(self.plot)
        #self.setLayout(self.l)
        #self.setCentralWidget(l)
        #l.addWidget(dc)
        #self.main_widget.setFocus()
        #self.setCentralWidget(self.main_widget)


        ### checkboxes
        checkBox = QtGui.QCheckBox('plot neuropil',self)
        checkBox.move(100,100)
        checkBox.stateChanged.connect(self.plot_neuropil)
        checkBox.toggle()

        #self.plots = QtGui.QWidget(self,width=1000,height=300)
        #layout = QtGui.QGridLayout()
        #self.plots.setLayout(layout)
        #plot1 = pg.PlotWidget
        #layout.addWidget(plot1,0,0,1,1)
        #elf.plots =  QtGui.QWidget(self,width=1000,height=300)
        #elf.plots.move(300,100)
        #self.plots        = PlotCells(self,width=10,height=4)


        #layout = QtGui.QVBoxLayout()
        #layout.addWidget(self.mpl_toolbar)
        #layout.addWidget(self.plots)
        #self.setLayout(layout)

        #elf.plots.addWidget(self.navi_toolbar)


        ### buttons for different views
        self.mask_view()

    def windowsize(self):
        print(10)
    #def resizeEvent(self,event):
    #    self.resized.emit()
    #    return super(MainW,self).resizeEvent(event)

    def plot_neuropil(self,state):
        if state == QtCore.Qt.Checked:
            print('yay')
        else:
            print('boo')

    def load_proc(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        #print(name)
        masks = np.load(name[0])

        if masks.ndim == 2 | (masks.ndim==3 & masks.shape[2]==3):
            self.masks = masks
            self.plot.plot(masks,masks)
            #pg.image(masks)
            self.selectionMode = True
        else:
            tryagain = QtGui.QMessageBox.question(self, 'error',
                                                  'Incorrect file, choose another?',
                                                  QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
            if tryagain == QtGui.QMessageBox.Yes:
                self.load_proc(self)
            else:
                pass

    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self,'Save File')
        file = open(name,'w')
        file.write('boop')
        file.close()

    # different mask views
    def mask_view(self):
        btn = QtGui.QPushButton('mean image (M)', self)
        btn.setShortcut('M')
        btn.clicked.connect(newwindow)
        btn.resize(btn.minimumSizeHint())
        btn.move(10,30)
        self.show()

class PlotCells(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        #self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setFocus()
        #self.mpl_toolbar = NavigationToolbar(self, parent)
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # add axes
        self.figure.patch.set_facecolor('black')
        self.ax1 = self.figure.add_axes([0.01,0.2,0.47,0.73])
        self.ax1.axis('off')
        self.ax2 = self.figure.add_axes([0.52,0.2,0.47,0.73], sharex=self.ax1, sharey=self.ax1)
        self.ax2.axis('off')
        self.ax3 = self.figure.add_axes([0.01,0.02,0.98,0.2])
        self.ax3.set_facecolor('black')

    def plot(self, masks1, masks2):
        self.ax1.imshow(masks1)
        self.ax2.imshow(masks2)
        self.ax3.plot(np.random.random((1000,)))

        #ax.set_title('PyQt Matplotlib Example')
        #self.figure.tight_layout()

        self.draw()
        self.show()

    def onclick(self,event):
        if event.inaxes:
            print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
                  ('double' if event.dblclick else 'single', event.button,
                   event.x, event.y, event.xdata, event.ydata))
            if self.ax1 is event.inaxes:
                print('plot1')


def run():
    ## Always start by initializing Qt (only once per application)
    app = QtGui.QApplication(sys.argv)
    GUI = MainW()
    #plot = pg.PlotWidget()
    #GUI.setCentralWidget(plot)
    #plot.resize(400,400)
    #plot.sigPointsClicked.connect(plot,meclick)
    sys.exit(app.exec_())

run()

## Define a top-level widget to hold everything
#w = QtGui.QWidget()
#w.setGeometry(0,0,900,500)
#w.setWindowTitle('suite2p')

## Create some widgets to be placed inside
#btn = QtGui.QPushButton('press me')
#text = QtGui.QLineEdit('enter text')
#listw = QtGui.QListWidget()
#plot = pg.PlotWidget()

## Create a grid layout to manage the widgets size and position
#layout = QtGui.QGridLayout()
#w.setLayout(layout)

## Add widgets to the layout in their proper positions
#layout.addWidget(btn, 0, 0)   # button goes in upper-left
#layout.addWidget(text, 1, 0)   # text edit goes in middle-left
#layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
#layout.addWidget(plot, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows

## Display the widget as a new window
#w.show()

## Start the Qt event loop
#app.exec_()
