# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'missingTransectEnd.ui'
#
# Created: Fri Mar 14 08:20:54 2014
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

class Ui_MissingTransectEndDialog(object):
    def setupUi(self, MissingTransectEndDialog):
        MissingTransectEndDialog.setObjectName(_fromUtf8("MissingTransectEndDialog"))
        MissingTransectEndDialog.resize(314, 183)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        MissingTransectEndDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MissingTransectEndDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(MissingTransectEndDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 25, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelWarnText = QtGui.QLabel(MissingTransectEndDialog)
        self.labelWarnText.setWordWrap(True)
        self.labelWarnText.setObjectName(_fromUtf8("labelWarnText"))
        self.verticalLayout.addWidget(self.labelWarnText)
        spacerItem1 = QtGui.QSpacerItem(20, 26, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonCancel = QtGui.QPushButton(MissingTransectEndDialog)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtGui.QPushButton(MissingTransectEndDialog)
        self.pushButtonAccept.setObjectName(_fromUtf8("pushButtonAccept"))
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(MissingTransectEndDialog)
        QtCore.QMetaObject.connectSlotsByName(MissingTransectEndDialog)

    def retranslateUi(self, MissingTransectEndDialog):
        MissingTransectEndDialog.setWindowTitle(_translate("MissingTransectEndDialog", "Transektende fehlt", None))
        self.labelWarnText.setText(_translate("MissingTransectEndDialog", "Es befindet sich bereits ein Transektbeginn in der Datenbank, zu dem kein Transektende passt. Falls Sie diese Eingabe tätigen, wird der vorherige Transektbeginn aus der Datenbank gelöscht. ", None))
        self.pushButtonCancel.setText(_translate("MissingTransectEndDialog", "&Abbrechen", None))
        self.pushButtonAccept.setText(_translate("MissingTransectEndDialog", "&OK", None))

import resources_rc
