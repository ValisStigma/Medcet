# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calender.ui'
#
# Created: Fri Feb 28 09:24:08 2014
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

class Ui_CalendarDialog(object):
    def setupUi(self, CalendarDialog):
        CalendarDialog.setObjectName(_fromUtf8("CalendarDialog"))
        CalendarDialog.resize(330, 180)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(10)
        CalendarDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logos/logo_oceancare_2.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CalendarDialog.setWindowIcon(icon)
        self.horizontalLayout = QtGui.QHBoxLayout(CalendarDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.calendarWidget = DoubleCalendar(CalendarDialog)
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.horizontalLayout.addWidget(self.calendarWidget)

        self.retranslateUi(CalendarDialog)
        QtCore.QMetaObject.connectSlotsByName(CalendarDialog)

    def retranslateUi(self, CalendarDialog):
        CalendarDialog.setWindowTitle(_translate("CalendarDialog", "Datumwahl", None))

class DoubleCalendar(QtGui.QCalendarWidget):
    def __init__(self, parent):
        QtGui.QCalendarWidget.__init__(self, parent)
        self.parent = parent
    def mouseDoubleClickEvent(self, ev):
        self.parent().parent().ui.dateEdit.setDate(self.ui.calendarWidget.selectedDate())
        self.parent.close()
        print 'jhaha'
import resources_rc
