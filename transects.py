
# -*- coding: utf-8 -*-
'''
This module consists of the class representing transects
'''
from dialogs import MissingEntryDialog, NonValidEntryDialog
from geoalchemy2.elements import WKTElement
import math
from dictionaries import (
    DICT_SPECIES_2, DICT_TRANSECT_TYPE, DICT_SPECIES_FANCY, DICT_SEA_ID,
    DICT_SEA_ID_NUM, DICT_SIGHT, DICT_WIND_DIRECTION_2, DICT_WIND_ID,
    DICT_WIND_ID_NUM, DICT_WIND_ID_VELOCITY, DICT_CLOUDS, DICT_TRANSECT,

    )
from models import MtPunkte
import datetime

class Transect(object):
    '''
    This class is the base class for transects, the actual transects inherit it
    '''
    def __init__(self, Prog):
        '''
        Instantiation
        '''
        interface = Prog.ui
        tempTime = []
        self.dictSeaID = DICT_SEA_ID
        self.dictSeaIDNum = DICT_SEA_ID_NUM
        self.dictSight = DICT_SIGHT
        self.dictWindDirection = DICT_WIND_DIRECTION_2
        self.dictWindID = DICT_WIND_ID
        self.dictWindIDNum = DICT_WIND_ID_NUM
        self.dictWindIDVelocity = DICT_WIND_ID_VELOCITY
        self.dictClouds = DICT_CLOUDS
        self.dictTransect = DICT_TRANSECT
        read_date = interface.dateEdit.date()
        for i in interface.dateEdit.date().getDate():
            if len(str(i)) == 1:
                i = '0' + str(i)
            tempTime.append(str(i))
        self.datum = datetime.date(read_date.year(), read_date.month(), read_date.day()) #'-'.join(tempTime)

        hour = interface.timeEdit.time().hour()
        minute = interface.timeEdit.time().minute()
        self.zeit = datetime.datetime(2010,1,1,hour=hour, minute=minute) #str(hour) + ':' + str(minute)

        self.guide = interface.lineEditGuide.text()
        self.course = interface.lineEditCourse.text()
        self.courseWeek = interface.lineEditCourseWeek.text()
        self.schiff = interface.lineEditShipName.text()
        self.laenge = interface.lineEditLangenGrad.text()
        self.langenMinuten = interface.lineEditLangenMinuten.text()
        self.breite = interface.lineEditBreitenGrad.text()
        self.breitenMinuten = interface.lineEditBreitenMinuten.text()
        self.militaer = interface.checkBoxMilitaryActivity.isChecked()
        self.akustik = interface.checkBoxAcoustic.isChecked()
        self.segel = interface.checkBoxSail.isChecked()
        self.sea = interface.comboBoxSea.currentText()
        self.seaText = interface.comboBoxSea.currentText()
        self.seaID_num = self.dictSeaIDNum[unicode(interface.comboBoxSea.currentText())]
        self.sight = unicode(interface.comboBoxSight.currentText())
        self.sightText = interface.comboBoxSight.currentText()
        self.windDirection = self.dictWindDirection[unicode(
            interface.comboBoxWindDirection.currentText())]
        self.windStrength = interface.comboBoxWindStrength.currentText()
        self.windStrengthID_num = self.dictWindIDNum[unicode(
            interface.comboBoxWindStrength.currentText())]
        self.windStrengthVelocity = self.dictWindIDVelocity[unicode(
            self.windStrength)]
        self.clouds = self.dictClouds[unicode(
            interface.comboBoxClouds.currentText())]
        self.cloudsPercent = str(
            interface.comboBoxClouds.currentText()).split('%')[0].strip()
        self.fahrt_id = None
        self.fotos = Prog.ui.checkBoxFotos.isChecked()
        self.aufnahme = Prog.ui.checkBoxFotosMade.isChecked()
        self.missingEntryDialog = MissingEntryDialog(Prog)
        self.missingEntryDialog.ui.pushButtonNonValidBack.clicked.connect(
            self.dont_save)
        self.missingEntryDialog.ui.pushButtonSaveAnyway.clicked.connect(
            self.save_anyway)

        self.nonValidEntryDialog = NonValidEntryDialog(Prog, self)
        self.nonValidEntryDialog.ui.pushButtonOk.clicked.connect(
            self.jump_to_non_valid_entry)

        self.valid = True

    def instantiate_missing_entry_dialog(self):

        if len(self.missing_entries_list) == 1:
            warnText = u'Folgendes Feld ist nicht ausgefüllt:'
            missingValues = self.missing_entries_list[0]
        else:
            warnText = u'Folgende Felder sind nicht ausgefüllt:'
            missingValues = ', '.join(self.missing_entries_list)
        self.missingEntryDialog.ui.labelMissingEntries.setText(
            warnText +
            u'\n\n' + missingValues +
            u'\n\nTrotzdem speichern?'
            )
        self.go_back = True
        self.missingEntryDialog.exec_()

    def instantiate_non_valid_entry_dialog(self):
        if len(self.non_valid_entries_list) == 1:
            errorText = u'Die folgende Eingabe ist ungütlig:'
            non_valid_entries = self.non_valid_entries_list[0]
        else:
            errorText = u'Die folgenden Eingaben sind ungütlig:'
            non_valid_entries = ',\n'.join(self.non_valid_entries_list)
        self.nonValidEntryDialog.ui.labelNonValidEntries.setText(
            errorText
            + u'\n\n' + non_valid_entries
            )
        self.valid = True
        self.nonValidEntryDialog.exec_()

    def save_anyway(self):
        self.missingEntryDialog.close()
        self.go_back = False

    def dont_save(self):
        self.missingEntryDialog.close()
        self.go_back = True

    def jump_to_non_valid_entry(self):
        self.valid = False
        self.nonValidEntryDialog.close()

    def evaluate(self):
        self.missing_entries = False
        self.non_valid_entries = False
        self.missing_entries_list = []
        self.non_valid_entries_list = []

        if self.schiff == '' or self.schiff is None:
            self.missing_entries = True
            self.missing_entries_list.append('Schiffname')
        if self.guide == '' or self.guide is None:
            self.missing_entries = True
            self.missing_entries_list.append(u'Guide')
        if self.course == '' or self.course is None:
            self.missing_entries = True
            self.missing_entries_list.append(u'Kurs')
        elif not (float(self.course) <= 360):
            self.non_valid_entries = True
            self.non_valid_entries_list.append(u'Kurs-Wert über 360')
        if self.courseWeek == '' or self.courseWeek is None:
            self.missing_entries = True
            self.missing_entries_list.append(u'Kurswoche')
        if self.laenge == '' or self.laenge is None:
            self.missing_entries = True
            self.missing_entries_list.append(u'Längengrad')
        elif float(self.laenge) < -7:
            self.non_valid_entries = True
            self.non_valid_entries_list.append(u'Längegrad kleiner als -7')
        elif float(self.laenge) > 42:
            self.non_valid_entries = True
            self.non_valid_entries_list.append(u'Längengrad grösser als 42')
        if self.langenMinuten == '' or self.langenMinuten is None:
            self.missing_entries_list.append(u'Längenminuten')
            self.missing_entries = True
        elif float(self.langenMinuten) >= 60:
            self.non_valid_entries = True
            self.non_valid_entries_list.append(u'Längenminuten grösser als 60')
        if self.breite == '' or self.breite is None:
            self.missing_entries_list.append(u'Breitengrad')
            self.missing_entries = True
        elif float(self.breite) < 30:
            self.non_valid_entries = True
            self.non_valid_entries_list.append(u'Breitengrad kleiner als 30')
        elif float(self.breite) > 48:
            self.non_valid_entries = True
            self.non_valid_entries_list.append(u'Breitengrad grösser als 48')
        if self.breitenMinuten == '' or self.breitenMinuten is None:
            self.missing_entries_list.append(u'Breitenminuten')
            self.missing_entries = True
        elif float(self.breitenMinuten) >= 60:
            self.non_valid_entries = True
            self.non_valid_entries_list.append(u'Breitenminuten grösser als 60')

    def prepare_for_entry(self):
        if len(self.guide) < 2:
            self.guide = None
        else:
            self.guide = str(self.guide[0:2])
        try:
            self.schiff = str(self.schiff[0:50])
        except ValueError:
            self.schiff = None
        try:
            self.laenge = self.laenge.replace(',', '.')
            self.laenge = float(self.laenge)
        except ValueError:
            self.laenge = None
        try:
            self.langenMinuten = float(self.langenMinuten.replace(',', '.'))
        except ValueError:
            self.langenMinuten = None
        if not self.langenMinuten is None:
            self.laenge = self.laenge + (self.langenMinuten / 60)
        try:
            self.breite = self.breite.replace(',', '.')
            self.breite = float(self.breite)
        except ValueError:
            self.breite = None
        try:
            self.breitenMinuten = float(self.breitenMinuten.replace(',', '.'))
        except ValueError:
            self.breitenMinuten = None
        if not self.breitenMinuten is None:
            self.breite = self.breite + (self.breitenMinuten / 60)
        try:
            self.kurswoche = int(self.courseWeek)
        except ValueError:
            self.kurswoche = None
        try:
            self.kurs = float(self.course)
        except ValueError:
            self.kurs = None
        try:
            self.meer_id = str(self.sea)
        except ValueError:
            self.meer_id = None
        try:
            self.wind_id = str(self.windStrength)
        except ValueError:
            self.wind_id = None
        try:
            self.windrichtung_id = str(self.windDirection)
        except ValueError:
            self.windrichtung_id = None
        try:
            self.bewoelkung_id = str(self.clouds)
        except ValueError:
            self.bewoelkung_id = None
        try:
            self.sicht_id = str(self.sight)
        except ValueError:
            self.sicht_id = None
        if self.laenge != '' and self.breite != '':
            self.geom = WKTElement(
                'POINT('
                + str(self.laenge)
                + ' '
                + str(self.breite)
                + ')',
                srid=4326
                )
        else:
            self.geom = None


class PureTransect(Transect):

    def __init__(self, Prog):
        Transect.__init__(self, Prog)
        interface = Prog.ui
        self.transekt_id = self.dictTransect[unicode(
            interface.comboBoxTransectID.currentText())]

    def evaluate(self):
        Transect.evaluate(self)

    def prepare_for_entry(self):
        Transect.prepare_for_entry(self)


class AdvancedTransect(Transect):
    '''
    This is a enhancement of the base class for transect and itself is the
    base class for planction- and sight-transects
    '''
    def __init__(self, Prog):
        '''
        Instantiation
        '''
        Transect.__init__(self, Prog)
        

    def evaluate(self):
        '''
        Adds some checks relevant for evaluation of advanced-transects
        to the evaluation defined in the base class
        '''
        Transect.evaluate(self)
        if self.temperature == '' or self.temperature is None:
            self.missing_entries = True
            self.missing_entries_list.append(u'Oberflächentemperatur')
        elif float(self.temperature < 15):
            self.non_valid_entries = True
            self.non_valid_entries_list.append(
                u'Oberflächentemperatur unter 15 Grad')
        elif float(self.temperature) > 30:
            self.non_valid_entries = True
            self.non_valid_entries_list.append(
                u'Oberflächentemperatur über 30 Grad')
        if self.salinity == '' or self.salinity is None:
            self.missing_entries = True
            self.missing_entries_list.append(u'Oberflächensalinität')
        elif float(self.salinity) < 30:
            self.non_valid_entries = True
            self.non_valid_entries_list.append(u'Oberflächensalinität unter 30')
        elif float(self.salinity) > 40:
            self.non_valid_entries = True
            self.non_valid_entries_list.append(u'Oberflächensalinität über 40')
        if self.sight_depth == '' or self.sight_depth is None:
            self.missing_entries = True
            self.missing_entries_list.append(u'Sichttiefe')

    def prepare_for_entry(self):
        '''
        Adds some preparation for advanced-transects
        to the preparation defined in the base class
        '''
        Transect.prepare_for_entry(self)
        try:
            self.temperatur = float(self.temperature)
        except ValueError:
            self.temperatur = None
        try:
            self.salinitaet = float(self.salinity)
        except ValueError:
            self.salinitaet = None
        try:
            self.sichttiefe = float(self.sight_depth)
        except ValueError:
            self.sichttiefe = None
        self.messzeit = self.zeit


class PlanctonTransect(AdvancedTransect):
    '''
    This class represents a plancton-transect
    '''
    def __init__(self, Prog):
        '''
        Instantion
        '''
        AdvancedTransect.__init__(self, Prog)
        interface = Prog.ui
        self.temperature = interface.lineEditTemperaturePlancton.text()
        self.salinity = interface.lineEditSalinityPlancton.text()
        self.sight_depth = interface.lineEditSightDepthPlancton.text()
        self.wasserprobe = interface.checkBoxWaterSamplePlancton.isChecked()
        self.zooplanktonprobe = interface.checkBoxZooPlancton.isChecked()
        self.phytoplanktonprobe = interface.checkBoxPhytoPlancton.isChecked()
        self.transekt_id = u'AA'

    def evaluate(self):
        '''
        Adds some checks relevant for evaluation of plancton-transects
        to the evaluation defined in the base class
        '''
        AdvancedTransect.evaluate(self)
        if not (self.phyto_plancton or self.water_sample or self.zoo_plancton):
            self.missing_entries = True
            self.missing_entries_list.append(u'Messungsart')

    def prepare_for_entry(self):
        '''
        Adds some preparation for plancton-transects
        to the preparation defined in the base class
        '''
        AdvancedTransect.prepare_for_entry(self)


class SightTransect(AdvancedTransect):
    '''
    This class represents a sight-transect
    '''
    def __init__(self, Prog):
        AdvancedTransect.__init__(self, Prog)
        interface = Prog.ui
        self.temperature = interface.lineEditTemperatureSights.text()
        self.salinity = interface.lineEditSalinitySights.text()
        self.sight_depth = interface.lineEditSightDepthSights.text()
        self.course_whale = interface.lineEditCourseWhale.text()
        self.min_number = interface.lineEditNumberMin.text()
        self.max_number = interface.lineEditNumberMax.text()
        self.position_whale = interface.lineEditPositionWhale.text()
        self.parametric_distance = interface.lineEditParamDistance.text()
        self.duration = interface.lineEditDuration.text()
        self.distance_to_ship = interface.lineEditDistanceToShip.text()
        self.other_observations = (
            str(interface.textEditOtherObservations.toPlainText()).strip())
        self.special_behaviour = (
            str(interface.textEditSpecialBehaviour.toPlainText()).strip())
        self.ruhend = interface.checkBoxLazy.isChecked()
        self.langsam = interface.checkBoxSlowSwim.isChecked()
        self.schnell = interface.checkBoxFastSwim.isChecked()
        self.richtung_wechselnd = interface.checkBoxNotConstantSwim.isChecked()
        self.richtung_konstant= interface.checkBoxConstantSwim.isChecked()
        self.nahrungsaufnahme = interface.checkBoxEating.isChecked()
        self.tauchgang = interface.checkBoxDive.isChecked()
        self.fluke_sichtbar = interface.checkBoxFlukeSight.isChecked()
        self.spy_hopping = interface.checkBoxSpyHop.isChecked()
        self.flukenschlagen = interface.checkBoxFlukeHit.isChecked()
        self.paarung = interface.checkBoxMating.isChecked()
        self.spiel = interface.checkBoxPlaying.isChecked()
        self.annaeherung = interface.checkBoxCurious.isChecked()
        self.lautgebung = interface.checkBoxLoud.isChecked()
        self.blas = interface.checkBoxBlow.isChecked()
        self.blow_frequency = interface.lineEditBlowFrequency.text()
        self.in_begleitung = interface.checkBoxOtherSpecies.isChecked()
        self.other_species_name = interface.lineEditOtherSpecies.text()
        self.spruenge = interface.checkBoxJump.isChecked()
        self.breach_seitlich = interface.checkBoxBreachSide.isChecked()
        self.breach_rueckwaerts = interface.checkBoxBreachBack.isChecked()
        self.jungtiere = interface.checkBoxYoungOnes.isChecked()
        self.kaelber = interface.checkBoxChildren.isChecked()
        self.neugeborene = interface.checkBoxNewborn.isChecked()
        self.number_of_young_ones = interface.lineEditNumNewBorns.text()
        self.schwimmen_nah = interface.checkBoxCloseBoat.isChecked()
        self.bugwellen = interface.checkBoxRideFront.isChecked()
        self.seitlich = interface.checkBoxRideSide.isChecked()
        self.heckwellen = interface.checkBoxRideBack.isChecked()
        self.unter_schiff = interface.checkBoxRideDive.isChecked()
        self.soziales_verhalten = interface.checkBoxSocial.isChecked()
        self.gruppe_kompakt = interface.checkBoxCompact.isChecked()
        self.gruppe_locker = interface.checkBoxNotCompact.isChecked()
        self.species = DICT_SPECIES_2[unicode(
            interface.comboBoxSpecies.currentText())]
        if self.species == -1:
            self.species = None
        self.transect_id = DICT_TRANSECT_TYPE[unicode(
            interface.comboBoxTransectID.currentText())]
        self.art = unicode(interface.comboBoxSpecies.currentText())
        if self.species is not None:
            self.vulgaer = DICT_SPECIES_FANCY[unicode(
                interface.comboBoxSpecies.currentText())]
            if self.vulgaer == -1:
                self.vulgaer = None
        else:
            self.vulgaer = None

    def evaluate(self):
        '''
        Adds some checks relevant for evaluation of sight-transects
        to the evaluation defined in the base class
        '''
        AdvancedTransect.evaluate(self)
        if self.duration == '' or self.duration is None:
            self.missing_entries = True
            self.missing_entries_list.append(u'Dauer der Sichtung')
        if (
                not self.species == u'av'
                and not self.species == u'Mf'
                and not self.species == u'ms'
                and not self.species == u'pe'
                and not self.species == u'so'
                and not self.species == u'Son'
                and not self.species == u'ubak'
                and not self.species == -1):
            if self.course_whale == '' or self.course_whale is None:
                self.missing_entries = True
                self.missing_entries_list.append(u'Kurs Wal')
            elif float(self.course_whale) > 360:
                self.non_valid_entries = True
                self.non_valid_entries_list.append('Kurs Wal über 360')
            if self.min_number == '' or self.min_number is None:
                self.missing_entries = True
                self.missing_entries_list.append(u'Anzahl (mindestens)')
            if self.max_number == '' or self.max_number is None:
                self.missing_entries = True
                self.missing_entries_list.append(u'Anzahl (höchstens)')
            if self.position_whale == '' or self.position_whale is None:
                self.missing_entries = True
                self.missing_entries_list.append(u'Position Wal')
            elif float(self.position_whale) > 360:
                self.non_valid_entries = True
                self.non_valid_entries_list.append(u'Position Wal über 360')
            if self.parametric_distance == '' or self.parametric_distance is None:
                self.missing_entries = True
                self.missing_entries_list.append(u'Parametrische Distanz')
            if self.distance_to_ship == '' or self.distance_to_ship is None:
                self.missing_entries = True
                self.missing_entries_list.append(u'Distanz zum Schiff')
            if not (self.max_number == '' or self.min_number == '' or self.max_number is None or self.min_number is None):
                if int(self.max_number) < int(self.min_number):
                    self.non_valid_entries = True
                    self.non_valid_entries_list.append(
                        u'Maximale Anzahl grösser als minimale')
        if self.blow and (self.blow_frequency == '' or self.blow_frequency is None):
            self.missing_entries = True
            self.missing_entries_list.append(u'Blasfrequenz')
        if self.other_species and (self.other_species_name == '' or self.other_species_name is None):
            self.missing_entries = True
            self.missing_entries_list.append(u'Name anderer Spezies')
        if self.jump and not (self.breach_back or self.breach_side):
            self.missing_entries = True
            self.missing_entries_list.append(u'Sprungrichtung')
        if self.young_ones and not (self.newborn or self.children):
            self.missing_entries = True
            self.missing_entries_list.append(u'Kälber oder Neugeborene')
        if self.young_ones and (self.number_of_young_ones == '' or self.number_of_young_ones is None):
            self.missing_entries = True
            self.missing_entries_list.append(u'Anzahl Jungtiere')
        if (
                self.close_boat
                and not (
                    self.ride_back
                    or self.ride_dive
                    or self.ride_front
                    or self.ride_side
                    )
                ):
            self.missing_entries = True
            self.missing_entries_list.append(u'Schwimmart nah beim Schiff')
        if self.social and not (self.compact or self.not_compact):
            self.missing_entries = True
            self.missing_entries_list.append(u'Soziale Formation')

    def prepare_for_entry(self):
        '''
        Adds some preparation for sight-transects
        to the preparation defined in the base class
        '''
        AdvancedTransect.prepare_for_entry(self)
        self.transekt_id = str(self.transect_id)
        if self.species is None:
            self.art_id = None
        else:
            self.art_id = str(self.species)
        try:
            self.anzahl_min = int(self.min_number)
        except ValueError:
            self.anzahl_min = None
        try:
            self.anzahl_max = int(self.max_number)
        except ValueError:
            self.anzahl_max = None
        try:
            self.kurs_wal = float(self.course_whale)
        except ValueError:
            self.kurs_wal = None
        try:
            self.position_wal = float(self.position_whale)
        except ValueError:
            self.position_wal = None
        try:
            self.distanz_p = float(self.parametric_distance)
        except ValueError:
            self.distanz_p = None
        try:
            self.distanz_m = float(self.distance_to_ship)
        except ValueError:
            self.distanz_m = None
        try:
            self.begleitende_spezies = str(self.other_species_name[0:20])
        except ValueError:
            self.begleitende_spezies = None
        try:
            self.blasfrequenz = str(self.blow_frequency[0:20])
        except ValueError:
            self.blasfrequenz = None
        try:
            self.anzahl_jungtiere = str(self.number_of_young_ones)
        except ValueError:
            self.anzahl_jungtiere = None
        try:
            self.anderes_verhalten = self.special_behaviour[0:200]
        except ValueError:
            self.anderes_verhalten = None
        try:
            self.zusaetzliche_beobachtungen = str(self.other_observations[0:200])
        except ValueError:
            self.zusaetzliche_beobachtungen = None
        try:
            self.dauer = float(self.duration)
        except ValueError:
            self.dauer = None
        if self.laenge != '' and self.breite != '' and self.transekt_id == 'S':
            if self.distanz_p is not None and self.position_wal != '':
                distance_parameter = self.distanz_p
                rad_per_reticle = 0.00497
                height = 3.0
                earth_radius = 6366
                ambigous_constant = (
                    math.sqrt(
                        2
                        * earth_radius
                        * height
                        / 1000
                        + math.pow(
                            (height/1000),
                            2)
                        )
                    )
                if distance_parameter == 0:
                    distance = ambigous_constant
                else:
                    angle = math.atan(ambigous_constant / earth_radius)

                    sin_part = math.sin(
                        angle + distance_parameter * rad_per_reticle)
                    cos_part = math.cos(
                        angle + distance_parameter * rad_per_reticle)
                    squared_part = math.pow(earth_radius, 2)
                    second_squared_part = math.pow(
                        (earth_radius + height / 1000)
                        * cos_part, 2
                        )
                    root_part = math.sqrt(squared_part - second_squared_part)
                    distance = (
                        (
                            earth_radius
                            + height
                            / 1000
                            )
                        * sin_part
                        - root_part
                        )

                distance = distance
                azimuth = self.position_wal

                self.breite_wal = (
                    math.asin(
                        math.sin(self.breite * math.pi / 180.0)
                        * math.cos(distance/earth_radius)
                        + math.cos(self.breite * math.pi / 180.0)
                        * math.sin(distance / earth_radius)
                        * math.cos(azimuth * math.pi / 180.0)
                        )
                    * 180
                    / math.pi
                    )
                self.laenge_wal = (
                    self.laenge
                    + math.atan2(
                        math.sin(azimuth * math.pi / 180.0)
                        * math.sin(distance / earth_radius)
                        * math.cos(self.laenge * math.pi / 180.0),
                        math.cos(distance / earth_radius)
                        - math.sin(self.laenge * math.pi / 180.0)
                        * math.sin(self.breite_wal * math.pi / 180.0)
                        )
                    )
            else:
                self.laenge_wal = self.laenge
                self.breite_wal = self.breite
        else:
            self.laenge_wal = None
            self.breite_wal = None

        if (
                self.transekt_id == 'S'
                and self.kurs != ''
                and self.kurs is not None
                and self.kurs_wal != ''
                and self.kurs_wal is not None
                ):
            self.sichtungswinkel = self.kurs_wal - self.kurs
            if self.sichtungswinkel > 180:
                self.sichtungswinkel = -1 * (360 - self.sichtungswinkel)
        else:
            self.sichtungswinkel = None
