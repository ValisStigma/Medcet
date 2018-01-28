# -*- coding: utf-8 -*-
'''
This class handles editing mode
'''
from PyQt4.QtCore import QDate, QTime, QVariant, Qt
from sqlalchemy.sql import select, func
from geoalchemy2.elements import WKTElement
from dialogs import (
    Calendar,
    UnsuccessfulEntryDialog,
    EditFrame,
    DeleteEntryDialog,
    WarnDialog,
    TransectDeletionDialog
    )
from handlers import set_validators, CheckboxRestrictor, EditGuiHander
from transects import PureTransect, PlanctonTransect, SightTransect
from dictionaries import (
    DICT_SEA, DICT_WIND, DICT_WIND_DIRECTION, DICT_SPECIES, DICT_TRANSECT_ID)
from models import MtPunkte

MT_FAHRTEN_IDS = ['B  ', 'KW ', 'E  ']
TT_OTHERS_IDS = ['AA ', 'WB ', 'W  ']


class EditMode(object):
    '''
    This class handles editing mode
    '''
    def __init__(self, language_dict, database_handler):
        self.edit_frame = EditFrame()
        self.language_dict = language_dict
        self.current_row_absolut = -1
        self.current_row_in_database = -1
        self.number_of_entries = 0
        self.current_row = None
        self.dialogs = {
            'error_message_entry': UnsuccessfulEntryDialog(self.edit_frame),
            'calendar': Calendar(self.edit_frame),
            'transect_deletion_dialog': TransectDeletionDialog(self.edit_frame),
            'unsuccessful_entry_dialog': UnsuccessfulEntryDialog(
                self.edit_frame),
            'delete_dialog': DeleteEntryDialog(self.edit_frame),
            'warn_dialog':  WarnDialog(self.edit_frame)
            }
        self.booleans = {
            'values_have_changed': False,
            'next_entry_button_pushed': False,
            'predecent_entry_button_pushed': False
            }
        self.gui_handler = EditGuiHander(self.edit_frame, self.language_dict)
        self.label_labels()
        self.dialogs['calendar'].ui.calendarWidget.setFirstDayOfWeek(1)
        set_validators(self.edit_frame.ui)
        self.__make_own_connections()
        self.engine = database_handler.get_engine()
        self.connection = database_handler.get_connection()
        self.points = database_handler.tables['points']
        self.transects = database_handler.tables['transects']
        self.tt_observations = database_handler.tables['tt_observations']
        self.tt_others = database_handler.tables['tt_others']
        self.session = database_handler.session
        frame_handler = CheckboxRestrictor(self.edit_frame)
        frame_handler.connect_actions()
        self.__initialize_with_newest_entry()
        self.edit_frame.ui.labelSubTitle.setText(u'Transektdetails')
        self.edit_frame.ui.stackedWidget.setCurrentWidget(
            self.edit_frame.ui.page)
        self.edit_frame.exec_()

    def label_labels(self):
        self.gui_handler.set_labels()
        self.dialogs['transect_deletion_dialog'].setWindowTitle(self.language_dict['transect_delete_title'])
        self.dialogs['transect_deletion_dialog'].ui.labelTransectDeletion.setText(self.language_dict['transect_delete'])
        self.dialogs['delete_dialog'].setWindowTitle(self.language_dict['delete_entry_title'])
        self.dialogs['delete_dialog'].ui.label.setText(self.language_dict['delete_entry'])
        self.dialogs['warn_dialog'].setWindowTitle(self.language_dict['warn_title'])
        self.dialogs['warn_dialog'].ui.label.setText(self.language_dict['warn'])
        self.dialogs['warn_dialog'].ui.pushButtonOnWarn.setText(self.language_dict['yes'])
        self.dialogs['warn_dialog'].ui.pushButtonAbortWarn.setText(self.language_dict['abort'])
        self.dialogs['warn_dialog'].ui.pushButtonSaveAndOnWarn.setText(self.language_dict['yes_save'])

    def plancton_data(self):
        '''
        Switches GUI-frame to plancton part
        '''
        self.enable_browsing(False)
        self.edit_frame.ui.stackedWidget.setCurrentWidget(
            self.edit_frame.ui.page_2)
        self.edit_frame.ui.labelSubTitle.setText(self.language_dict['probe_title'])

    def go_back_to_start(self):
        '''
        Switches GUI-frame back to start
        '''
        self.enable_browsing(True)
        self.edit_frame.ui.stackedWidget.setCurrentWidget(
            self.edit_frame.ui.page)
        self.edit_frame.ui.labelSubTitle.setText(self.language_dict['transect_details_title'])

    def enable_browsing(self, boolean):
        self.edit_frame.ui.pushButtonNextEntry.setEnabled(boolean)
        self.edit_frame.ui.pushButtonPredecentEntry.setEnabled(boolean)

    def sight_data(self):
        '''
        Switches GUI-frame to sight part
        '''
        self.enable_browsing(False)
        self.edit_frame.ui.stackedWidget.setCurrentWidget(
            self.edit_frame.ui.page_3)
        self.edit_frame.ui.labelSubTitle.setText(self.language_dict['sight_title'])

    def go_to_details_sight(self):
        '''
        Switches GUI-frame to details part
        '''
        self.enable_browsing(False)
        self.edit_frame.ui.stackedWidget.setCurrentWidget(
            self.edit_frame.ui.page_4)
        self.edit_frame.ui.labelSubTitle.setText(self.language_dict['Transektdetails > Sichtung > Sichtungsdetails'])

    def __set_defaults(self):
        '''
        Sets all GUI-widgets to default
        '''
        self.gui_handler.set_defaults()

    def __make_own_connections(self):
        '''
        Connects all GUI-buttons to their functions
        '''
        self.edit_frame.ui.pushButtonNextEntry.clicked.connect(
            self.__try_next_entry)
        self.edit_frame.ui.pushButtonPredecentEntry.clicked.connect(
            self.__try_predecent_entry)
        self.edit_frame.ui.pushButtonDeleteEntry.clicked.connect(
            self.delete_entry)
        self.dialogs['delete_dialog'].ui.pushButtonAbortDelete.clicked.connect(
            self.dialogs['delete_dialog'].close)
        self.dialogs['delete_dialog'].ui.pushButtonOkDelete.clicked.connect(
            self.delete_entry_accepted)
        self.dialogs['warn_dialog'].ui.pushButtonAbortWarn.clicked.connect(
            self.__warn_abort)
        self.dialogs['warn_dialog'].ui.pushButtonOnWarn.clicked.connect(
            self.__warn_ignore)
        self.dialogs['warn_dialog'].ui.pushButtonSaveAndOnWarn.clicked.connect(
            self.__warn_save_and_on)
        for i in self.gui_handler.gui_lists['combo_boxes']:
            i.activated.connect(self.value_change)
        for i in self.gui_handler.gui_lists['line_editors']:
            i.textEdited.connect(self.value_change)
        for i in self.gui_handler.gui_lists['checkboxes']:
            i.clicked.connect(self.value_change)
        self.edit_frame.ui.pushButtonCalendar.clicked.connect(
            self.__show_calendar)
        self.edit_frame.ui.pushButtonPlanctonData.clicked.connect(
            self.plancton_data)
        self.edit_frame.ui.pushButtonSightData.clicked.connect(
            self.sight_data)
        self.edit_frame.ui.pushButtonGoToDetailsSight.clicked.connect(
            self.go_to_details_sight)
        self.edit_frame.ui.pushButtonGoBackPlancton.clicked.connect(
            self.go_back_to_start)
        self.edit_frame.ui.pushButtonGoBackSight.clicked.connect(
            self.go_back_to_start)
        self.edit_frame.ui.pushButtonGoBackSightDetails.clicked.connect(
            self.sight_data)
        self.dialogs[
            'transect_deletion_dialog'].ui.pushButtonCancel.clicked.connect(
                self.__transect_deletion_cancelled)
        self.dialogs[
            'transect_deletion_dialog'].ui.pushButtonDelete.clicked.connect(
                self.__transect_deletion_accepted)
        self.edit_frame.ui.pushButtonSailData.clicked.connect(
            self.save_transect_changes)
        self.edit_frame.ui.pushButtonSendOffPlanctonData.clicked.connect(
            self.save_plancton_change)
        self.edit_frame.ui.pushButtonSendOffSightData.clicked.connect(
            self.save_sight_change)
        self.edit_frame.ui.pushButtonSendOffSightEarly.clicked.connect(
            self.save_sight_change)

    def save_sight_change(self):
        '''
        User changed GUI-frames but had changed values in a sight transect,
        wants to save them, so they're stored in the database
        '''
        if self.booleans['values_have_changed']:
            transect_entry = SightTransect(self.edit_frame)
            if not validate_test_class(transect_entry):
                return
            if transect_entry.valid:
                self.__prepare_entry(transect_entry)
                if (
                        transect_entry.transekt_id == 'W'
                        or transect_entry.transekt_id == 'WB'
                        ):
                    if (
                            self.current_row.transekt_id != 'W'
                            and self.current_row.transekt_id != 'WB'
                            ):
                        self.engine.execute(
                            self.tt_observations.delete()
                            .where(
                                self.tt_observations.c.punkt_id
                                == self.current_row.punkt_id
                                )
                            )
                        fid_maximum = self.engine.execute(
                            select([func.max(self.tt_others.c.fid)])
                            ).fetchone()[0] + 1
                        self.engine.execute(
                            self.tt_others.insert()
                            .values(
                                fid=fid_maximum,
                                punkt_id=self.current_row.punkt_id,
                                fahrt_id=self.current_row.fahrt_id,
                                datum=transect_entry.datum,
                                zeit=transect_entry.zeit,
                                kurswoche=transect_entry.kurswoche,
                                guide=transect_entry.guide,
                                schiff=transect_entry.schiff,
                                transekt_id=transect_entry.transekt_id,
                                transektvorgang=transect_entry.transektvorgang,
                                temperatur=transect_entry.temperatur,
                                salinitaet=transect_entry.salinitaet,
                                messzeit=transect_entry.messzeit,
                                breite=transect_entry.breite,
                                laenge=transect_entry.laenge,
                                kurs=transect_entry.kurs,
                                meer_id=transect_entry.meer_id,
                                meer_id_num=transect_entry.meer_id_num,
                                zustand_meer=transect_entry.zustand_meer,
                                wind_id=transect_entry.wind_id,
                                wind_id_num=transect_entry.wind_id_num,
                                windbezeichnung=transect_entry.windbezeichnung,
                                windgeschwindigkeit=(
                                    transect_entry.windgeschwindigkeit),
                                windrichtung_id=transect_entry.windrichtung_id,
                                windrichtung=transect_entry.windrichtung,
                                bewoelkung_id=transect_entry.bewoelkung_id,
                                bewoelkungsgrad=transect_entry.bewoelkungsgrad,
                                sicht_id=transect_entry.sicht_id,
                                sicht_beschreibung=(
                                    transect_entry.sicht_beschreibung),
                                sichttiefe=transect_entry.sichttiefe,
                                fotos=transect_entry.fotos,
                                akustik=transect_entry.akustik,
                                aufnahme=transect_entry.aufnahme,
                                militaer=transect_entry.militaer,
                                segel=transect_entry.segel,
                                zusaetzliche_beobachtungen=(
                                    transect_entry.zusaetzliche_beobachtungen),
                                geom=transect_entry.geom
                                )
                            )
                    else:
                        self.engine.execute(
                            self.tt_others.update()
                            .where(
                                self.tt_others.c.punkt_id
                                == self.current_row.punkt_id
                                )
                            .values(
                                datum=transect_entry.datum,
                                zeit=transect_entry.zeit,
                                kurswoche=transect_entry.kurswoche,
                                guide=transect_entry.guide,
                                schiff=transect_entry.schiff,
                                transekt_id=transect_entry.transekt_id,
                                transektvorgang=transect_entry.transektvorgang,
                                temperatur=transect_entry.temperatur,
                                salinitaet=transect_entry.salinitaet,
                                messzeit=transect_entry.messzeit,
                                breite=transect_entry.breite,
                                laenge=transect_entry.laenge,
                                kurs=transect_entry.kurs,
                                meer_id=transect_entry.meer_id,
                                meer_id_num=transect_entry.meer_id_num,
                                zustand_meer=transect_entry.zustand_meer,
                                wind_id=transect_entry.wind_id,
                                wind_id_num=transect_entry.wind_id_num,
                                windbezeichnung=transect_entry.windbezeichnung,
                                windgeschwindigkeit=(
                                    transect_entry.windgeschwindigkeit),
                                windrichtung_id=transect_entry.windrichtung_id,
                                windrichtung=transect_entry.windrichtung,
                                bewoelkung_id=transect_entry.bewoelkung_id,
                                bewoelkungsgrad=transect_entry.bewoelkungsgrad,
                                sicht_id=transect_entry.sicht_id,
                                sicht_beschreibung=(
                                    transect_entry.sicht_beschreibung),
                                sichttiefe=transect_entry.sichttiefe,
                                fotos=transect_entry.fotos,
                                akustik=transect_entry.akustik,
                                aufnahme=transect_entry.aufnahme,
                                militaer=transect_entry.militaer,
                                segel=transect_entry.segel,
                                zusaetzliche_beobachtungen=(
                                    transect_entry.zusaetzliche_beobachtungen),
                                geom=transect_entry.geom
                                )
                            )
                elif transect_entry.transekt_id != 'ST':
                    if (
                            self.current_row.transekt_id == 'W'
                            or self.current_row.transekt_id == 'WB'
                            ):
                        self.engine.execute(
                            self.tt_others.delete().where(
                                self.tt_others.punkt_id
                                == self.current_row.punkt_id
                                )
                            )
                        fid_maximum = self.engine.execute(
                            select(
                                [func.max(self.tt_others.c.fid)]
                                )
                            ).fetchone()[0] + 1
                        self.engine.execute(
                            self.tt_observations.insert()
                            .values(
                                fid=fid_maximum,
                                punkt_id=self.current_row.punkt_id,
                                fahrt_id=self.current_row.punkt_id,
                                datum=transect_entry.datum,
                                zeit=transect_entry.zeit,
                                kurswoche=transect_entry.kurswoche,
                                guide=transect_entry.guide,
                                schiff=transect_entry.schiff,
                                transekt_id=transect_entry.transekt_id,
                                transektvorgang=transect_entry.transektvorgang,
                                temperatur=transect_entry.temperatur,
                                salinitaet=transect_entry.salinitaet,
                                messzeit=transect_entry.messzeit,
                                breite=transect_entry.breite,
                                laenge=transect_entry.laenge,
                                kurs=transect_entry.kurs,
                                meer_id=transect_entry.meer_id,
                                meer_id_num=transect_entry.meer_id_num,
                                zustand_meer=transect_entry.zustand_meer,
                                wind_id=transect_entry.wind_id,
                                wind_id_num=transect_entry.wind_id_num,
                                windbezeichnung=transect_entry.windbezeichnung,
                                windgeschwindigkeit=(
                                    transect_entry.windgeschwindigkeit),
                                windrichtung_id=transect_entry.windrichtung_id,
                                windrichtung=transect_entry.windrichtung,
                                bewoelkung_id=transect_entry.bewoelkung_id,
                                bewoelkungsgrad=transect_entry.bewoelkungsgrad,
                                sicht_id=transect_entry.sicht_id,
                                sicht_beschreibung=(
                                    transect_entry.sicht_beschreibung),
                                sichttiefe=transect_entry.sichttiefe,
                                fotos=transect_entry.fotos,
                                akustik=transect_entry.akustik,
                                aufnahme=transect_entry.aufnahme,
                                militaer=transect_entry.militaer,
                                segel=transect_entry.segel,
                                art_id=transect_entry.art_id,
                                art=transect_entry.art,
                                vulgaer=transect_entry.vulgaer,
                                anzahl_min=transect_entry.anzahl_min,
                                anzahl_max=transect_entry.anzahl_max,
                                kurs_wal=transect_entry.kurs_wal,
                                position_wal=transect_entry.position_wal,
                                sichtungswinkel=transect_entry.sichtungswinkel,
                                distanz_p=transect_entry.distanz_p,
                                distanz_m=transect_entry.distanz_m,
                                breite_wal=transect_entry.breite_wal,
                                laenge_wal=transect_entry.laenge_wal,
                                dauer=transect_entry.dauer,
                                ruhend=transect_entry.ruhend,
                                langsam=transect_entry.langsam,
                                schnell=transect_entry.schnell,
                                richtung_konstant=(
                                    transect_entry.richtung_konstant),
                                richtung_wechselnd=(
                                    transect_entry.richtung_wechselnd),
                                nahrungsaufnahme=(
                                    transect_entry.nahrungsaufnahme),
                                flukenschlagen=transect_entry.flukenschlagen,
                                spruenge=transect_entry.spruenge,
                                breach_seitlich=transect_entry.breach_seitlich,
                                breach_rueckwaerts=(
                                    transect_entry.breach_rueckwaerts),
                                soziales_verhalten=(
                                    transect_entry.soziales_verhalten),
                                paarung=transect_entry.paarung,
                                spiel=transect_entry.spiel,
                                gruppe_kompakt=transect_entry.gruppe_kompakt,
                                gruppe_locker=transect_entry.gruppe_locker,
                                jungtiere=transect_entry.jungtiere,
                                anzahl_jungtiere=(
                                    transect_entry.anzahl_jungtiere),
                                kaelber=transect_entry.kaelber,
                                neugeborene=transect_entry.neugeborene,
                                annaeherung=transect_entry.annaeherung,
                                schwimmen_nah=transect_entry.schwimmen_nah,
                                bugwellen=transect_entry.bugwellen,
                                heckwellen=transect_entry.heckwellen,
                                seitlich=transect_entry.seitlich,
                                unter_schiff=transect_entry.unter_schiff,
                                tauchgang=transect_entry.tauchgang,
                                fluke_sichtbar=transect_entry.fluke_sichtbar,
                                lautgebung=transect_entry.lautgebung,
                                in_begleitung=transect_entry.in_begleitung,
                                begleitende_spezies=(
                                    transect_entry.begleitende_spezies),
                                blas=transect_entry.blas,
                                blasfrequenz=transect_entry.blasfrequenz,
                                spy_hopping=transect_entry.spy_hopping,
                                anderes_verhalten=(
                                    transect_entry.anderes_verhalten),
                                zusaetzliche_beobachtungen=(
                                    transect_entry.zusaetzliche_beobachtungen),
                                geom=transect_entry.geom
                                ))
                    else:
                        self.engine.execute(
                            self.tt_observations.update()
                            .where(
                                self.tt_observations.c.punkt_id
                                == self.current_row.punkt_id
                                )
                            .values(
                                datum=transect_entry.datum,
                                zeit=transect_entry.zeit,
                                kurswoche=transect_entry.kurswoche,
                                guide=transect_entry.guide,
                                schiff=transect_entry.schiff,
                                transekt_id=transect_entry.transekt_id,
                                transektvorgang=transect_entry.transektvorgang,
                                temperatur=transect_entry.temperatur,
                                salinitaet=transect_entry.salinitaet,
                                messzeit=transect_entry.messzeit,
                                breite=transect_entry.breite,
                                laenge=transect_entry.laenge,
                                kurs=transect_entry.kurs,
                                meer_id=transect_entry.meer_id,
                                meer_id_num=transect_entry.meer_id_num,
                                zustand_meer=transect_entry.zustand_meer,
                                wind_id=transect_entry.wind_id,
                                wind_id_num=transect_entry.wind_id_num,
                                windbezeichnung=transect_entry.windbezeichnung,
                                windgeschwindigkeit=(
                                    transect_entry.windgeschwindigkeit),
                                windrichtung_id=transect_entry.windrichtung_id,
                                windrichtung=transect_entry.windrichtung,
                                bewoelkung_id=transect_entry.bewoelkung_id,
                                bewoelkungsgrad=transect_entry.bewoelkungsgrad,
                                sicht_id=transect_entry.sicht_id,
                                sicht_beschreibung=(
                                    transect_entry.sicht_beschreibung),
                                sichttiefe=transect_entry.sichttiefe,
                                fotos=transect_entry.fotos,
                                akustik=transect_entry.akustik,
                                aufnahme=transect_entry.aufnahme,
                                militaer=transect_entry.militaer,
                                segel=transect_entry.segel,
                                art_id=transect_entry.art_id,
                                art=transect_entry.art,
                                vulgaer=transect_entry.vulgaer,
                                anzahl_min=transect_entry.anzahl_min,
                                anzahl_max=transect_entry.anzahl_max,
                                kurs_wal=transect_entry.kurs_wal,
                                position_wal=transect_entry.position_wal,
                                sichtungswinkel=transect_entry.sichtungswinkel,
                                distanz_p=transect_entry.distanz_p,
                                distanz_m=transect_entry.distanz_m,
                                breite_wal=transect_entry.breite_wal,
                                laenge_wal=transect_entry.laenge_wal,
                                dauer=transect_entry.dauer,
                                ruhend=transect_entry.ruhend,
                                langsam=transect_entry.langsam,
                                schnell=transect_entry.schnell,
                                richtung_konstant=(
                                    transect_entry.richtung_konstant),
                                richtung_wechselnd=(
                                    transect_entry.richtung_wechselnd),
                                nahrungsaufnahme=(
                                    transect_entry.nahrungsaufnahme),
                                flukenschlagen=transect_entry.flukenschlagen,
                                spruenge=transect_entry.spruenge,
                                breach_seitlich=transect_entry.breach_seitlich,
                                breach_rueckwaerts=(
                                    transect_entry.breach_rueckwaerts),
                                soziales_verhalten=(
                                    transect_entry.soziales_verhalten),
                                paarung=transect_entry.paarung,
                                spiel=transect_entry.spiel,
                                gruppe_kompakt=transect_entry.gruppe_kompakt,
                                gruppe_locker=transect_entry.gruppe_locker,
                                jungtiere=transect_entry.jungtiere,
                                anzahl_jungtiere=(
                                    transect_entry.anzahl_jungtiere),
                                kaelber=transect_entry.kaelber,
                                neugeborene=transect_entry.neugeborene,
                                annaeherung=transect_entry.annaeherung,
                                schwimmen_nah=transect_entry.schwimmen_nah,
                                bugwellen=transect_entry.bugwellen,
                                heckwellen=transect_entry.heckwellen,
                                seitlich=transect_entry.seitlich,
                                unter_schiff=transect_entry.unter_schiff,
                                tauchgang=transect_entry.tauchgang,
                                fluke_sichtbar=transect_entry.fluke_sichtbar,
                                lautgebung=transect_entry.lautgebung,
                                in_begleitung=transect_entry.in_begleitung,
                                begleitende_spezies=(
                                    transect_entry.begleitende_spezies),
                                blas=transect_entry.blas,
                                blasfrequenz=transect_entry.blasfrequenz,
                                spy_hopping=transect_entry.spy_hopping,
                                anderes_verhalten=(
                                    transect_entry.anderes_verhalten),
                                zusaetzliche_beobachtungen=(
                                    transect_entry.zusaetzliche_beobachtungen),
                                geom=transect_entry.geom
                                )
                        )
                self.engine.execute(
                    self.points.update()
                    .where(
                        self.points.c.punkt_id == self.current_row.punkt_id
                        )
                    .values(
                        datum=transect_entry.datum,
                        zeit=transect_entry.zeit,
                        messzeit=transect_entry.zeit,
                        kurswoche=transect_entry.kurswoche,
                        guide=transect_entry.guide,
                        schiff=transect_entry.schiff,
                        transekt_id=transect_entry.transekt_id,
                        temperatur=transect_entry.temperatur,
                        salinitaet=transect_entry.salinitaet,
                        breite=transect_entry.breite,
                        laenge=transect_entry.laenge,
                        kurs=transect_entry.kurs,
                        meer_id=transect_entry.meer_id,
                        wind_id=transect_entry.wind_id,
                        windrichtung_id=transect_entry.windrichtung_id,
                        bewoelkung_id=transect_entry.bewoelkung_id,
                        sicht_id=transect_entry.sicht_id,
                        sichttiefe=transect_entry.sichttiefe,
                        fotos=transect_entry.fotos,
                        akustik=transect_entry.akustik,
                        aufnahme=transect_entry.aufnahme,
                        militaer=transect_entry.militaer,
                        segel=transect_entry.segel,
                        art_id=transect_entry.art_id,
                        anzahl_min=transect_entry.anzahl_min,
                        anzahl_max=transect_entry.anzahl_max,
                        kurs_wal=transect_entry.kurs_wal,
                        position_wal=transect_entry.position_wal,
                        sichtungswinkel=transect_entry.sichtungswinkel,
                        distanz_p=transect_entry.distanz_p,
                        distanz_m=transect_entry.distanz_m,
                        breite_wal=transect_entry.breite_wal,
                        laenge_wal=transect_entry.laenge_wal,
                        dauer=transect_entry.dauer,
                        ruhend=transect_entry.ruhend,
                        langsam=transect_entry.langsam,
                        schnell=transect_entry.schnell,
                        richtung_konstant=transect_entry.richtung_konstant,
                        richtung_wechselnd=transect_entry.richtung_wechselnd,
                        nahrungsaufnahme=transect_entry.nahrungsaufnahme,
                        flukenschlagen=transect_entry.flukenschlagen,
                        spruenge=transect_entry.spruenge,
                        breach_seitlich=transect_entry.breach_seitlich,
                        breach_rueckwaerts=transect_entry.breach_rueckwaerts,
                        soziales_verhalten=transect_entry.soziales_verhalten,
                        paarung=transect_entry.paarung,
                        spiel=transect_entry.spiel,
                        gruppe_kompakt=transect_entry.gruppe_kompakt,
                        gruppe_locker=transect_entry.gruppe_locker,
                        jungtiere=transect_entry.jungtiere,
                        anzahl_jungtiere=transect_entry.anzahl_jungtiere,
                        kaelber=transect_entry.kaelber,
                        neugeborene=transect_entry.neugeborene,
                        annaeherung=transect_entry.annaeherung,
                        schwimmen_nah=transect_entry.schwimmen_nah,
                        bugwellen=transect_entry.bugwellen,
                        heckwellen=transect_entry.heckwellen,
                        seitlich=transect_entry.seitlich,
                        unter_schiff=transect_entry.unter_schiff,
                        tauchgang=transect_entry.tauchgang,
                        fluke_sichtbar=transect_entry.fluke_sichtbar,
                        lautgebung=transect_entry.lautgebung,
                        in_begleitung=transect_entry.in_begleitung,
                        begleitende_spezies=transect_entry.begleitende_spezies,
                        blas=transect_entry.blas,
                        blasfrequenz=transect_entry.blasfrequenz,
                        spy_hopping=transect_entry.spy_hopping,
                        anderes_verhalten=transect_entry.anderes_verhalten,
                        zusaetzliche_beobachtungen=transect_entry.zusaetzliche_beobachtungen,
                        geom=transect_entry.geom,
                        )
                    )
            self.booleans['values_have_changed'] = False
        else:
            return
        self.go_back_to_start()

    def save_plancton_change(self):
        '''
        User changed GUI-frames but had changed values in a plancton transect,
        wants to save them, so they're stored in the database
        '''
        if self.booleans['values_have_changed']:
            transect_entry = PlanctonTransect(self.edit_frame)
            if not validate_test_class(transect_entry):
                return
            if transect_entry.valid:
                self.__prepare_entry(transect_entry)
                self.engine.execute(
                    self.points.update()
                    .where(
                        self.points.c.punkt_id == self.current_row.punkt_id
                        )
                    .values(
                        datum=transect_entry.datum,
                        zeit=transect_entry.zeit,
                        messzeit=transect_entry.messzeit,
                        kurswoche=transect_entry.kurswoche,
                        guide=transect_entry.guide,
                        breite=transect_entry.breite,
                        laenge=transect_entry.laenge,
                        kurs=transect_entry.kurs,
                        fotos=transect_entry.fotos,
                        aufnahme=transect_entry.fotos,
                        meer_id=transect_entry.meer_id,
                        wind_id=transect_entry.wind_id,
                        windrichtung_id=transect_entry.windrichtung_id,
                        bewoelkung_id=transect_entry.bewoelkung_id,
                        sicht_id=transect_entry.sicht_id,
                        segel=transect_entry.segel,
                        akustik=transect_entry.akustik,
                        militaer=transect_entry.militaer,
                        geom=transect_entry.geom,
                        schiff=transect_entry.schiff,
                        temperatur=transect_entry.temperatur,
                        salinitaet=transect_entry.salinitaet,
                        sichttiefe=transect_entry.sichttiefe,
                        zooplanktonprobe=transect_entry.zooplanktonprobe,
                        phytoplanktonprobe=transect_entry.phytoplanktonprobe,
                        wasserprobe=transect_entry.wasserprobe
                        )
                    )
                self.engine.execute(
                    self.tt_others.update()
                    .where(
                        self.tt_others.c.punkt_id == self.current_row.punkt_id
                        )
                    .values(
                        datum=transect_entry.datum,
                        zeit=transect_entry.zeit,
                        kurswoche=transect_entry.kurswoche,
                        guide=transect_entry.guide,
                        schiff=transect_entry.schiff,
                        temperatur=transect_entry.temperatur,
                        salinitaet=transect_entry.salinitaet,
                        messzeit=transect_entry.messzeit,
                        breite=transect_entry.breite,
                        laenge=transect_entry.laenge,
                        kurs=transect_entry.kurs,
                        meer_id=transect_entry.meer_id,
                        meer_id_num=transect_entry.meer_id_num,
                        zustand_meer=transect_entry.zustand_meer,
                        wind_id=transect_entry.wind_id,
                        wind_id_num=transect_entry.wind_id_num,
                        windbezeichnung=transect_entry.windbezeichnung,
                        windgeschwindigkeit=transect_entry.windgeschwindigkeit,
                        windrichtung_id=transect_entry.windrichtung_id,
                        windrichtung=transect_entry.windrichtung,
                        bewoelkung_id=transect_entry.bewoelkung_id,
                        bewoelkungsgrad=transect_entry.bewoelkungsgrad,
                        sicht_id=transect_entry.sicht_id,
                        sicht_beschreibung=transect_entry.sicht_beschreibung,
                        sichttiefe=transect_entry.sichttiefe,
                        fotos=transect_entry.fotos,
                        akustik=transect_entry.akustik,
                        aufnahme=transect_entry.fotos,
                        zooplanktonprobe=transect_entry.zooplanktonprobe,
                        phytoplanktonprobe=transect_entry.phytoplanktonprobe,
                        wasserprobe=transect_entry.wasserprobe,
                        militaer=transect_entry.militaer,
                        segel=transect_entry.segel,
                        geom=transect_entry.geom
                        )
                    )

            self.booleans['values_have_changed'] = False
        else:
            return
        self.go_back_to_start()

    def save_transect_changes(self):
        '''
        User changed GUI-frames but had changed values in a course transect,
        wants to save them, so they're stored in the database
        '''
        if self.booleans['values_have_changed']:
            transect_entry = PureTransect(self.edit_frame)
            if not validate_test_class(transect_entry):
                return
            if transect_entry.valid:
                self.__prepare_entry(transect_entry)
                id_in_database = self.current_row.punkt_id
                if transect_entry.transekt_id == 'B':
                    transect_end = self.get_transect_point(
                        transect_entry.fahrt_id, 'E  ')
                    temporary_geometry = self.get_transect_geometry(
                        transect_entry, transect_entry, transect_entry.fahrt_id)
                    self.connection.execute(
                        self.transects.update()
                        .where(
                            self.transects.c.fahrt_id == transect_entry.fahrt_id
                            )
                        .values(
                            datum_b=transect_entry.datum,
                            zeit_b=transect_entry.zeit,
                            kurswoche=transect_entry.kurswoche,
                            guide=transect_entry.guide,
                            schiff=transect_entry.schiff,
                            akustik=transect_entry.akustik,
                            geom=temporary_geometry
                            )
                        )
                elif transect_entry.transekt_id == 'KW':
                    transect_start = self.get_transect_point(
                        transect_entry.fahrt_id, 'B  ')
                    transect_end = self.get_transect_point(
                        transect_entry.fahrt_id, 'E  ')
                    temporary_geometry = self.get_transect_geometry(
                        transect_start, transect_end, transect_entry.fahrt_id)
                    self.connection.execute(
                        self.transects.update()
                        .where(
                            self.transects.c.fahrt_id == transect_entry.fahrt_id
                            )
                        .values(
                            schiff=transect_entry.schiff,
                            akustik=transect_entry.akustik,
                            geom=temporary_geometry
                            )
                        )
                elif transect_entry.transekt_id == 'E':
                    transect_start = self.get_transect_point(
                        transect_entry.fahrt_id, 'B  ')
                    temporary_geometry = self.get_transect_geometry(
                        transect_start, transect_entry, transect_entry.fahrt_id)
                    self.connection.execute(
                        self.transects.update()
                        .where(
                            self.transects.c.fahrt_id == transect_entry.fahrt_id
                            )
                        .values(
                            datum_e=transect_entry.datum,
                            zeit_e=transect_entry.zeit,
                            kurswoche=transect_entry.kurswoche,
                            guide=transect_entry.guide,
                            schiff=transect_entry.schiff,
                            akustik=transect_entry.akustik,
                            geom=temporary_geometry
                            )
                        )
                self.connection.execute(
                    self.points.update()
                    .where(
                        self.points.c.punkt_id == id_in_database
                        )
                    .values(
                        datum=transect_entry.datum,
                        zeit=transect_entry.zeit,
                        kurswoche=transect_entry.kurswoche,
                        guide=transect_entry.guide,
                        breite=transect_entry.breite,
                        laenge=transect_entry.laenge,
                        kurs=transect_entry.kurs,
                        meer_id=transect_entry.meer_id,
                        wind_id=transect_entry.wind_id,
                        windrichtung_id=transect_entry.windrichtung_id,
                        bewoelkung_id=transect_entry.bewoelkung_id,
                        sicht_id=transect_entry.sicht_id,
                        segel=transect_entry.segel,
                        akustik=transect_entry.akustik,
                        militaer=transect_entry.militaer,
                        geom=transect_entry.geom,
                        schiff=transect_entry.schiff,
                        )
                    )
            self.booleans['values_have_changed'] = False
        else:
            return
        self.go_back_to_start()

    def __prepare_entry(self, test_class):
        '''
        Prepare data for entry in db
        '''
        test_class.prepareForEntry()
        test_class.punkt_id = self.current_row.punkt_id
        test_class.fahrt_id = self.current_row.fahrt_id

    def __transect_deletion_cancelled(self):
        '''
        User cancelled the deletion of a dataset
        '''
        self.dialogs['transect_deletion_dialog'].concurred = False
        self.dialogs['transect_deletion_dialog'].close()

    def __transect_deletion_accepted(self):
        '''
        User wants to delete a dataset
        '''
        self.dialogs['transect_deletion_dialog'].concurred = True
        self.dialogs['transect_deletion_dialog'].close()

    def __show_calendar(self):
        '''
        Shows calendar for date-selection
        '''
        self.dialogs['calendar'].show()

    def __set_index_label(self):
        '''
        Sets the GUI-label showing the current index
        of dataset viewed in database
        '''
        self.edit_frame.ui.labelCurrentEntry.setText(
            self.language_dict['entry_title']
            + str(self.current_row_absolut)
            + self.language_dict['entry_of']
            + str(self.number_of_entries)
            )

    def __initialize_with_newest_entry(self):
        '''
        On start-up of editing mode, the GUI is initialized
        showing the most current dataset in the database
        '''
        self.edit_frame.ui.pushButtonNextEntry.setEnabled(False)
        self.number_of_entries = self.engine.execute(
            select([func.count()]).select_from(self.points)).fetchone()[0]
        self.current_row_absolut = self.number_of_entries
        self.current_row_in_database = self.session.query(MtPunkte).order_by(MtPunkte.datum.desc(), MtPunkte.zeit.desc()).first().punkt_id
        self.current_row = self.__return_current_shown_row()
        self.setup_basic_values(self.current_row)

    def __try_predecent_entry(self):
        '''
        Tries to show predecent entry in GUI, but first checks
        if the user changed any values
        '''
        if self.booleans['values_have_changed']:
            self.booleans['predecent_entry_button_pushed'] = True
            self.dialogs['warn_dialog'].exec_()
        else:
            self.predecent_entry()

    def __try_next_entry(self):
        '''
        Tries to show next entry in GUI, but first checks
        if the user changed any values
        '''
        if self.booleans['values_have_changed']:
            self.booleans['next_entry_button_pushed'] = True
            self.dialogs['warn_dialog'].exec_()
        else:
            self.next_entry()

    def __try_linear_id(self):
        '''
        For performance reasons, try to get next higher / lower
        index of identifier in the database
        '''
        self.__set_defaults()
        return self.__return_current_shown_row()

    def __send_row_to_gui(self, current_row):
        '''
        Sends a row from the database to the GUI
        '''
        self.current_row = current_row
        self.__check_for_end_of_table()
        self.setup_basic_values(self.current_row)

    def predecent_entry(self):
        '''
        Pulls the predecent entry in the database into the GUI
        '''
        self.edit_frame.ui.pushButtonNextEntry.setEnabled(True)
        self.current_row_in_database = self.session.query(MtPunkte).filter(((MtPunkte.datum == self.current_row.datum) & (MtPunkte.zeit < self.current_row.zeit)) |
            (MtPunkte.datum < self.current_row.datum)).order_by(MtPunkte.datum.desc(), MtPunkte.zeit.desc()).first().punkt_id
        self.current_row_absolut -= 1
        self.__send_row_to_gui(self.__return_current_shown_row())

    def next_entry(self):
        '''
        Pulls the next entry in the database into the GUI
        '''
        self.edit_frame.ui.pushButtonPredecentEntry.setEnabled(True)
        self.current_row_in_database = self.session.query(MtPunkte).filter(((MtPunkte.datum == self.current_row.datum) & (MtPunkte.zeit > self.current_row.zeit)) |
            (MtPunkte.datum > self.current_row.datum)).order_by(MtPunkte.datum.asc(), MtPunkte.zeit.asc()).first().punkt_id
        self.current_row_absolut += 1
        self.__send_row_to_gui(self.__return_current_shown_row())

    def __check_for_end_of_table(self):
        '''
        Checks if the dataset selected is the newest one in the database
        '''
        maximum = self.session.query(MtPunkte).order_by(MtPunkte.datum.desc(), MtPunkte.zeit.desc()).first().punkt_id
        if self.current_row.punkt_id == maximum:
            self.edit_frame.ui.pushButtonNextEntry.setEnabled(False)

    def setup_basic_values(self, row):
        '''
        Sets up those GUI-elements common for all transect-types for
        a new dataset
        '''
        self.__set_index_label()
        for i in range(12):
            j = self.edit_frame.ui.comboBoxTransectID.model().index(i, 0)
            self.edit_frame.ui.comboBoxTransectID.model().setData(
                j, QVariant(1 | 32), Qt.UserRole-1)
        self.edit_frame.ui.comboBoxTransectID.setCurrentIndex(
            DICT_TRANSECT_ID[row.transekt_id])
        self.booleans['values_have_changed'] = False
        self.edit_frame.ui.pushButtonPlanctonData.setEnabled(True)
        self.edit_frame.ui.pushButtonSailData.setEnabled(True)
        self.edit_frame.ui.pushButtonSightData.setEnabled(True)
        if row.datum is not None:
            self.edit_frame.ui.dateEdit.setDate(QDate(row.datum))
        if row.zeit is not None:
            self.edit_frame.ui.timeEdit.setTime(QTime(row.zeit))
        if row.breite is not None:
            self.edit_frame.ui.lineEditBreitenGrad.setText(str(row.breite))
        if row.laenge is not None:
            self.edit_frame.ui.lineEditLangenGrad.setText(str(row.laenge))
        if row.kurswoche is not None:
            self.edit_frame.ui.lineEditCourseWeek.setText(str(row.kurswoche))
        if row.guide is not None:
            self.edit_frame.ui.lineEditGuide.setText(unicode(row.guide))
        if row.kurs is not None:
            self.edit_frame.ui.lineEditCourse.setText(str(row.kurs))
        if row.schiff is not None:
            self.edit_frame.ui.lineEditShipName.setText(
                unicode(str(row.schiff).strip()))
        if row.meer_id is None:
            self.edit_frame.ui.comboBoxSea.setCurrentIndex(12)
        else:
            self.edit_frame.ui.comboBoxSea.setCurrentIndex(
                DICT_SEA[unicode(row.meer_id.strip())])
        if row.bewoelkung_id is None:
            self.edit_frame.ui.comboBoxClouds.setCurrentIndex(9)
        else:
            self.edit_frame.ui.comboBoxClouds.setCurrentIndex(row.bewoelkung_id)
        if row.sicht_id is None:
            self.edit_frame.ui.comboBoxSight.setCurrentIndex(3)
        else:
            self.edit_frame.ui.comboBoxSight.setCurrentIndex(row.sicht_id - 1)
        if row.wind_id is None:
            self.edit_frame.ui.comboBoxWindStrength.setCurrentIndex(0)
        else:
            self.edit_frame.ui.comboBoxWindStrength.setCurrentIndex(
                DICT_WIND[unicode(row.wind_id.strip())])
        if row.windrichtung_id is None:
            self.edit_frame.ui.comboBoxWindDirection.setCurrentIndex(15)
        else:
            self.edit_frame.ui.comboBoxWindDirection.setCurrentIndex(
                DICT_WIND_DIRECTION[unicode(row.windrichtung_id.strip())])
        if row.akustik:
            self.edit_frame.ui.checkBoxAcoustic.setCheckState(2)
        if row.segel:
            self.edit_frame.ui.checkBoxSail.setCheckState(2)
        if row.militaer:
            self.edit_frame.ui.checkBoxMilitaryActivity.setCheckState(2)

        if (row.transekt_id.strip() == u'B' or row.transekt_id.strip() == u'KW'
                or row.transekt_id.strip() == u'E'):
            self.setup_pure_transect(row)

        elif row.transekt_id.strip() == u'AA':
            self.setup_plancton_transect(row)

        else:
            self.setup_sight_transect(row)

    def setup_pure_transect(self, row):
        '''
        Sets up those GUI-elements relevant for a course-transect for
        a new dataset
        '''
        if row.transekt_id.strip() == 'B':
            disable = [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12]
        if row.transekt_id.strip() == 'KW':
            disable = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12]
        if row.transekt_id.strip() == 'E':
            disable = [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12]
        for i in disable:
            j = self.edit_frame.ui.comboBoxTransectID.model().index(i, 0)
            self.edit_frame.ui.comboBoxTransectID.model().setData(
                j, QVariant(0), Qt.UserRole-1)
        self.edit_frame.ui.labelCurrentTransectType.setText(self.language_dict[unicode(row.transekt_id.strip())])
        self.edit_frame.ui.labelWarnText.setText(self.language_dict['transect_warning'])
        self.edit_frame.ui.pushButtonPlanctonData.setEnabled(False)
        self.edit_frame.ui.pushButtonSightData.setEnabled(False)

    def setup_plancton_transect(self, row):
        '''
        Sets up those GUI-elements relevant for a plancton-transect for
        a new dataset
        '''
        disable = [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for i in disable:
            j = self.edit_frame.ui.comboBoxTransectID.model().index(i, 0)
            self.edit_frame.ui.comboBoxTransectID.model().setData(
                j, QVariant(0), Qt.UserRole-1)
        self.edit_frame.ui.labelCurrentTransectType.setText(self.language_dict['probe_combo'])
        self.edit_frame.ui.labelWarnText.setText(self.language_dict['probe_warning'])
        self.edit_frame.ui.pushButtonSailData.setEnabled(False)
        self.edit_frame.ui.pushButtonSightData.setEnabled(False)

        if row.temperatur is not None:
            self.edit_frame.ui.lineEditTemperaturePlancton.setText(
                str(row.temperatur))
        if row.salinitaet is not None:
            self.edit_frame.ui.lineEditSalinityPlancton.setText(
                str(row.salinitaet))
        if row.sichttiefe is not None:
            self.edit_frame.ui.lineEditSightDepthPlancton.setText(
                str(row.sichttiefe))
        if row.zooplanktonprobe:
            self.edit_frame.ui.checkBoxZooPlancton.setCheckState(2)
        if row.phytoplanktonprobe:
            self.edit_frame.ui.checkBoxPhytoPlancton.setCheckState(2)
        if row.wasserprobe:
            self.edit_frame.ui.checkBoxWaterSamplePlancton.setCheckState(2)

    def setup_sight_transect(self, row):
        '''
        Sets up those GUI-elements relevant for a sight-transect for
        a new dataset
        '''
        disable = [1, 4, 5, 7]
        for i in disable:
            j = self.edit_frame.ui.comboBoxTransectID.model().index(i, 0)
            self.edit_frame.ui.comboBoxTransectID.model().setData(
                j, QVariant(0), Qt.UserRole-1)
        self.edit_frame.ui.labelCurrentTransectType.setText(
            self.language_dict[unicode(row.transekt_id).strip()])
        self.edit_frame.ui.labelWarnText.setText(self.language_dict['sight_warning'])
        self.edit_frame.ui.pushButtonPlanctonData.setEnabled(False)
        self.edit_frame.ui.pushButtonSailData.setEnabled(False)

        if row.temperatur is not None:
            self.edit_frame.ui.lineEditTemperatureSights.setText(
                str(row.temperatur))
        if row.salinitaet is not None:
            self.edit_frame.ui.lineEditSalinitySights.setText(
                str(row.salinitaet))
        if row.sichttiefe is not None:
            self.edit_frame.ui.lineEditSightDepthSights.setText(
                str(row.sichttiefe))
        if row.art_id is None:
            self.edit_frame.ui.comboBoxSpecies.setCurrentIndex(20)
        else:
            self.edit_frame.ui.comboBoxSpecies.setCurrentIndex(
                DICT_SPECIES[unicode(row.art_id.strip())])
        if row.kurs_wal is not None:
            self.edit_frame.ui.lineEditCourseWhale.setText(str(row.kurs_wal))
        if row.anzahl_min is not None:
            self.edit_frame.ui.lineEditNumberMin.setText(str(row.anzahl_min))
        if row.anzahl_max is not None:
            self.edit_frame.ui.lineEditNumberMax.setText(str(row.anzahl_max))
        if row.position_wal is not None:
            self.edit_frame.ui.lineEditPositionWhale.setText(
                str(row.position_wal))
        if row.distanz_p is not None:
            self.edit_frame.ui.lineEditParamDistance.setText(
                str(row.distanz_p))
        if row.dauer is not None:
            self.edit_frame.ui.lineEditDuration.setText(str(row.dauer))
        if row.distanz_m is not None:
            self.edit_frame.ui.lineEditDistanceToShip.setText(
                str(row.distanz_m))
        if row.zusaetzliche_beobachtungen is not None:
            self.edit_frame.ui.textEditOtherObservations.setText(
                unicode(str(row.zusaetzliche_beobachtungen)))
        if row.anderes_verhalten is not None:
            self.edit_frame.ui.textEditSpecialBehaviour.setText(
                unicode(str(row.anderes_verhalten)))
        if row.ruhend:
            self.edit_frame.ui.checkBoxLazy.setCheckState(2)
        if row.langsam:
            self.edit_frame.ui.checkBoxSlowSwim.setCheckState(2)
        if row.schnell:
            self.edit_frame.ui.checkBoxFastSwim.setCheckState(2)
        if row.richtung_wechselnd:
            self.edit_frame.ui.checkBoxNotConstantSwim.setCheckState(2)
        if row.richtung_konstant:
            self.edit_frame.ui.checkBoxConstantSwim.setCheckState(2)
        if row.nahrungsaufnahme:
            self.edit_frame.ui.checkBoxEating.setCheckState(2)
        if row.tauchgang:
            self.edit_frame.ui.checkBoxDive.setCheckState(2)
        if row.fluke_sichtbar:
            self.edit_frame.ui.checkBoxFlukeSight.setCheckState(2)
        if row.spy_hopping:
            self.edit_frame.ui.checkBoxSpyHop.setCheckState(2)
        if row.flukenschlagen:
            self.edit_frame.ui.checkBoxFlukeHit.setCheckState(2)
        if row.paarung:
            self.edit_frame.ui.checkBoxMating.setCheckState(2)
        if row.spiel:
            self.edit_frame.ui.checkBoxPlaying.setCheckState(2)
        if row.annaeherung:
            self.edit_frame.ui.checkBoxCurious.setCheckState(2)
        if row.lautgebung:
            self.edit_frame.ui.checkBoxLoud.setCheckState(2)
        if row.fotos:
            self.edit_frame.ui.checkBoxFotos.setCheckState(2)
            self.edit_frame.ui.checkBoxFotosMade.setEnabled(True)
            self.edit_frame.ui.labelFotosMade.setEnabled(True)
        if row.aufnahme:
            self.edit_frame.ui.checkBoxFotosMade.setCheckState(2)
        if row.blas:
            self.edit_frame.ui.checkBoxBlow.setCheckState(2)
            self.edit_frame.ui.labelBlowFrequency.setEnabled(True)
            self.edit_frame.ui.lineEditBlowFrequency.setEnabled(True)
        if row.blasfrequenz is not None:
            self.edit_frame.ui.lineEditBlowFrequency.setText(
                str(row.blasfrequenz))
        if row.in_begleitung:
            self.edit_frame.ui.checkBoxOtherSpecies.setCheckState(2)
            self.edit_frame.ui.labelOtherSpecies.setEnabled(True)
            self.edit_frame.ui.lineEditOtherSpecies.setEnabled(True)
        if row.begleitende_spezies is not None:
            self.edit_frame.ui.lineEditOtherSpecies.setText(
                unicode(str(row.begleitende_spezies)))
        if row.spruenge:
            self.edit_frame.ui.checkBoxJump.setCheckState(2)
            self.edit_frame.ui.labelBreachBack.setEnabled(True)
            self.edit_frame.ui.checkBoxBreachBack.setEnabled(True)
            self.edit_frame.ui.labelBreachSide.setEnabled(True)
            self.edit_frame.ui.checkBoxBreachSide.setEnabled(True)
        if row.breach_seitlich:
            self.edit_frame.ui.checkBoxBreachSide.setCheckState(2)
        if row.breach_rueckwaerts:
            self.edit_frame.ui.checkBoxBreachBack.setCheckState(2)
        if row.jungtiere:
            self.edit_frame.ui.checkBoxYoungOnes.setCheckState(2)
            self.edit_frame.ui.labelChildren.setEnabled(True)
            self.edit_frame.ui.labelNewBorn.setEnabled(True)
            self.edit_frame.ui.labelNumNewBorns.setEnabled(True)
            self.edit_frame.ui.checkBoxChildren.setEnabled(True)
            self.edit_frame.ui.checkBoxNewborn.setEnabled(True)
            self.edit_frame.ui.lineEditNumNewBorns.setEnabled(True)
        if row.kaelber:
            self.edit_frame.ui.checkBoxChildren.setCheckState(2)
        if row.neugeborene:
            self.edit_frame.ui.checkBoxNewborn.setCheckState(2)
        if row.anzahl_jungtiere is not None:
            self.edit_frame.ui.lineEditNumNewBorns.setText(
                str(row.anzahl_jungtiere))
        if row.schwimmen_nah:
            self.edit_frame.ui.checkBoxCloseBoat.setCheckState(2)
            self.edit_frame.ui.labelRideBack.setEnabled(True)
            self.edit_frame.ui.labelRideDive.setEnabled(True)
            self.edit_frame.ui.labelRideFront.setEnabled(True)
            self.edit_frame.ui.labelRideSide.setEnabled(True)
            self.edit_frame.ui.checkBoxRideBack.setEnabled(True)
            self.edit_frame.ui.checkBoxRideDive.setEnabled(True)
            self.edit_frame.ui.checkBoxRideFront.setEnabled(True)
            self.edit_frame.ui.checkBoxRideSide.setEnabled(True)
        if row.bugwellen:
            self.edit_frame.ui.checkBoxRideFront.setCheckState(2)
        if row.seitlich:
            self.edit_frame.ui.checkBoxRideSide.setCheckState(2)
        if row.heckwellen:
            self.edit_frame.ui.checkBoxRideBack.setCheckState(2)
        if row.unter_schiff:
            self.edit_frame.ui.checkBoxRideDive.setCheckState(2)
        if row.soziales_verhalten:
            self.edit_frame.ui.checkBoxSocial.setCheckState(2)
            self.edit_frame.ui.checkBoxCompact.setEnabled(True)
            self.edit_frame.ui.checkBoxNotCompact.setEnabled(True)
            self.edit_frame.ui.labelCompact.setEnabled(True)
            self.edit_frame.ui.labelNotCompact.setEnabled(True)
        if row.gruppe_kompakt:
            self.edit_frame.ui.checkBoxCompact.setCheckState(2)
        if row.gruppe_locker:
            self.edit_frame.ui.checkBoxNotCompact.setCheckState(2)

    def value_change(self):
        '''
        User changed a value of a datafield in the GUI
        '''
        self.booleans['values_have_changed'] = True

    def delete_entry(self):
        '''
        User wants to delete an entry, show warning-dialog
        '''
        self.dialogs['delete_dialog'].exec_()

    def delete_row_main(self):
        '''
        Delete entry in table mt_punkte
        '''
        identifier = self.current_row.punkt_id
        self.engine.execute(self.points.delete().where(
            self.points.c.punkt_id == identifier))
        self.number_of_entries -= 1
        return identifier

    def delete_entry_accepted(self):
        '''
        User assured he wants to delete, now carry out
        deletion of dataset in database
        '''
        if self.current_row.transekt_id in TT_OTHERS_IDS:
            identifier = self.delete_row_main()
            result = self.engine.execute(
                select([self.tt_others]).where(
                    self.tt_others.c.punkt_id == identifier))
            for row in result:
                self.engine.execute(
                    self.tt_others.delete()
                    .where(row.c.punkt_id == identifier))
        elif self.current_row.transekt_id in MT_FAHRTEN_IDS:
            self.dialogs['transect_deletion_dialog'].exec_()
            if self.dialogs['transect_deletion_dialog'].concurred:
                result = self.engine.execute(
                    select([self.points]).where(
                        self.points.c.fahrt_id == self.current_row.fahrt_id))
                for row in result:
                    if row.transekt_id in MT_FAHRTEN_IDS:
                        self.engine.execute(
                            self.points.delete()
                            .where(
                                self.points.c.punkt_id == row.punkt_id
                                )
                            )
                        self.number_of_entries -= 1
                    elif row.transekt_id in TT_OTHERS_IDS:
                        self.connection.execute(
                            self.points.update()
                            .where(
                                self.points.c.punkt_id == row.punkt_id
                                )
                            .values(
                                fahrt_id=None
                                )
                            )
                        self.connection.execute(
                            self.tt_others.update()
                            .where(
                                self.tt_others.c.punkt_id == row.punkt_id
                                )
                            .values(
                                fahrt_id=None
                                )
                            )
                    elif row.transekt_id == 'S  ':
                        self.change_transekt_id(row.punkt_id, 'A  ')
                    elif row.transekt_id == 'Ak ':
                        self.change_transekt_id(row.punkt_id, 'Ako')
                    else:
                        self.connection.execute(
                            self.points.update()
                            .where(
                                self.points.c.punkt_id == row.punkt_id
                                )
                            .values(
                                fahrt_id=None
                                )
                            )
                        self.connection.execute(
                            self.tt_observations.update()
                            .where(
                                self.tt_observations.c.punkt_id == row.punkt_id
                                )
                            .values(
                                fahrt_id=None
                                )
                            )
                self.engine.execute(
                    self.transects.delete()
                    .where(
                        self.transects.c.fahrt_id == self.current_row.fahrt_id
                        )
                    )
            else:
                self.dialogs['delete_dialog'].close()
                return
        else:
            identifier = self.delete_row_main()
            result = self.engine.execute(
                select(
                    self.tt_observations).where(
                        self.tt_observations.c.punkt_id == identifier))
            for row in result:
                self.engine.execute(
                    self.tt_observations
                    .delete()
                    .where(row.c.punkt_id == identifier))

        self.dialogs['delete_dialog'].close()
        if self.current_row_absolut == 1:
            self.next_entry()
        else:
            self.predecent_entry()

    def __show_warning_message(self):
        '''
        Show the warning dialog
        '''
        self.dialogs['warn_dialog'].exec_()

    def __warn_abort(self):
        '''
        Show abort-dialog
        '''
        self.dialogs['warn_dialog'].close()

    def __warn_ignore(self):
        '''
        User ignored warning, carry on
        '''
        self.dialogs['warn_dialog'].close()
        if self.booleans['next_entry_button_pushed']:
            self.next_entry()
        elif self.booleans['predecent_entry_button_pushed']:
            self.predecent_entry()
        self.booleans['next_entry_button_pushed'] = False
        self.booleans['predecent_entry_button_pushed'] = False

    def __warn_save_and_on(self):
        '''
        User goes on
        '''
        self.__check_for_end_of_table()
        print 'Implement'

    def __get_max_id_in_punkt_id(self):
        '''
        Returns the highest primary key in punkt_id
        '''
        return self.engine.execute(
            select([func.max(self.points.c.punkt_id)])).fetchone()[0]

    def __return_current_shown_row(self):
        '''
        Returns row currently displayed in GUI in punkt_id
        '''
        return self.session.query(MtPunkte).filter(MtPunkte.punkt_id == self.current_row_in_database).first()

    def change_transekt_id(self, punkt_id, transekt_id):
        '''
        Changes the transect_id of rows in tables mt_punkte
        and tt_pbservations when state of a transect is changed.
        Identifier is 'punkt_id', transekt_id is changed to transekt_id
        '''
        self.connection.execute(
            self.points.update()
            .where(self.points.c.punkt_id == punkt_id)
            .values(fahrt_id=None, transekt_id=transekt_id)
            )
        self.connection.execute(
            self.tt_observations.update()
            .where(self.tt_observations.c.punkt_id == punkt_id)
            .values(fahrt_id=None, transekt_id=transekt_id)
            )

    def get_transect_point(self, fahrt_id, transekt_id):
        '''
        Returns the start or end of a transect with fahrt_id
        'fahrt_id', depending if transekt_id is 'B  ' or 'E  '
        '''
        self.engine.execute(
            select([self.points])
            .where(
                self.points.c.fahrt_id == fahrt_id
                )
            .where(
                self.points.c.transekt_id == transekt_id
                )
            ).fetchone()

    def __get_intermediate_points(self, fahrt_id):
        '''
        Gets all intermediate points of a transect with
        fahrt_id 'fahrt_id'
        '''
        transect_halt_points = self.session.query(MtPunkte).filter(MtPunkte.fahrt_id == fahrt_id, MtPunkte.transekt_id == 'KW ').all()
        course_turns = []
        for row in transect_halt_points:
            course_turns.append(str(row.laenge))
            course_turns.append(' ')
            course_turns.append(str(row.breite))
            course_turns.append(', ')
        return ''.join(course_turns)

    def get_transect_geometry(self, start_point, end_point, fahrt_id):
        '''
        Returns the geometry of the transect defined by
        start- and end_point
        '''
        intermediate_points = self.__get_intermediate_points(
            fahrt_id)
        transect_geometry = (
            WKTElement(
                'LINESTRING('
                + str(start_point.laenge)
                + ' ' + str(start_point.breite)
                + ', '
                + intermediate_points
                + str(end_point.laenge)
                + ' ' + str(end_point.breite)
                + ')',
                srid=4326
                )
            )
        return transect_geometry


def validate_test_class(test_class):
    '''
    Validate current entries in GUI
    '''
    test_class.evaluate()
    if test_class.missingEntries:
        test_class.instantiateMissingEntryDialog()
        if test_class.go_back:
            return False
    if test_class.nonValidEntries:
        test_class.instantiateNonValidEntryDialog()
    return True
