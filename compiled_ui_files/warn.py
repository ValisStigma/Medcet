# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'warn.ui'
#
# Created: Thu Mar 06 07:53:39 2014
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

class Ui_WarnDialog(object):
    def setupUi(self, WarnDialog):
        WarnDialog.setObjectName(_fromUtf8("WarnDialog"))
        WarnDialog.resize(449, 112)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        WarnDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        WarnDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(WarnDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 6, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(WarnDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(20, 6, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonAbortWarn = QtGui.QPushButton(WarnDialog)
        self.pushButtonAbortWarn.setMinimumSize(QtCore.QSize(137, 40))
        self.pushButtonAbortWarn.setObjectName(_fromUtf8("pushButtonAbortWarn"))
        self.horizontalLayout.addWidget(self.pushButtonAbortWarn)
        self.pushButtonSaveAndOnWarn = QtGui.QPushButton(WarnDialog)
        self.pushButtonSaveAndOnWarn.setObjectName(_fromUtf8("pushButtonSaveAndOnWarn"))
        self.horizontalLayout.addWidget(self.pushButtonSaveAndOnWarn)
        self.pushButtonOnWarn = QtGui.QPushButton(WarnDialog)
        self.pushButtonOnWarn.setMinimumSize(QtCore.QSize(137, 40))
        self.pushButtonOnWarn.setObjectName(_fromUtf8("pushButtonOnWarn"))
        self.horizontalLayout.addWidget(self.pushButtonOnWarn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(WarnDialog)
        QtCore.QMetaObject.connectSlotsByName(WarnDialog)

    def retranslateUi(self, WarnDialog):
        WarnDialog.setWindowTitle(_translate("WarnDialog", "Änderungen vorhanden", None))
        self.label.setText(_translate("WarnDialog", "Dieser Eintrag wurde verändert. Wollen Sie wirklich fortfahren?", None))
        self.pushButtonAbortWarn.setText(_translate("WarnDialog", "&Abbrechen", None))
        self.pushButtonSaveAndOnWarn.setText(_translate("WarnDialog", "Änderungen &speichern \n"
"und weiter", None))
        self.pushButtonOnWarn.setText(_translate("WarnDialog", "&Ja", None))

import resources_rc
