# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nonValidEntry.ui'
#
# Created: Fri Feb 28 09:21:35 2014
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

class Ui_nonValidEntryDialog(object):
    def setupUi(self, nonValidEntryDialog):
        nonValidEntryDialog.setObjectName(_fromUtf8("nonValidEntryDialog"))
        nonValidEntryDialog.resize(389, 237)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        nonValidEntryDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        nonValidEntryDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(nonValidEntryDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 108, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelNonValidEntries = QtGui.QLabel(nonValidEntryDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.labelNonValidEntries.setFont(font)
        self.labelNonValidEntries.setText(_fromUtf8(""))
        self.labelNonValidEntries.setWordWrap(True)
        self.labelNonValidEntries.setObjectName(_fromUtf8("labelNonValidEntries"))
        self.verticalLayout.addWidget(self.labelNonValidEntries)
        spacerItem1 = QtGui.QSpacerItem(20, 108, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonOk = QtGui.QPushButton(nonValidEntryDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.pushButtonOk.setFont(font)
        self.pushButtonOk.setObjectName(_fromUtf8("pushButtonOk"))
        self.horizontalLayout.addWidget(self.pushButtonOk)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(nonValidEntryDialog)
        QtCore.QMetaObject.connectSlotsByName(nonValidEntryDialog)

    def retranslateUi(self, nonValidEntryDialog):
        nonValidEntryDialog.setWindowTitle(_translate("nonValidEntryDialog", "Ungültige Eingabe", None))
        self.pushButtonOk.setText(_translate("nonValidEntryDialog", "Ok", None))

import resources_rc
