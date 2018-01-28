'''
This class serves as a handler for the GUI of the main-menu
of the application. It includes a custom-made widget 'SpecialLabel'
'''
from compiled_ui_files.mainWindow import Ui_MainWindowMedCet
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QPixmap, QWidget, QLabel, QMainWindow


class MainFrame(QMainWindow):
    '''
    Handler for the GUI of the main-menu
    '''
    def __init__(self):
        '''
        Instantiation of the GUI
        '''
        QMainWindow.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_MainWindowMedCet()
        self.ui.setupUi(self)
        pictures_main_mode = [
            u'./ui_files/buttonMainModeUnclicked.png',
            u'./ui_files/buttonMainModeHover.png',
            u'./ui_files/buttonMainModeClicked.png'
            ]
        self.ui.buttonMainMode = SpecialLabel(self, pictures_main_mode)
        pictures_edit_mode = [
            u'./ui_files/buttonEditModeUnclicked.png',
            u'./ui_files/buttonEditModeHover.png',
            u'./ui_files/buttonEditModeClicked.png'
            ]
        self.ui.buttonEditMode = SpecialLabel(self, pictures_edit_mode)

        self.ui.gridLayout.addWidget(self.ui.buttonMainMode, 0, 1)
        self.ui.gridLayout.addWidget(self.ui.buttonEditMode, 0, 3)


class SpecialLabel(QWidget):
    '''
    This custom-made Widget is basically a button consisting of a clickable
    image, which fires a QEvent, something that PyQt4 does not support, might
    get supported in later versions
    '''
    def __init__(self, parent, pictures):
        '''
        Initialisation, it takes an array of three images, one for the states
        hover, unpressed and pressed
        '''
        QWidget.__init__(self, parent)
        self.paint = pictures
        self.resize(100, 100)
        self.setMinimumSize(100, 100)
        self.pictures = pictures
        self.image_button = None
        self.initButton()

    def initButton(self):
        '''
        Initialisation of the button-functionality
        '''
        self.image_button = ExtendedQLabel(self)
        self.image_button.move(0, 0)
        self.image_button.setPixmap(QPixmap(self.pictures[0]))

    def enterEvent(self, ev):
        '''
        On entering widget frame, change image
        '''
        self.image_button.setPixmap(QPixmap(self.pictures[1]))

    def leaveEvent(self, ev):
        '''
        On leaving widget frame, change image
        '''
        self.image_button.setPixmap(QPixmap(self.pictures[0]))

    def mousePressEvent(self, ev):
        '''
        On mouse-press, change image
        '''
        self.image_button.setPixmap(QPixmap(self.pictures[2]))


class ExtendedQLabel(QLabel):
    '''
    Custom widget that inherits from QLabel, but adds an 'on-click'
    event
    '''
    def __init(self, parent):
        '''
        Initialization
        '''
        QLabel.__init__(self, parent)

    def mouseReleaseEvent(self, ev):
        '''
        Adds the click-event
        '''
        self.emit(SIGNAL('clicked()'))
