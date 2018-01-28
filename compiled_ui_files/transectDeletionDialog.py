# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'transectDeletionDialog.ui'
#
# Created: Fri Mar 21 08:18:10 2014
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

class Ui_TransectDeletionDialog(object):
    def setupUi(self, TransectDeletionDialog):
        TransectDeletionDialog.setObjectName(_fromUtf8("TransectDeletionDialog"))
        TransectDeletionDialog.resize(389, 192)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        TransectDeletionDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TransectDeletionDialog.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(TransectDeletionDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 14, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.labelTransectDeletion = QtGui.QLabel(TransectDeletionDialog)
        self.labelTransectDeletion.setWordWrap(True)
        self.labelTransectDeletion.setObjectName(_fromUtf8("labelTransectDeletion"))
        self.verticalLayout.addWidget(self.labelTransectDeletion)
        spacerItem1 = QtGui.QSpacerItem(20, 14, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pushButtonCancel = QtGui.QPushButton(TransectDeletionDialog)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonDelete = QtGui.QPushButton(TransectDeletionDialog)
        self.pushButtonDelete.setObjectName(_fromUtf8("pushButtonDelete"))
        self.horizontalLayout.addWidget(self.pushButtonDelete)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(TransectDeletionDialog)
        QtCore.QMetaObject.connectSlotsByName(TransectDeletionDialog)

    def retranslateUi(self, TransectDeletionDialog):
        TransectDeletionDialog.setWindowTitle(_translate("TransectDeletionDialog", "Transektlöschung", None))
        self.labelTransectDeletion.setText(_translate("TransectDeletionDialog", "Dieser Eintrag ist Teil einer Transektdefinition. Wenn er gelöscht wird, werden die entsprechenden Beginn-, Kurswechsel- und Endeinträge gelöscht. Bei allen anderen Einträgen, die diesen Transekt referenzieren, wird diese Referenz gelöscht. Dies hat zur Folge, dass eine Sichtung zur Fremdsichtung wird und so weiter.", None))
        self.pushButtonCancel.setText(_translate("TransectDeletionDialog", "Abbrechen", None))
        self.pushButtonDelete.setText(_translate("TransectDeletionDialog", "Löschen", None))

import resources_rc
