from PyQt5 import QtCore, QtGui, QtWidgets
from digitrec import *
from QuickPaint import *

# setup of main window
class MainGUI(QtWidgets.QWidget):
    def __init__(self):
        # initializes mainWindow
        super().__init__()
        self.setupUi()
    
    def setupUi(self):
        self.resize(626, 420)
        self.setObjectName("centralwidget")
        self.setWindowTitle("SketchMath")
        self.backgroundSetup()
        self.tmpSetup()
        self.paintButtonSetup()
        self.addButtonSetup()
        self.subtractionButtonSetup()
        self.multiplciationButtonSetup()
        self.divisionButtonSetup()
        self.translateButtonSetup()
        self.show()

        self.compile = CompileThread()
        self.compile.start()

    def backgroundSetup(self):
        self.backgroundImage = QtWidgets.QLabel(self)
        self.backgroundImage.setGeometry(QtCore.QRect(0, 0, 631, 401))
        self.backgroundImage.setText("")
        self.backgroundImage.setPixmap(QtGui.QPixmap("background.png"))
        self.backgroundImage.setObjectName("backgroundImage")

    def tmpSetup(self):
        self.answerLabel = QtWidgets.QLabel(self)
        self.answerLabel.setGeometry(QtCore.QRect(280, 190, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Beckman")
        font.setPointSize(11)
        self.answerLabel.setFont(font)
        self.answerLabel.setStyleSheet("Color : white")
        self.answerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.answerLabel.setObjectName("answerLabel")

    def paintButtonSetup(self):
        self.paintButton = QtWidgets.QPushButton(self)
        self.paintButton.setGeometry(QtCore.QRect(120, 250, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Jokerman")
        font.setPointSize(12)
        self.paintButton.setFont(font)
        self.paintButton.setAutoFillBackground(False)
        self.paintButton.setObjectName("paintButton")
        self.paintButton.setText("PUSH")
        self.paintButton.clicked.connect(self.openPaint)
        self.dialogs = list()

    def addButtonSetup(self):
        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.setGeometry(QtCore.QRect(415, 250, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(14)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.addButton.setText("+")
        self.addButton.clicked.connect(self.addOp)

    def subtractionButtonSetup(self):
        self.subtrButton = QtWidgets.QPushButton(self)
        self.subtrButton.setGeometry(QtCore.QRect(465, 250, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(16)
        self.subtrButton.setFont(font)
        self.subtrButton.setObjectName("subtrButton")
        self.subtrButton.setText("-")
        self.subtrButton.clicked.connect(self.subtrOp)

    def multiplciationButtonSetup(self):
        self.multButton = QtWidgets.QPushButton(self)
        self.multButton.setGeometry(QtCore.QRect(415, 285, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(16)
        self.multButton.setFont(font)
        self.multButton.setObjectName("multButton")
        self.multButton.setText("*")
        self.multButton.clicked.connect(self.multOp)

    def divisionButtonSetup(self):
        self.divButton = QtWidgets.QPushButton(self)
        self.divButton.setGeometry(QtCore.QRect(465, 285, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Beckman")
        font.setPointSize(16)
        self.divButton.setFont(font)
        self.divButton.setObjectName("divButton")
        self.divButton.setText("/")
        self.divButton.clicked.connect(self.divOp)

    def translateButtonSetup(self):
        self.translateButton = QtWidgets.QPushButton(self)
        self.translateButton.setGeometry(QtCore.QRect(280, 270, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(7)
        self.translateButton.setFont(font)
        self.translateButton.setStyleSheet("color: white; background-color: transparent")
        self.translateButton.setObjectName("translateButton")
        self.translateButton.setText("Translate")
        self.translateButton.clicked.connect(self.translateOp)

    # defines paint button operations, redirects to QuickPaint.py
    def openPaint(self):
        self.sub = Paint()
        self.sub.show()

    # defines translate operation, computes 4 answers
    def translateOp(self):
        tmp1, tmp2 = self.makePred()
        self.sumOperation = str(tmp1 + tmp2)
        self.diffOperation = str(tmp1 - tmp2)
        self.prodOperation = str(tmp1 * tmp2) 
        self.quotOperation = str(tmp1 / tmp2)

    # pushes operations to text label
    def addOp(self):
        self.answerLabel.setText(self.sumOperation)

    def subtrOp(self):
        self.answerLabel.setText(self.diffOperation)

    def multOp(self):
        self.answerLabel.setText(self.prodOperation)

    def divOp(self):
        self.answerLabel.setText(self.quotOperation)

    def stringToInt(self, inputString):
        newInt = int(''.join(str(i) for i in inputString))
        return newInt

    # operation for making predication of digits, pulls in digitrec.py
    def makePred(self):
        global model
        num1 = []
        num2 = []
        
        firstImage = imageGray('./test1.png')
        readOne = readNums(firstImage)
        for digit in readOne:
            prediction1 = model.predict(digit.reshape(1, 28, 28, 1))    
            num1.append(np.argmax(prediction1))
        
        secondImage = imageGray('./test2.png')
        readTwo = readNums(secondImage)
        for digit in readTwo:
            prediction2 = model.predict(digit.reshape(1, 28, 28, 1))    
            num2.append(np.argmax(prediction2))

        firstNum = self.stringToInt(num1)
        secondNum = self.stringToInt(num2)
        return firstNum, secondNum


global model
class CompileThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def run(self):
        global model
        model = Compiler()
