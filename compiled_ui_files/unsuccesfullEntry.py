# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unsuccesfullEntry.ui'
#
# Created: Fri Feb 28 10:11:55 2014
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

class Ui_UnsuccesfulEntryDialog(object):
    def setupUi(self, UnsuccesfulEntryDialog):
        UnsuccesfulEntryDialog.setObjectName(_fromUtf8("UnsuccesfulEntryDialog"))
        UnsuccesfulEntryDialog.resize(420, 196)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        UnsuccesfulEntryDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UnsuccesfulEntryDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(UnsuccesfulEntryDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelErrorMessage = QtGui.QLabel(UnsuccesfulEntryDialog)
        self.labelErrorMessage.setWordWrap(True)
        self.labelErrorMessage.setObjectName(_fromUtf8("labelErrorMessage"))
        self.verticalLayout.addWidget(self.labelErrorMessage)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonOk = QtGui.QPushButton(UnsuccesfulEntryDialog)
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.horizontalLayout.addWidget(self.pushButtonOk)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(UnsuccesfulEntryDialog)
        QtCore.QObject.connect(self.pushButtonOk, QtCore.SIGNAL(_fromUtf8("clicked()")), UnsuccesfulEntryDialog.close)
        QtCore.QMetaObject.connectSlotsByName(UnsuccesfulEntryDialog)

    def retranslateUi(self, UnsuccesfulEntryDialog):
        UnsuccesfulEntryDialog.setWindowTitle(_translate("UnsuccesfulEntryDialog", "Unerfolgreicher Datenbankeintrag", None))
        self.labelErrorMessage.setText(_translate("UnsuccesfulEntryDialog", "TextLabel", None))
        self.pushButtonOk.setText(_translate("UnsuccesfulEntryDialog", "Ok", None))

import resources_rc
