import sys
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL
from main_mode import MainMode
from main_window_handler import MainFrame
from edit_mode import EditMode
from dictionaries import LANGUAGE_ENGLISH, LANGUAGE_GERMAN
from handlers import DatabaseHandler
from dialogs import NoDatabaseConnectionDialog


class StartPoint(object):

    def __init__(self):
        self.main_frame = MainFrame()
        self.main_mode = None
        self.edit_mode = None
        self.language_dict = LANGUAGE_GERMAN
        self.main_frame.connect(
            self.main_frame.ui.pushButtonMainMode,
            SIGNAL('clicked()'),
            self.start_main_mode
            )

        self.main_frame.connect(
            self.main_frame.ui.pushButtonEditMode,
            SIGNAL('clicked()'),
            self.start_edit_mode
            )
        self.main_frame.ui.comboBoxLanguage.currentIndexChanged.connect(
            self.language_switch)
        self.database_handler = DatabaseHandler()
        self.dlg = NoDatabaseConnectionDialog(self.main_frame)
        self.dlg.ui.label.setText(self.language_dict['no_database_text'])
        self.dlg.setWindowTitle(self.language_dict['no_database_title'])
        self.dlg.connect(
            self.dlg.ui.pushButtonOfflineMode,
            SIGNAL('clicked()'),
            self.dlg.close
            )
        if self.database_handler.connect_to_database(self.dlg):
            self.no_connection = False
        else:
            self.no_connection = True
            self.main_frame.ui.buttonEditMode.image_button.setPixmap(QtGui.QPixmap('./ui_files/buttonEditDisabled.png'))
            self.main_frame.ui.buttonEditMode.pictures = [
                u'./ui_files/buttonEditDisabled.png',
                u'./ui_files/buttonEditDisabled.png',
                u'./ui_files/buttonEditDisabled.png'
                ]
        self.main_frame.show()

    def start_main_mode(self):
        self.main_mode = MainMode(self.language_dict, self.database_handler, self.no_connection)

    def start_edit_mode(self):
        if not self.no_connection:
            self.edit_mode = EditMode(self.language_dict, self.database_handler)

    def language_switch(self):
        current_text = unicode(
            self.main_frame.ui.comboBoxLanguage.currentText()
            )
        if current_text == 'Deutsch':
            self.language_dict = LANGUAGE_GERMAN
        elif current_text == 'English':
            self.language_dict = LANGUAGE_ENGLISH
        self.main_frame.ui.pushButtonMainMode.setText(self.language_dict['enter'])
        self.main_frame.ui.pushButtonEditMode.setText(self.language_dict['edit'])
        self.dlg.ui.label.setText(self.language_dict['no_database_text'])
        self.dlg.setWindowTitle(self.language_dict['no_database_title'])


APPLICATION = QtGui.QApplication(sys.argv)
CURRENT_POINT = StartPoint()
sys.exit(APPLICATION.exec_())
