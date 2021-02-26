from PyQt5 import QtCore, QtGui, QtWidgets
from digitrec import *
from QuickPaint import *

# setup of main window
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(626, 420)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.backgroundSetup()
        self.tmpSetup()
        self.paintButtonSetup()
        self.addButtonSetup()
        self.subtractionButtonSetup()
        self.multiplciationButtonSetup()
        self.divisionButtonSetup()
        self.translateButtonSetup()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def backgroundSetup(self):
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 631, 401))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("background.png"))
        self.label.setObjectName("label")

    def tmpSetup(self):
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(280, 190, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Beckman")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("Color : white")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

    def paintButtonSetup(self):
        self.paintButton = QtWidgets.QPushButton(self.centralwidget)
        self.paintButton.setGeometry(QtCore.QRect(120, 250, 101, 61))
        font = QtGui.QFont()
        font.setFamily("Jokerman")
        font.setPointSize(12)
        self.paintButton.setFont(font)
        self.paintButton.setAutoFillBackground(False)
        self.paintButton.setObjectName("paintButton")
        self.paintButton.clicked.connect(self.openPaint)
        self.dialogs = list()

    def addButtonSetup(self):
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(415, 250, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(14)
        self.addButton.setFont(font)
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.addOp)

    def subtractionButtonSetup(self):
        self.subtrButton = QtWidgets.QPushButton(self.centralwidget)
        self.subtrButton.setGeometry(QtCore.QRect(465, 250, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(16)
        self.subtrButton.setFont(font)
        self.subtrButton.setObjectName("subtrButton")
        self.subtrButton.clicked.connect(self.subtrOp)

    def multiplciationButtonSetup(self):
        self.multButton = QtWidgets.QPushButton(self.centralwidget)
        self.multButton.setGeometry(QtCore.QRect(415, 285, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(16)
        self.multButton.setFont(font)
        self.multButton.setObjectName("multButton")
        self.multButton.clicked.connect(self.multOp)

    def divisionButtonSetup(self):
        self.divButton = QtWidgets.QPushButton(self.centralwidget)
        self.divButton.setGeometry(QtCore.QRect(465, 285, 41, 31))
        font = QtGui.QFont()
        font.setFamily("Beckman")
        font.setPointSize(16)
        self.divButton.setFont(font)
        self.divButton.setObjectName("divButton")
        self.divButton.clicked.connect(self.divOp)

    def translateButtonSetup(self):
        self.translateButton = QtWidgets.QPushButton(self.centralwidget)
        self.translateButton.setGeometry(QtCore.QRect(280, 270, 61, 20))
        font = QtGui.QFont()
        font.setFamily("Beckman Free")
        font.setPointSize(7)
        self.translateButton.setFont(font)
        self.translateButton.setStyleSheet("color: white; background-color: transparent")
        self.translateButton.setObjectName("translateButton")
        self.translateButton.clicked.connect(self.translateOp)

    # defines paint button operations, redirects to QuickPaint.py
    def openPaint(self):
        self.sub = Second()
        self.sub.show()

    # defines translate operation, computes 4 answers
    def translateOp(self):
        tmp1, tmp2 = makePred()
        self.sum_op = str(tmp1 + tmp2)
        self.diff_op = str(tmp1 - tmp2)
        self.prod_op = str(tmp1 * tmp2) 
        self.quot_op = str(tmp1 / tmp2)

    # pushes operations to text label
    def addOp(self):
        self.label_2.setText(self.sum_op)

    def subtrOp(self):
        self.label_2.setText(self.diff_op)

    def multOp(self):
        self.label_2.setText(self.prod_op)

    def divOp(self):
        self.label_2.setText(self.quot_op)

    # changes windows tiltle names
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SketchMath"))
        self.paintButton.setText(_translate("MainWindow", "PUSH"))
        self.addButton.setText(_translate("MainWindow", "+"))
        self.subtrButton.setText(_translate("MainWindow", "-"))
        self.multButton.setText(_translate("MainWindow", "*"))
        self.divButton.setText(_translate("MainWindow", "/"))
        self.translateButton.setText(_translate("MainWindow", "Translate"))



# non member
def stringToInt(l):
    final = int(''.join(str(i) for i in l))
    return final

# operation for making predication of digits, pulls in digitrec.py
def makePred():
    num1 = []
    num2 = []
    model = Compiler()
    
    final_image1 = imageGray('./test1.png')
    test1 = readNums(final_image1)
    for digit in test1:
        prediction1 = model.predict(digit.reshape(1, 28, 28, 1))    
        num1.append(np.argmax(prediction1))
    final_image2 = imageGray('./test2.png')
    test2 = readNums(final_image2)
    for digit in test2:
        prediction2 = model.predict(digit.reshape(1, 28, 28, 1))    
        num2.append(np.argmax(prediction2))
    firstnum = stringToInt(num1)
    secondnum = stringToInt(num2)
    return firstnum, secondnum
