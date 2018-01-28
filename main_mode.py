# -*- coding: utf-8 -*-
'''
This module consists of the class representing
the main mode
'''
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, func
from geoalchemy2.elements import WKTElement
import ppygis
from dialogs import (
    MainFrame,
    Calendar,
    UnsuccessfulEntryDialog,
    MissingTransectEndDialog,
    MissingTransectBeginnDialog,
    InvalidKWEntryDialog
    )
from transects import PureTransect, PlanctonTransect, SightTransect
from handlers import set_validators, CheckboxRestrictor, MainModeGuiHandler
from config import OfflineConfiguration
from models import MtPunkte

class MainMode(object):
    '''
    This class represents the main mode
    '''

    def test_if_offline_data(self):
            self.sub_engine = create_engine(OfflineConfiguration.SQLALCHEMY_DATABASE_URI)
            self.sub_connection = self.engine.connect()
            self.sub_meta = MetaData()
            self.sub_points = Table(
                'mt_punkte',
                self.sub_meta,
                autoload=True,
                autoload_with=self.sub_engine)
            result = self.sub_engine.execute(
                select([self.sub_points])).fetchall()
            for res in result:
                if res.laenge != '' and res.breite != '':
                    res.geom = WKTElement(
                        'POINT('
                        + str(res.laenge)
                        + ' '
                        + str(res.breite)
                        + ')',
                        srid=4326
                        )
                else:
                    res.geom = None
                self.send_off_from_local_data_base(res)
            self.sub_engine.execute(self.sub_points.delete())

    def __init__(self, language_dict, databaseHandler, no_connection):
        '''
        Instantiation and setting up all the variables
        '''
        self.main_frame = MainFrame()
        self.language_dict = language_dict
        self.dialogs = {
            'error_message_entry': UnsuccessfulEntryDialog(self.main_frame),
            'main_frame.ui.calendar': Calendar(self.main_frame),
            'missing_transect_beginn_dialog': MissingTransectBeginnDialog(
                self.main_frame),
            'missing_transect_end_dialog': MissingTransectEndDialog(
                self.main_frame),
            'invalid_course_dialog': InvalidKWEntryDialog(self.main_frame)
            }
        self.dialogs[
            'main_frame.ui.calendar'].ui.calendarWidget.setFirstDayOfWeek(1)
        self.gui_handler = MainModeGuiHandler(self.main_frame, self.language_dict)
        self.label_labels()
        set_validators(self.main_frame.ui)
        self.restrict_transect_choices()
        self.dialogs['missing_transect_end_dialog'].delete = False
        self.dialogs['missing_transect_beginn_dialog'].delete = False
        self.__make_own_connections()
        self.no_connection = no_connection
        if self.no_connection:
            self.engine = create_engine(OfflineConfiguration.SQLALCHEMY_DATABASE_URI)
            self.connection = self.engine.connect()
            self.meta = MetaData()
            self.points = Table(
                'mt_punkte',
                self.meta,
                autoload=True,
                autoload_with=self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
        else:
            self.session = databaseHandler.session
            self.engine = databaseHandler.get_engine()
            self.connection = databaseHandler.get_connection()
            self.points = databaseHandler.tables['points']
            self.transects = databaseHandler.tables['transects']
            self.test_if_offline_data()
        frame_handler = CheckboxRestrictor(self.main_frame)
        frame_handler.connect_actions()
        self.main_frame.ui.labelSubTitle.setText(
            self.language_dict['transect_details_title']
            )
        self.main_frame.ui.stackedWidget.setCurrentWidget(
            self.main_frame.ui.page
            )
        self.set_defaults()
        self.set_date_defaults()
        self.main_frame.exec_()

    def label_labels(self):
        self.gui_handler.set_labels()
        self.dialogs['missing_transect_end_dialog'].setWindowTitle(self.language_dict['missing_transect_end_title'])
        self.dialogs['missing_transect_end_dialog'].ui.labelWarnText.setText(self.language_dict['missing_transect_end'])
        self.dialogs['missing_transect_beginn_dialog'].setWindowTitle(self.language_dict['missing_transect_begin_title'])
        self.dialogs['missing_transect_beginn_dialog'].ui.labelWarnText.setText(self.language_dict['missing_transect_begin'])
        self.dialogs['invalid_course_dialog'].setWindowTitle(self.language_dict['invalid_course_turn_title'])
        self.dialogs['invalid_course_dialog'].ui.labelInvalidKWEntry.setText(self.language_dict['invalid_course_turn'])

    def restrict_transect_choices(self):
        '''
        Blocks buttons to call other GUI-frames
        '''
        self.main_frame.ui.pushButtonSendOffSailData.setEnabled(False)
        self.main_frame.ui.pushButtonPlanctonData.setEnabled(False)
        self.main_frame.ui.pushButtonSightData.setEnabled(False)

    def set_date_defaults(self):
        '''
        Sets the GUI-fields representing date and time to default
        '''
        self.gui_handler.set_date_defaults()

    def set_defaults(self):
        '''
        Sets defaults wished by for customer
        '''
        self.gui_handler.set_defaults()

    def set_main_frame_defaults(self):
        '''
        Sets defaults in the main-frame of the GUI
        '''
        self.gui_handler.set_main_frame_defaults()

    def set_main_frame_post_entry(self):
        '''
        Sets defaults in the main-frame of the GUI after an entry was made
        '''
        self.gui_handler.set_main_frame_post_entry()

    def set_plancton_default(self):
        '''
        Sets defaults in the plancton part of the GUI
        '''
        self.gui_handler.set_plancton_default()

    def set_sight_default(self):
        '''
        Sets defaults in the sight part of the GUI
        '''
        self.gui_handler.set_sight_default()

    def set_sight_details_default(self):
        '''
        Sets default in the details part of the sight part of the GUI
        '''
        self.gui_handler.set_sight_details_default()

    def __make_own_connections(self):
        '''
        Sets up all connections between GUI-elements and functions
        '''
        self.main_frame.ui.pushButtonSetFormToDefault.clicked.connect(
            self.set_main_frame_defaults)
        self.main_frame.ui.pushButtonSendOffSailData.clicked.connect(
            self.send_off_sail_data)
        self.main_frame.ui.pushButtonSendOffPlanctonData.clicked.connect(
            self.send_off_plancton_data)
        self.main_frame.ui.pushButtonSendOffSightData.clicked.connect(
            self.send_off_sight_data)
        self.main_frame.ui.pushButtonCalendar.clicked.connect(
            self.__show_calendar)
        self.main_frame.ui.comboBoxTransectID.currentIndexChanged.connect(
            self.transect_chosen)
        self.dialogs[
            'missing_transect_end_dialog'].ui.pushButtonAccept.clicked.connect(
                self.delete_transect_begins)
        self.dialogs[
            'missing_transect_end_dialog'].ui.pushButtonCancel.clicked.connect(
                self.save_redundant_transect_begins)
        self.dialogs[
            'missing_transect_beginn_dialog'
            ].ui.pushButtonAccept.clicked.connect(
                self.delete_redundant_transect_ends)
        self.main_frame.ui.pushButtonPlanctonData.clicked.connect(
            self.plancton_data)
        self.dialogs[
            'invalid_course_dialog'].ui.pushButtonAccept.clicked.connect(
                self.dialogs['invalid_course_dialog'].close)
        self.main_frame.ui.pushButtonSightData.clicked.connect(
            self.sight_data)
        self.main_frame.ui.pushButtonGoToDetailsSight.clicked.connect(
            self.go_to_details_sight)
        self.main_frame.ui.pushButtonSendOffBeforeDetails.clicked.connect(
            self.send_off_sight_data)
        self.main_frame.ui.pushButtonGoBackPlancton.clicked.connect(
            self.go_back_to_main_frame)
        self.main_frame.ui.pushButtonGoBackSight.clicked.connect(
            self.go_back_to_main_frame)
        self.main_frame.ui.pushButtonGoBackSightDetails.clicked.connect(
            self.sight_data)

    def delete_transect_begins(self):
        '''
        Deletes redundant beginnings of a transect
        '''
        self.dialogs['missing_transect_end_dialog'].delete = True
        self.dialogs['missing_transect_end_dialog'].close()

    def save_redundant_transect_begins(self):
        '''
        Saves redundant beginnings of a transect
        '''
        self.dialogs['missing_transect_end_dialog'].delete = False
        self.dialogs['missing_transect_end_dialog'].close()

    def delete_redundant_transect_ends(self):
        '''
        Deletes redundant ends of transect
        '''
        self.dialogs['missing_transect_beginn_dialog'].delete = True
        self.dialogs['missing_transect_beginn_dialog'].close()

    def __show_calendar(self):
        '''
        Brings up the calendar for choosing a date
        '''
        self.dialogs['main_frame.ui.calendar'].show()

    def plancton_data(self):
        '''
        Opens the GUI-frame for plancton
        '''
        self.main_frame.ui.pushButtonSetFormToDefault.clicked.disconnect()
        self.main_frame.ui.pushButtonSetFormToDefault.clicked.connect(
            self.set_plancton_default)
        self.main_frame.ui.stackedWidget.setCurrentWidget(
            self.main_frame.ui.page_2)
        self.main_frame.ui.labelSubTitle.setText(
            self.language_dict['probe_title'])

    def go_back_to_main_frame(self):
        '''
        Opens the main GUI-frame
        '''
        self.main_frame.ui.pushButtonSetFormToDefault.clicked.disconnect()
        self.main_frame.ui.pushButtonSetFormToDefault.clicked.connect(
            self.set_main_frame_defaults)
        self.main_frame.ui.stackedWidget.setCurrentWidget(
            self.main_frame.ui.page)
        self.main_frame.ui.labelSubTitle.setText(self.language_dict['transect_details_title'])

    def sight_data(self):
        '''
        Opens the GUI-frame for sight-data
        '''
        self.main_frame.ui.pushButtonSetFormToDefault.clicked.disconnect()
        self.main_frame.ui.pushButtonSetFormToDefault.clicked.connect(
            self.set_sight_default)
        self.main_frame.ui.stackedWidget.setCurrentWidget(
            self.main_frame.ui.page_3)
        self.main_frame.ui.labelSubTitle.setText(self.language_dict['sight_title'])

    def go_to_details_sight(self):
        '''
        Opens the GUI-frame for details of sight-data
        '''
        self.main_frame.ui.pushButtonSetFormToDefault.clicked.disconnect()
        self.main_frame.ui.pushButtonSetFormToDefault.clicked.connect(
            self.set_sight_details_default)
        self.main_frame.ui.stackedWidget.setCurrentWidget(
            self.main_frame.ui.page_4)
        self.main_frame.ui.labelSubTitle.setText(
            self.language_dict['sight_details_title'])

    def transect_chosen(self):
        '''
        Checks if a transect was chosen in the input field
        '''
        current_text = unicode(
            self.main_frame.ui.comboBoxTransectID.currentText()
            )
        self.restrict_transect_choices()
        if (
                current_text == u'Beginn'
                or current_text == u'Kurswechsel'
                or current_text == u'Ende'
                or current_text == u'Begin'
                or current_text == u'Course Turn'
                or current_text == u'End'):
            self.main_frame.ui.pushButtonSendOffSailData.setEnabled(True)
        elif current_text == u'Probenahme' or current_text == u'sampling':
            self.main_frame.ui.pushButtonPlanctonData.setEnabled(True)
        elif current_text == u'Bitte Auswählen' or current_text == u'Please Choose':
            pass
        else:
            self.main_frame.ui.pushButtonSightData.setEnabled(True)

    def send_off_sail_data(self):
        '''
        Sends of a dataset representing a pure transect to the database
        '''
        dataset = PureTransect(self.main_frame)
        self.__prepare_entry(dataset)
        if self.no_connection:
            self.send_off_sail_data_offline(dataset)
        else:
            if not validate_dataset(dataset):
                return
            if dataset.valid:
                self.send_off_sail_data_abstract(dataset)

    def send_off_sail_data_abstract(self, dataset):
        if dataset.transekt_id == u'B':
            current_highest_index = self.__get_latest_fahrt_id()
            last_transect_end = self.__get_last_transect_end(
                current_highest_index)
            if last_transect_end is None:
                self.dialogs['missing_transect_end_dialog'].exec_()
                if self.dialogs['missing_transect_end_dialog'].delete:
                    self.__delete_old_transect(current_highest_index)
                else:
                    return
            fahrt_id = current_highest_index + 1
            ins = self.transects.insert().values(
                fahrt_id=fahrt_id,
                datum_b=dataset.datum,
                zeit_b=dataset.zeit,
                kurswoche=dataset.kurswoche,
                guide=dataset.guide,
                schiff=dataset.schiff,
                akustik=dataset.akustik
                )
            self.engine.execute(ins)

        elif dataset.transekt_id == u'E':
            current_highest_index = self.__get_latest_fahrt_id()
            last_transect_end = self.__get_last_transect_end(
                current_highest_index)
            if last_transect_end is not None:
                self.dialogs['missing_transect_beginn_dialog'].exec_()
                return
            else:
                fahrt_id = current_highest_index
            begin_transect = self.engine.execute(
                select([self.points]).where(
                    self.points.c.fahrt_id == fahrt_id)).fetchone()
            result = self.engine.execute(
                select([self.points]).where(
                    self.points.c.fahrt_id == fahrt_id
                    ).where(
                        self.points.c.transekt_id == 'KW '))
            polyline = []
            point = ppygis.Point(begin_transect.laenge, begin_transect.breite, srid=4326)
            polyline.append(point)
            for row in result:
                point = ppygis.Point(row.laenge, row.breite, srid=4326)
                polyline.append(point)
            point = ppygis.Point(dataset.laenge, dataset.breite, srid=4326)
            linestring = ppygis.LineString(polyline, srid=4326)
            fahrt_id = current_highest_index
            self.connection.execute(
                self.transects.update()
                .where(self.transects.c.fahrt_id
                       == fahrt_id)
                .values(datum_e=dataset.datum,
                        zeit_e=dataset.zeit, geom=linestring))

        elif dataset.transekt_id == 'KW':
            fahrt_id = self.__get_latest_fahrt_id()
            last_transect_end = self.__get_last_transect_end(
                fahrt_id)
            if last_transect_end is not None:
                self.dialogs['invalid_course_dialog'].exec_()
                return
        result = self.engine.execute(
            select([func.max(self.points.c.punkt_id)]))
        for row in result:
            punkt_id = row[0] + 1
        ins = self.points.insert().values(
            punkt_id=punkt_id,
            fahrt_id=fahrt_id,
            transekt_id=dataset.transekt_id,
            sicht_id=dataset.sicht_id,
            bewoelkung_id=dataset.bewoelkung_id,
            windrichtung_id=dataset.windrichtung_id,
            wind_id=dataset.wind_id,
            meer_id=dataset.meer_id,
            kurs=dataset.kurs,
            kurswoche=dataset.kurswoche,
            breite=dataset.breite,
            laenge=dataset.laenge,
            schiff=dataset.schiff,
            guide=dataset.guide,
            segel=dataset.segel,
            akustik=dataset.akustik,
            militaer=dataset.militaer,
            zeit=dataset.zeit,
            datum=dataset.datum,
            fotos=dataset.fotos,
            aufnahme=dataset.aufnahme
            )
        self.engine.execute(ins)
        self.set_main_frame_post_entry()

    def send_off_plancton_data(self):
        '''
        Sends off a dataset representing a plancton-transect
        to the database
        '''
        dataset = PlanctonTransect(self.main_frame)
        if self.no_connection:
            self.__prepare_entry(dataset)
            self.send_off_plancton_data_offline(dataset)
        else:
            if not validate_dataset(dataset):
                return
            if dataset.valid:
                self.__prepare_entry(dataset)
                self.send_off_plancton_data_abstract(dataset)

    def send_off_plancton_data_abstract(self, dataset):
        result = self.engine.execute(
            select([func.max(self.transects.c.fahrt_id)])).fetchone()
        result = self.engine.execute(
            select([self.transects]).where(
                self.transects.c.fahrt_id == result[0])
            ).fetchone()
        if result[2] is None:
            fahrt_id = result.fahrt_id
        else:
            fahrt_id = None
        result = self.engine.execute(
            select([func.max(self.points.c.punkt_id)]))
        for row in result:
            punkt_id = row[0] + 1
        ins = self.points.insert().values(
            punkt_id=punkt_id,
            fahrt_id=fahrt_id,
            transekt_id=dataset.transekt_id,
            sicht_id=dataset.sicht_id,
            bewoelkung_id=dataset.bewoelkung_id,
            windrichtung_id=dataset.windrichtung_id,
            wind_id=dataset.wind_id,
            meer_id=dataset.meer_id,
            kurs=dataset.kurs,
            kurswoche=dataset.kurswoche,
            breite=dataset.breite,
            laenge=dataset.laenge,
            schiff=dataset.schiff,
            guide=dataset.guide,
            segel=dataset.segel,
            akustik=dataset.akustik,
            militaer=dataset.militaer,
            zeit=dataset.zeit,
            datum=dataset.datum,
            fotos=dataset.fotos,
            aufnahme=dataset.aufnahme,
            temperatur=dataset.temperatur,
            salinitaet=dataset.salinitaet,
            sichttiefe=dataset.sichttiefe,
            wasserprobe=dataset.wasserprobe,
            zooplanktonprobe=dataset.zooplanktonprobe,
            phytoplanktonprobe=dataset.phytoplanktonprobe
            )
        self.engine.execute(ins)
        self.set_main_frame_post_entry()
        self.set_plancton_default()
        self.go_back_to_main_frame()

    def send_off_sight_data(self):
        '''
        Sends off a dataset representing a sigh-transect
        to the database
        '''
        dataset = SightTransect(self.main_frame)
        if self.no_connection:
            self.__prepare_entry(dataset)
            self.send_off_sight_data_offline(dataset)
        else:
            if not validate_dataset(dataset):
                return
            if dataset.valid:
                self.__prepare_entry(dataset)
                self.send_off_sight_data_abstract(dataset)

    def send_off_from_local_data_base(self, dataset):
        if dataset.transekt_id == 'KW' or dataset.transekt_id == 'B' or dataset.transekt_id == 'E':
            self.send_off_sail_data_abstract(dataset)
        elif dataset.transekt_id == 'AA':
            self.send_off_plancton_data_abstract(dataset)
        else:
            self.send_off_sight_data_abstract(dataset)

    def send_off_sight_data_abstract(self, dataset):
        result = self.engine.execute(
            select([func.max(self.transects.c.fahrt_id)])).fetchone()
        current_highest_id = result[0]
        result = self.engine.execute(
            select([self.transects.c.datum_b]).where(
                self.transects.c.fahrt_id == current_highest_id
                )).fetchone()
        if result is None:
            fahrt_id = current_highest_id
        else:
            fahrt_id = None
        result = self.engine.execute(
            select([func.max(self.points.c.punkt_id)]))
        for row in result:
            punkt_id = row[0] + 1
        ins = self.points.insert().values(
            punkt_id=punkt_id,
            fahrt_id=fahrt_id,
            transekt_id=dataset.transekt_id,
            sicht_id=dataset.sicht_id,
            bewoelkung_id=dataset.bewoelkung_id,
            windrichtung_id=dataset.windrichtung_id,
            wind_id=dataset.wind_id,
            meer_id=dataset.meer_id,
            kurs=dataset.kurs,
            kurswoche=dataset.kurswoche,
            breite=dataset.breite,
            laenge=dataset.laenge,
            schiff=dataset.schiff,
            guide=dataset.guide,
            segel=dataset.segel,
            akustik=dataset.akustik,
            militaer=dataset.militaer,
            zeit=dataset.zeit,
            datum=dataset.datum,
            fotos=dataset.fotos,
            aufnahme=dataset.aufnahme,
            temperatur=dataset.temperatur,
            salinitaet=dataset.salinitaet,
            sichttiefe=dataset.sichttiefe,
            ruhend=dataset.ruhend,
            langsam=dataset.langsam,
            schnell=dataset.schnell,
            richtung_wechselnd=dataset.richtung_wechselnd,
            richtung_konstant=dataset.richtung_konstant,
            nahrungsaufnahme=dataset.nahrungsaufnahme,
            tauchgang=dataset.tauchgang,
            fluke_sichtbar=dataset.fluke_sichtbar,
            spy_hopping=dataset.spy_hopping,
            flukenschlagen=dataset.flukenschlagen,
            paarung=dataset.paarung,
            spiel=dataset.spiel,
            annaeherung=dataset.annaeherung,
            lautgebung=dataset.lautgebung,
            blas=dataset.blas,
            in_begleitung=dataset.in_begleitung,
            spruenge=dataset.spruenge,
            breach_seitlich=dataset.breach_seitlich,
            breach_rueckwaerts=dataset.breach_rueckwaerts,
            jungtiere=dataset.jungtiere,
            kaelber=dataset.kaelber,
            neugeborene=dataset.neugeborene,
            schwimmen_nah=dataset.schwimmen_nah,
            bugwellen=dataset.bugwellen,
            seitlich=dataset.seitlich,
            heckwellen=dataset.heckwellen,
            unter_schiff=dataset.unter_schiff,
            soziales_verhalten=dataset.soziales_verhalten,
            gruppe_kompakt=dataset.gruppe_kompakt,
            gruppe_locker=dataset.gruppe_locker,
            art_id=dataset.art_id,
            anzahl_min=dataset.anzahl_min,
            anzahl_max=dataset.anzahl_max,
            kurs_wal=dataset.kurs_wal,
            position_wal=dataset.position_wal,
            distanz_p=dataset.distanz_p,
            distanz_m=dataset.distanz_m,
            begleitende_spezies=dataset.begleitende_spezies,
            blasfrequenz=dataset.blasfrequenz,
            anzahl_jungtiere=dataset.anzahl_jungtiere,
            anderes_verhalten=dataset.anderes_verhalten,
            zusaetzliche_beobachtungen=dataset.zusaetzliche_beobachtungen,
            dauer=dataset.dauer,
            breite_wal=dataset.breite_wal,
            laenge_wal=dataset.laenge_wal,
            sichtungswinkel=dataset.sichtungswinkel
            )
        self.engine.execute(ins)
        self.set_sight_details_default()
        self.set_sight_default()
        self.set_main_frame_post_entry()
        self.go_back_to_main_frame()

    def __prepare_entry(self, dataset):
        '''
        Prepare a dataset for entry into database
        '''
        dataset.prepare_for_entry()
        result = self.engine.execute(
            select([func.max(self.points.c.punkt_id)]))
        if result.rowcount == -1:
            dataset.punkt_id = 1
        else:
            for row in result:
                dataset.punkt_id = row[0] + 1

    def __get_latest_fahrt_id(self):
        '''
        Returns the latest fahrt_id used for inserting
        and deleting transects into the db
        '''
        return self.engine.execute(
            select(
                [func.max(self.transects.c.fahrt_id)]
                )).fetchone()[0]

    def __get_last_transect_end(self, current_highest_index):
        '''
        Returns the latest end of a transect, used
        for determining validness for transects
        '''
        return self.engine.execute(
            select([self.transects.c.datum_e])
            .where(
                self.transects.c.fahrt_id == current_highest_index
                )
            ).fetchone()[0]

    def __delete_old_transect(self, fahrt_id):
        '''
        Deletes transect with fahrt_id 'fahrt_id' and updates all
        rows associated with it
        '''
        result = self.engine.execute(
            select([self.points]).where(
                self.points.c.fahrt_id == fahrt_id
            ))
        for row in result:
            if (row.transekt_id == 'B  '
                    or row.transekt_id == 'KW '):
                self.connection.execute(
                    self.points.delete().
                    where(self.points.c.punkt_id
                          == row.punkt_id))
            if row.transekt_id == 'Ak ':
                self.connection.execute(
                    self.points.update()
                    .where(self.points.c.fahrt_id
                           == fahrt_id)
                    .values(transekt_id='Ako')
                    )
            elif row.transekt_id == 'S  ':
                self.connection.execute(
                    self.points.update()
                    .where(self.points.c.fahrt_id
                           == fahrt_id)
                    .values(transekt_id='A  '))
            self.connection.execute(
                self.points.update()
                .where(self.points.c.fahrt_id
                       == fahrt_id)
                .values(fahrt_id=None))
            self.connection.execute(
                self.transects.delete()
                .where(self.transects.c.fahrt_id
                       == fahrt_id))
            self.connection.execute(
                self.points.delete()
                .where(self.points.c.fahrt_id
                       == fahrt_id)
                .where(self.points.c.transekt_id == 'B  ')
                )

    def send_off_sail_data_offline(self, dataset):
        ins = self.points.insert().values(
            transekt_id=dataset.transekt_id,
            sicht_id=dataset.sicht_id,
            bewoelkung_id=dataset.bewoelkung_id,
            windrichtung_id=dataset.windrichtung_id,
            wind_id=dataset.wind_id,
            meer_id=dataset.meer_id,
            kurs=dataset.kurs,
            kurswoche=dataset.kurswoche,
            breite=dataset.breite,
            laenge=dataset.laenge,
            schiff=dataset.schiff,
            guide=dataset.guide,
            segel=dataset.segel,
            akustik=dataset.akustik,
            militaer=dataset.militaer,
            zeit=dataset.zeit,
            datum=dataset.datum,
            fotos=dataset.fotos,
            aufnahme=dataset.aufnahme
            )
        self.engine.execute(ins)
        self.set_main_frame_post_entry()

    def send_off_plancton_data_offline(self, dataset):
        ins = self.points.insert().values(
            transekt_id=dataset.transekt_id,
            sicht_id=dataset.sicht_id,
            bewoelkung_id=dataset.bewoelkung_id,
            windrichtung_id=dataset.windrichtung_id,
            wind_id=dataset.wind_id,
            meer_id=dataset.meer_id,
            kurs=dataset.kurs,
            kurswoche=dataset.kurswoche,
            breite=dataset.breite,
            laenge=dataset.laenge,
            schiff=dataset.schiff,
            guide=dataset.guide,
            segel=dataset.segel,
            akustik=dataset.akustik,
            militaer=dataset.militaer,
            zeit=dataset.zeit,
            datum=dataset.datum,
            fotos=dataset.fotos,
            aufnahme=dataset.aufnahme,
            temperatur=dataset.temperatur,
            salinitaet=dataset.salinitaet,
            sichttiefe=dataset.sichttiefe,
            wasserprobe=dataset.wasserprobe,
            zooplanktonprobe=dataset.zooplanktonprobe,
            phytoplanktonprobe=dataset.phytoplanktonprobe
            )
        self.engine.execute(ins)
        self.set_main_frame_post_entry()
        self.set_plancton_default()
        self.go_back_to_main_frame()

    def send_off_sight_data_offline(self, dataset):
        ins = self.points.insert().values(
            transekt_id=dataset.transekt_id,
            sicht_id=dataset.sicht_id,
            bewoelkung_id=dataset.bewoelkung_id,
            windrichtung_id=dataset.windrichtung_id,
            wind_id=dataset.wind_id,
            meer_id=dataset.meer_id,
            kurs=dataset.kurs,
            kurswoche=dataset.kurswoche,
            breite=dataset.breite,
            laenge=dataset.laenge,
            schiff=dataset.schiff,
            guide=dataset.guide,
            segel=dataset.segel,
            akustik=dataset.akustik,
            militaer=dataset.militaer,
            zeit=dataset.zeit,
            datum=dataset.datum,
            fotos=dataset.fotos,
            aufnahme=dataset.aufnahme,
            temperatur=dataset.temperatur,
            salinitaet=dataset.salinitaet,
            sichttiefe=dataset.sichttiefe,
            ruhend=dataset.ruhend,
            langsam=dataset.langsam,
            schnell=dataset.schnell,
            richtung_wechselnd=dataset.richtung_wechselnd,
            richtung_konstant=dataset.richtung_konstant,
            nahrungsaufnahme=dataset.nahrungsaufnahme,
            tauchgang=dataset.tauchgang,
            fluke_sichtbar=dataset.fluke_sichtbar,
            spy_hopping=dataset.spy_hopping,
            flukenschlagen=dataset.flukenschlagen,
            paarung=dataset.paarung,
            spiel=dataset.spiel,
            annaeherung=dataset.annaeherung,
            lautgebung=dataset.lautgebung,
            blas=dataset.blas,
            in_begleitung=dataset.in_begleitung,
            spruenge=dataset.spruenge,
            breach_seitlich=dataset.breach_seitlich,
            breach_rueckwaerts=dataset.breach_rueckwaerts,
            jungtiere=dataset.jungtiere,
            kaelber=dataset.kaelber,
            neugeborene=dataset.neugeborene,
            schwimmen_nah=dataset.schwimmen_nah,
            bugwellen=dataset.bugwellen,
            seitlich=dataset.seitlich,
            heckwellen=dataset.heckwellen,
            unter_schiff=dataset.unter_schiff,
            soziales_verhalten=dataset.soziales_verhalten,
            gruppe_kompakt=dataset.gruppe_kompakt,
            gruppe_locker=dataset.gruppe_locker,
            art_id=dataset.art_id,
            anzahl_min=dataset.anzahl_min,
            anzahl_max=dataset.anzahl_max,
            kurs_wal=dataset.kurs_wal,
            position_wal=dataset.position_wal,
            distanz_p=dataset.distanz_p,
            distanz_m=dataset.distanz_m,
            begleitende_spezies=dataset.begleitende_spezies,
            blasfrequenz=dataset.blasfrequenz,
            anzahl_jungtiere=dataset.anzahl_jungtiere,
            anderes_verhalten=dataset.anderes_verhalten,
            zusaetzliche_beobachtungen=dataset.zusaetzliche_beobachtungen,
            dauer=dataset.dauer,
            breite_wal=dataset.breite_wal,
            laenge_wal=dataset.laenge_wal,
            sichtungswinkel=dataset.sichtungswinkel
            )
        self.engine.execute(ins)
        self.set_sight_details_default()
        self.set_sight_default()
        self.set_main_frame_post_entry()
        self.go_back_to_main_frame()


def validate_dataset(dataset):
    '''
    Validates a dataset before putting it into
    the dataset
    '''
    dataset.evaluate()
    if dataset.missing_entries:
        dataset.instantiate_missing_entry_dialog()
        if dataset.go_back:
            return False
    if dataset.non_valid_entries:
        dataset.instantiate_invalid_entries_dialog()
    return True
