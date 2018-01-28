# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'invalidKWEntry.ui'
#
# Created: Wed Mar 19 14:51:15 2014
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

class Ui_InvalidKWEntryDialog(object):
    def setupUi(self, InvalidKWEntryDialog):
        InvalidKWEntryDialog.setObjectName(_fromUtf8("InvalidKWEntryDialog"))
        InvalidKWEntryDialog.resize(312, 182)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        InvalidKWEntryDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        InvalidKWEntryDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(InvalidKWEntryDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelInvalidKWEntry = QtGui.QLabel(InvalidKWEntryDialog)
        self.labelInvalidKWEntry.setWordWrap(True)
        self.labelInvalidKWEntry.setObjectName(_fromUtf8("labelInvalidKWEntry"))
        self.verticalLayout.addWidget(self.labelInvalidKWEntry)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonAccept = QtGui.QPushButton(InvalidKWEntryDialog)
        self.pushButtonAccept.setObjectName(_fromUtf8("pushButtonAccept"))
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(InvalidKWEntryDialog)
        QtCore.QMetaObject.connectSlotsByName(InvalidKWEntryDialog)

    def retranslateUi(self, InvalidKWEntryDialog):
        InvalidKWEntryDialog.setWindowTitle(_translate("InvalidKWEntryDialog", "Kein freier Transekt", None))
        self.labelInvalidKWEntry.setText(_translate("InvalidKWEntryDialog", "Es befindet sich kein freier Transektvorgang in der Datenbank. Geben Sie bitte zuerst einen Transektbeginn ein", None))
        self.pushButtonAccept.setText(_translate("InvalidKWEntryDialog", "OK", None))

import resources_rc
