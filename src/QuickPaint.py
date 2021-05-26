from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os
  
class Paint(QtWidgets.QMainWindow): 
    def __init__(self): 
        super(Paint, self).__init__()
        self.windowSetup()
        self.menuOptionsSetup()
        self.saveCommmandSetup()
        self.eraseCommmandSetup()
        self.colorsSetup()
        self.brushSizeSetup()
  
    def windowSetup(self):
        self.setWindowTitle("QuickPaint") 
        self.setGeometry(100, 100, 500, 500)
        self.setWindowIcon(QtGui.QIcon("./icons/painticon.png"))
        self.image = QtGui.QImage(self.size(), QtGui.QImage.Format_RGB32)
        self.image.fill(QtCore.Qt.white)
        
        # default brush
        self.brushSize = 2
        self.drawing = False
        self.brushColor = QtCore.Qt.black
        self.lastPoint = QtCore.QPoint()

    def menuOptionsSetup(self):
        global main_menu 
        main_menu = self.menuBar()  
        global file_menu 
        file_menu = main_menu.addMenu("File")
        global color_menu
        color_menu = main_menu.addMenu("Color") 
        global size_menu
        size_menu = main_menu.addMenu("Size") 

    def saveCommmandSetup(self):
        save_command = QtWidgets.QAction(QtGui.QIcon("./icons/saveicon.png"), "Save", self) 
        save_command.setShortcut("Ctrl + S") 
        file_menu.addAction(save_command)
        save_command.triggered.connect(self.save)

    def eraseCommmandSetup(self):
        erase_command = QtWidgets.QAction(QtGui.QIcon("./icons/brushicon.png"), "Erase", self)  
        erase_command.setShortcut("Ctrl + E") 
        file_menu.addAction(erase_command)
        erase_command.triggered.connect(self.erase) 

    # designation of menu bar commands
    def save(self): 
        file_path = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", "PNG;;JPG;;All_Files")
        if file_path[0] == "": 
            return
        self.image.save(file_path[0]) 
  
    def erase(self):  
        self.image.fill(QtCore.Qt.white) 
        self.update() 

    def colorsSetup(self):
        black = QtWidgets.QAction(QtGui.QIcon("./icons/blackicon.png"), "Black", self)
        color_menu.addAction(black) 
        black.triggered.connect(self.color_black) 

        white = QtWidgets.QAction(QtGui.QIcon("./icons/whiteicon.png"), "White", self) 
        color_menu.addAction(white) 
        white.triggered.connect(self.color_white) 

        darkCyan = QtWidgets.QAction(QtGui.QIcon("./icons/darkCyanicon.png"), "Cyan", self) 
        color_menu.addAction(darkCyan) 
        darkCyan.triggered.connect(self.color_darkCyan) 

        darkBlue = QtWidgets.QAction(QtGui.QIcon("./icons/darkBlueicon.png"), "Blue", self) 
        color_menu.addAction(darkBlue) 
        darkBlue.triggered.connect(self.color_darkBlue) 

        darkMagenta = QtWidgets.QAction(QtGui.QIcon("./icons/darkMagentaicon.png"), "Magenta", self) 
        color_menu.addAction(darkMagenta) 
        darkMagenta.triggered.connect(self.color_darkMagenta) 

        darkRed = QtWidgets.QAction(QtGui.QIcon("./icons/darkRedicon.png"), "Dark Red", self) 
        color_menu.addAction(darkRed) 
        darkRed.triggered.connect(self.color_darkRed) 

    # designation of colors
    def color_black(self): 
        self.brushColor = QtCore.Qt.black 

    def color_white(self): 
        self.brushColor = QtCore.Qt.white 

    def color_darkCyan(self): 
        self.brushColor = QtCore.Qt.darkCyan

    def color_darkBlue(self): 
        self.brushColor = QtCore.Qt.darkBlue 

    def color_darkMagenta(self): 
        self.brushColor = QtCore.Qt.darkMagenta 

    def color_darkRed(self): 
        self.brushColor = QtCore.Qt.darkRed


    def brushSizeSetup(self):
        size4 = QtWidgets.QAction(QtGui.QIcon("./icons/4icon.png"), "4 pixels", self) 
        size_menu.addAction(size4) 
        size4.triggered.connect(self.Brush4) 

        size8 = QtWidgets.QAction(QtGui.QIcon("./icons/8icon.png"), "8 pixels", self) 
        size_menu.addAction(size8) 
        size8.triggered.connect(self.Brush8) 

        size12 = QtWidgets.QAction(QtGui.QIcon("./icons/12icon.png"), "12 pixels", self) 
        size_menu.addAction(size12) 
        size12.triggered.connect(self.Brush12) 

        size16 = QtWidgets.QAction(QtGui.QIcon("./icons/16icon.png"), "16 pixels", self) 
        size_menu.addAction(size16) 
        size16.triggered.connect(self.Brush16)

    # designation of brush sizes
    def Brush4(self): 
        self.brushSize = 4

    def Brush8(self): 
        self.brushSize = 8

    def Brush12(self): 
        self.brushSize = 12

    def Brush16(self): 
        self.brushSize = 16

    # mouse movement and action setup
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
 
    def mouseReleaseEvent(self, action):
        if action.button() == QtCore.Qt.LeftButton:
            self.drawing = False 

    def mouseMoveEvent(self, event):
        if(event.buttons() & QtCore.Qt.LeftButton) & self.drawing:
            painter = QtGui.QPainter(self.image)
            painter.setPen(QtGui.QPen(self.brushColor, self.brushSize, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()
  
    # setup of painter
    def paintEvent(self, event): 
        canvasPainter = QtGui.QPainter(self) 
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect()) 
