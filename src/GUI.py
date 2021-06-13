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
        self.show()

        self.compile = CompileThread()
        self.compile.start()

    def backgroundSetup(self):
        self.backgroundImage = QtWidgets.QLabel(self)
        self.backgroundImage.setGeometry(QtCore.QRect(0, 0, 626, 417))
        self.setFixedSize(626, 417)
        self.backgroundImage.setText("")
        self.backgroundImage.setPixmap(QtGui.QPixmap("background2.png"))
        self.backgroundImage.setObjectName("backgroundImage")

    def tmpSetup(self):
        self.answerLabel = QtWidgets.QLabel(self)
        self.answerLabel.setGeometry(QtCore.QRect(280, 197, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Sicret Mono PERSONAL")
        font.setPointSize(11)
        self.answerLabel.setFont(font)
        self.answerLabel.setStyleSheet("Color : white")
        self.answerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.answerLabel.setObjectName("answerLabel")

    def paintButtonSetup(self):
        self.paintButton = QtWidgets.QPushButton(self)
        self.paintButton.setGeometry(QtCore.QRect(125, 235, 95, 61))
        font = QtGui.QFont()
        font.setFamily("Sicret Mono PERSONAL")
        font.setPointSize(17)
        self.paintButton.setFont(font)
        self.paintButton.setAutoFillBackground(False)
        self.paintButton.setObjectName("paintButton")
        self.paintButton.setText("PUSH")
        self.paintButton.clicked.connect(self.openPaint)
        self.dialogs = list()

    def addButtonSetup(self):
        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.setGeometry(QtCore.QRect(419, 235, 35, 25))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(14)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.addButton.setText("+")
        self.addButton.clicked.connect(self.addOp)

    def subtractionButtonSetup(self):
        self.subtrButton = QtWidgets.QPushButton(self)
        self.subtrButton.setGeometry(QtCore.QRect(465, 235, 35, 25))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(16)
        self.subtrButton.setFont(font)
        self.subtrButton.setObjectName("subtrButton")
        self.subtrButton.setText("-")
        self.subtrButton.clicked.connect(self.subtrOp)

    def multiplciationButtonSetup(self):
        self.multButton = QtWidgets.QPushButton(self)
        self.multButton.setGeometry(QtCore.QRect(419, 270, 35, 25))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(16)
        self.multButton.setFont(font)
        self.multButton.setObjectName("multButton")
        self.multButton.setText("*")
        self.multButton.clicked.connect(self.multOp)

    def divisionButtonSetup(self):
        self.divButton = QtWidgets.QPushButton(self)
        self.divButton.setGeometry(QtCore.QRect(465, 270, 35, 25))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(16)
        self.divButton.setFont(font)
        self.divButton.setObjectName("divButton")
        self.divButton.setText("/")
        self.divButton.clicked.connect(self.divOp)


    # defines paint button operations, redirects to QuickPaint.py
    def openPaint(self):
        self.sub = Paint()
        self.sub.show()

    # pushes operations to text label
    def addOp(self):
        tmp1, tmp2 = self.makePred()
        self.answerLabel.setText(str(tmp1 + tmp2))

    def subtrOp(self):
        tmp1, tmp2 = self.makePred()
        self.answerLabel.setText(str(tmp1 - tmp2))

    def multOp(self):
        tmp1, tmp2 = self.makePred()
        self.answerLabel.setText(str(tmp1 * tmp2))

    def divOp(self):
        tmp1, tmp2 = self.makePred()
        self.answerLabel.setText(str(tmp1 / tmp2))

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
