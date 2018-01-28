# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'noDataBaseConnection.ui'
#
# Created: Fri Sep  5 16:18:04 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_NoDatabaseConnectionDialog(object):
    def setupUi(self, NoDatabaseConnectionDialog):
        NoDatabaseConnectionDialog.setObjectName(_fromUtf8("NoDatabaseConnectionDialog"))
        NoDatabaseConnectionDialog.resize(351, 139)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        NoDatabaseConnectionDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NoDatabaseConnectionDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(NoDatabaseConnectionDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtGui.QLabel(NoDatabaseConnectionDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonOfflineMode = QtGui.QPushButton(NoDatabaseConnectionDialog)
        self.pushButtonOfflineMode.setObjectName(_fromUtf8("pushButtonOfflineMode"))
        self.horizontalLayout.addWidget(self.pushButtonOfflineMode)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(NoDatabaseConnectionDialog)
        QtCore.QMetaObject.connectSlotsByName(NoDatabaseConnectionDialog)

    def retranslateUi(self, NoDatabaseConnectionDialog):
        NoDatabaseConnectionDialog.setWindowTitle(_translate("NoDatabaseConnectionDialog", "Keine Verbindung zur Datenbank", None))
        self.label.setText(_translate("NoDatabaseConnectionDialog", "Leider ist die Verbindung zur Datenbank fehlgeschlagen.", None))
        self.pushButtonOfflineMode.setText(_translate("NoDatabaseConnectionDialog", "Ok", None))

import resources_rc
