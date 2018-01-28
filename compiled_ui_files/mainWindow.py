# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created: Mon Nov 03 17:13:12 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindowMedCet(object):
    def setupUi(self, MainWindowMedCet):
        MainWindowMedCet.setObjectName(_fromUtf8("MainWindowMedCet"))
        MainWindowMedCet.resize(585, 316)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        MainWindowMedCet.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindowMedCet.setWindowIcon(icon)
        MainWindowMedCet.setStyleSheet(_fromUtf8("background-color: #bce2ff"))
        self.centralwidget = QtGui.QWidget(MainWindowMedCet)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelTitle = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(22)
        self.labelTitle.setFont(font)
        self.labelTitle.setObjectName(_fromUtf8("labelTitle"))
        self.verticalLayout.addWidget(self.labelTitle)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 120, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonMainMode = QtGui.QPushButton(self.centralwidget)
        self.pushButtonMainMode.setObjectName(_fromUtf8("pushButtonMainMode"))
        self.gridLayout.addWidget(self.pushButtonMainMode, 1, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 4, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 1, 4, 1, 1)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem7, 1, 2, 1, 1)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem8, 0, 0, 1, 1)
        self.pushButtonEditMode = QtGui.QPushButton(self.centralwidget)
        self.pushButtonEditMode.setObjectName(_fromUtf8("pushButtonEditMode"))
        self.gridLayout.addWidget(self.pushButtonEditMode, 1, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem9)
        self.comboBoxLanguage = QtGui.QComboBox(self.centralwidget)
        self.comboBoxLanguage.setObjectName(_fromUtf8("comboBoxLanguage"))
        self.comboBoxLanguage.addItem(_fromUtf8(""))
        self.comboBoxLanguage.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBoxLanguage)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        MainWindowMedCet.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindowMedCet)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 585, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindowMedCet.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindowMedCet)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindowMedCet.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindowMedCet)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindowMedCet.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindowMedCet)
        QtCore.QMetaObject.connectSlotsByName(MainWindowMedCet)

    def retranslateUi(self, MainWindowMedCet):
        MainWindowMedCet.setWindowTitle(_translate("MainWindowMedCet", "MedCet", None))
        self.labelTitle.setText(_translate("MainWindowMedCet", "MedCet", None))
        self.label.setText(_translate("MainWindowMedCet", "<html><head/><body><p><img src=\":/logos/oc-logo.png\"/></p></body></html>", None))
        self.pushButtonMainMode.setText(_translate("MainWindowMedCet", "Erfassen", None))
        self.pushButtonEditMode.setText(_translate("MainWindowMedCet", "Editieren", None))
        self.comboBoxLanguage.setItemText(0, _translate("MainWindowMedCet", "Deutsch", None))
        self.comboBoxLanguage.setItemText(1, _translate("MainWindowMedCet", "English", None))
        self.toolBar.setWindowTitle(_translate("MainWindowMedCet", "toolBar", None))

import resources_rc
