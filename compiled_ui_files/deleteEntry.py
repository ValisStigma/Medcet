# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deleteEntry.ui'
#
# Created: Thu Mar 06 10:05:34 2014
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

class Ui_DeletionsDialog(object):
    def setupUi(self, DeletionsDialog):
        DeletionsDialog.setObjectName(_fromUtf8("DeletionsDialog"))
        DeletionsDialog.resize(270, 160)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        DeletionsDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DeletionsDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(DeletionsDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(DeletionsDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(20, 30, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonAbortDelete = QtGui.QPushButton(DeletionsDialog)
        self.pushButtonAbortDelete.setObjectName(_fromUtf8("pushButtonAbortDelete"))
        self.horizontalLayout.addWidget(self.pushButtonAbortDelete)
        self.pushButtonOkDelete = QtGui.QPushButton(DeletionsDialog)
        self.pushButtonOkDelete.setObjectName(_fromUtf8("pushButtonOkDelete"))
        self.horizontalLayout.addWidget(self.pushButtonOkDelete)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DeletionsDialog)
        QtCore.QMetaObject.connectSlotsByName(DeletionsDialog)

    def retranslateUi(self, DeletionsDialog):
        DeletionsDialog.setWindowTitle(_translate("DeletionsDialog", "Löschen", None))
        self.label.setText(_translate("DeletionsDialog", "Hierdurch wird dieser Eintrag komplett aus der Datenbank entfernt.", None))
        self.pushButtonAbortDelete.setText(_translate("DeletionsDialog", "&Abbrechen", None))
        self.pushButtonOkDelete.setText(_translate("DeletionsDialog", "&Ok", None))

import resources_rc
