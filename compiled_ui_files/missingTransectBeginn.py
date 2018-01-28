# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'missingTransectBeginn.ui'
#
# Created: Wed Mar 19 14:35:13 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_MissingTransectBeginnDialog(object):
    def setupUi(self, MissingTransectBeginnDialog):
        MissingTransectBeginnDialog.setObjectName(_fromUtf8("MissingTransectBeginnDialog"))
        MissingTransectBeginnDialog.resize(314, 183)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        MissingTransectBeginnDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MissingTransectBeginnDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(MissingTransectBeginnDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelWarnText = QtGui.QLabel(MissingTransectBeginnDialog)
        self.labelWarnText.setWordWrap(True)
        self.labelWarnText.setObjectName(_fromUtf8("labelWarnText"))
        self.verticalLayout.addWidget(self.labelWarnText)
        spacerItem1 = QtGui.QSpacerItem(20, 26, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonAccept = QtGui.QPushButton(MissingTransectBeginnDialog)
        self.pushButtonAccept.setObjectName(_fromUtf8("pushButtonAccept"))
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MissingTransectBeginnDialog)
        QtCore.QMetaObject.connectSlotsByName(MissingTransectBeginnDialog)

    def retranslateUi(self, MissingTransectBeginnDialog):
        MissingTransectBeginnDialog.setWindowTitle(_translate("MissingTransectBeginnDialog", "Transektbeginn fehlt", None))
        self.labelWarnText.setText(_translate("MissingTransectBeginnDialog", "Es befindet sich kein passender Transektbeginn in der Datenbank. Geben Sie bitte zuerst einen Transektbeginn ein.", None))
        self.pushButtonAccept.setText(_translate("MissingTransectBeginnDialog", "&OK", None))

import resources_rc
