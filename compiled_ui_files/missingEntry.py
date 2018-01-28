# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'missingEntry.ui'
#
# Created: Fri Feb 28 09:23:04 2014
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

class Ui_missingEntryDialog(object):
    def setupUi(self, missingEntryDialog):
        missingEntryDialog.setObjectName(_fromUtf8("missingEntryDialog"))
        missingEntryDialog.resize(391, 236)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        missingEntryDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        missingEntryDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(missingEntryDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelMissingEntries = QtGui.QLabel(missingEntryDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.labelMissingEntries.setFont(font)
        self.labelMissingEntries.setText(_fromUtf8(""))
        self.labelMissingEntries.setWordWrap(True)
        self.labelMissingEntries.setObjectName(_fromUtf8("labelMissingEntries"))
        self.verticalLayout.addWidget(self.labelMissingEntries)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonNonValidBack = QtGui.QPushButton(missingEntryDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.pushButtonNonValidBack.setFont(font)
        self.pushButtonNonValidBack.setObjectName(_fromUtf8("pushButtonNonValidBack"))
        self.horizontalLayout.addWidget(self.pushButtonNonValidBack)
        self.pushButtonSaveAnyway = QtGui.QPushButton(missingEntryDialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        self.pushButtonSaveAnyway.setFont(font)
        self.pushButtonSaveAnyway.setObjectName(_fromUtf8("pushButtonSaveAnyway"))
        self.horizontalLayout.addWidget(self.pushButtonSaveAnyway)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(missingEntryDialog)
        QtCore.QMetaObject.connectSlotsByName(missingEntryDialog)

    def retranslateUi(self, missingEntryDialog):
        missingEntryDialog.setWindowTitle(_translate("missingEntryDialog", "Unvollständige Eingabe", None))
        self.pushButtonNonValidBack.setText(_translate("missingEntryDialog", "&Zurück", None))
        self.pushButtonSaveAnyway.setText(_translate("missingEntryDialog", "Trotzdem &speichern", None))

import resources_rc
