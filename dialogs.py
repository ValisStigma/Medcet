#!/usr/local/bin/python2.7
# encoding: utf-8

from PyQt4 import QtGui
from compiled_ui_files.noDataBaseConnection import Ui_NoDatabaseConnectionDialog
from compiled_ui_files.calender import Ui_CalendarDialog
from compiled_ui_files.nonValidEntry import Ui_nonValidEntryDialog
from compiled_ui_files.missingEntry import Ui_missingEntryDialog
from compiled_ui_files.unsuccesfullEntry import Ui_UnsuccesfulEntryDialog
from compiled_ui_files.mainModeDialog import Ui_MainModeDialog
from compiled_ui_files.missingTransectBeginn import Ui_MissingTransectBeginnDialog
from compiled_ui_files.missingTransectEnd import Ui_MissingTransectEndDialog
from compiled_ui_files.invalidKWEntry import Ui_InvalidKWEntryDialog
from compiled_ui_files.editFrameDialog import Ui_EditModeDialog
from compiled_ui_files.deleteEntry import Ui_DeletionsDialog
from compiled_ui_files.warn import Ui_WarnDialog
from compiled_ui_files.transectDeletionDialog import Ui_TransectDeletionDialog


class MainFrame(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_MainModeDialog()
        self.ui.setupUi(self)


class NoDatabaseConnectionDialog(QtGui.QDialog):
    def __init__(self, mainFrame):
        QtGui.QDialog.__init__(self, mainFrame)
        # Set up the user interface from Designer.
        self.ui = Ui_NoDatabaseConnectionDialog()
        self.ui.setupUi(self)
        self.parent = mainFrame

    def closeEvent(self, event):
        '''
        Overwriting of close event
        '''
        self.parent.close()


class Calendar(QtGui.QDialog):
    '''
    Calendar GUI-window for date-picking
    '''
    def __init__(self, mainFrame):
        QtGui.QDialog.__init__(self, mainFrame)
        # Set up the user interface from Designer.
        self.ui = Ui_CalendarDialog()
        self.ui.setupUi(self)
        self.parent = mainFrame

    def closeEvent(self, event):
        '''
        Overwriting of close event
        '''
        self.parent.ui.dateEdit.setDate(self.ui.calendarWidget.selectedDate())

    def mouseDoubleClickEvent(self, event):
        '''
        Overwriting of double-click event
        '''
        self.parent.ui.dateEdit.setDate(self.ui.calendarWidget.selectedDate())
        self.close()


class NonValidEntryDialog(QtGui.QDialog):
    def __init__(self, parent, transect):
        QtGui.QDialog.__init__(self, parent)
        # Set up the user interface from Designer.
        self.ui = Ui_nonValidEntryDialog()
        self.ui.setupUi(self)
        self.transect = transect

    def closeEvent(self, event):
        self.transect.valid = False
        event.accept()


class MissingEntryDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        # Set up the user interface from Designer.
        self.ui = Ui_missingEntryDialog()
        self.ui.setupUi(self)


class UnsuccessfulEntryDialog(QtGui.QDialog):
    def __init__(self, mainFrame):
        QtGui.QDialog.__init__(self, mainFrame)
        # Set up the user interface from Designer.
        self.ui = Ui_UnsuccesfulEntryDialog()
        self.ui.setupUi(self)


class MissingTransectBeginnDialog(QtGui.QDialog):
    def __init__(self, mainFrame):
        QtGui.QDialog.__init__(self, mainFrame)
        self.ui = Ui_MissingTransectBeginnDialog()
        self.ui.setupUi(self)


class MissingTransectEndDialog(QtGui.QDialog):
    def __init__(self, mainFrame):
        QtGui.QDialog.__init__(self, mainFrame)
        self.ui = Ui_MissingTransectEndDialog()
        self.ui.setupUi(self)


class InvalidKWEntryDialog(QtGui.QDialog):
    def __init__(self, mainFrame):
        QtGui.QDialog.__init__(self, mainFrame)
        self.ui = Ui_InvalidKWEntryDialog()
        self.ui.setupUi(self)


class EditFrame(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_EditModeDialog()
        self.ui.setupUi(self)


class DeleteEntryDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_DeletionsDialog()
        self.ui.setupUi(self)


class WarnDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_WarnDialog()
        self.ui.setupUi(self)


class TransectDeletionDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_TransectDeletionDialog()
        self.ui.setupUi(self)
