# -*- coding: utf-8 -*-
'''
This Module consists of different classes and functions
that help the application to apply changes to the GUI,
make database-connections and other stuff
'''
from PyQt4 import QtGui, Qt
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table
import time
from config import OnlineConfiguration

def set_validators(interface):
    '''
    Instantiates all the input-fields-validators according
    to database-constraints
    '''
    interface.lineEditLangenGrad.setValidator(
        QtGui.QDoubleValidator(-7, 42, 10))
    interface.lineEditLangenMinuten.setValidator(
        QtGui.QDoubleValidator(0, 360, 10))
    interface.lineEditBreitenGrad.setValidator(
        QtGui.QDoubleValidator(30, 48, 10))
    interface.lineEditBreitenMinuten.setValidator(
        QtGui.QDoubleValidator(0, 360, 10))
    interface.lineEditCourse.setValidator(QtGui.QDoubleValidator(0, 360, 10))
    interface.lineEditCourseWeek.setValidator(QtGui.QIntValidator(0, 52))
    interface.timeEdit.setDisplayFormat(u"hh:mm")
    interface.lineEditTemperaturePlancton.setValidator(
        QtGui.QDoubleValidator(15, 30, 5))
    interface.lineEditSalinityPlancton.setValidator(
        QtGui.QDoubleValidator(30, 40, 5))
    interface.lineEditSightDepthPlancton.setValidator(
        QtGui.QDoubleValidator(0, 500, 5))
    interface.lineEditTemperatureSights.setValidator(
        QtGui.QDoubleValidator(15, 30, 5))
    interface.lineEditSalinitySights.setValidator(
        QtGui.QDoubleValidator(30, 40, 5))
    interface.lineEditSightDepthSights.setValidator(
        QtGui.QDoubleValidator(0, 500, 5))
    interface.lineEditCourseWhale.setValidator(
        QtGui.QDoubleValidator(0, 360, 5))
    interface.lineEditNumberMin.setValidator(QtGui.QIntValidator(0, 1000))
    interface.lineEditNumberMax.setValidator(QtGui.QIntValidator(0, 1000))
    interface.lineEditPositionWhale.setValidator(
        QtGui.QDoubleValidator(0, 360, 5))
    interface.lineEditParamDistance.setValidator(
        QtGui.QDoubleValidator(0, 100, 10))
    interface.lineEditDistanceToShip.setValidator(
        QtGui.QDoubleValidator(0, 100000, 5))
    interface.lineEditNumNewBorns.setValidator(QtGui.QIntValidator(1, 500))


class DatabaseHandler(object):
    '''
    Class responsible for serving all database-related needed things
    '''
    def __init__(self):
        '''Instantiates to None
        '''
        self.engine = None
        self.error_text_entry = (
            u'''Leider konnte die Verbindung mit der
            Datenbank nicht hergestellt werden.
            \nBeachten Sie untenstehende Fehlermeldung
            und ändern sie die Werte entsprechend''')
        self.tables = {}
        self.connection = None
        self.meta = None

    def connect_to_database(self, warn_dialog):
        '''
        Connects to the database
        '''
        try:
            self.engine = create_engine(
                OnlineConfiguration.SQLALCHEMY_DATABASE_URI)
            self.engine.connect()
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            self.meta = MetaData()
            self.tables['points'] = Table(
                'mt_punkte',
                self.meta,
                autoload=True,
                autoload_with=self.engine)
            self.tables['transects'] = Table(
                'mt_fahrten',
                self.meta,
                autoload=True,
                autoload_with=self.engine)
            self.tables['tt_others'] = Table(
                'tt_andere', self.meta,
                autoload=True,
                autoload_with=self.engine)
            self.tables['tt_observations'] = Table(
                'tt_beobachtungen', self.meta,
                autoload=True,
                autoload_with=self.engine)
            self.connection = self.engine.connect()
            return 1
        except OperationalError:
            warn_dialog.exec_()
            return 0

    def get_engine(self):
        '''
        Returns the engine of the database
        '''
        return self.engine

    def get_connection(self):
        '''
        Returns the connection of the database
        '''
        return self.connection


class CheckboxRestrictor(object):
    '''
    Controls the availibilty of checkboxes of the GUI
    '''
    def __init__(self, frame):
        '''
        Instantiation, the GUI 'frame' is passed to the restrictor
        '''
        self.frame = frame

    def connect_actions(self):
        '''
        Connects the control-checkboxes to the restrict-functions
        '''
        self.frame.ui.checkBoxSocial.clicked.connect(self.social_clicked)
        self.frame.ui.checkBoxAcoustic.clicked.connect(self.fotos_clicked)
        self.frame.ui.checkBoxBlow.clicked.connect(self.blow_clicked)
        self.frame.ui.checkBoxOtherSpecies.clicked.connect(
            self.other_species_clicked)
        self.frame.ui.checkBoxJump.clicked.connect(self.jump_clicked)
        self.frame.ui.checkBoxDive.clicked.connect(self.dive_clicked)
        self.frame.ui.checkBoxCloseBoat.clicked.connect(self.close_boat_clicked)

    def social_clicked(self):
        '''
        Controls the checkboxes in the social-group
        '''
        box = self.frame.sender()
        if box.isChecked():
            self.frame.ui.checkBoxPlaying.setEnabled(True)
            self.frame.ui.checkBoxMating.setEnabled(True)
            self.frame.ui.labelPlaying.setEnabled(True)
            self.frame.ui.labelMating.setEnabled(True)
        else:
            self.frame.ui.checkBoxPlaying.setEnabled(False)
            self.frame.ui.checkBoxPlaying.setCheckState(0)
            self.frame.ui.checkBoxMating.setEnabled(False)
            self.frame.ui.checkBoxMating.setCheckState(0)
            self.frame.ui.labelPlaying.setEnabled(False)
            self.frame.ui.labelMating.setEnabled(False)

    def fotos_clicked(self):
        '''
        Controls the checkboxes in the fotos-group
        '''
        box = self.frame.sender()
        if box.isChecked():
            self.frame.ui.checkBoxFotosMade.setEnabled(True)
            self.frame.ui.labelFotosMade.setEnabled(True)
        else:
            self.frame.ui.checkBoxFotosMade.setEnabled(False)
            self.frame.ui.checkBoxFotosMade.setCheckState(0)
            self.frame.ui.labelFotosMade.setEnabled(False)

    def blow_clicked(self):
        '''
        Controls the checkboxes in the blow-group
        '''
        box = self.frame.sender()
        if box.isChecked():
            self.frame.ui.labelBlowFrequency.setEnabled(True)
            self.frame.ui.lineEditBlowFrequency.setEnabled(True)
        else:
            self.frame.ui.labelBlowFrequency.setEnabled(False)
            self.frame.ui.lineEditBlowFrequency.setEnabled(False)
            self.frame.ui.lineEditBlowFrequency.setText('')

    def other_species_clicked(self):
        '''
        Controls the checkboxes in the other-species-group
        '''
        box = self.frame.sender()
        if box.isChecked():
            self.frame.ui.labelOtherSpecies.setEnabled(True)
            self.frame.ui.lineEditOtherSpecies.setEnabled(True)
        else:
            self.frame.ui.labelOtherSpecies.setEnabled(False)
            self.frame.ui.lineEditOtherSpecies.setEnabled(False)
            self.frame.ui.lineEditOtherSpecies.setText('')

    def jump_clicked(self):
        '''
        Controls the checkboxes in the jump-group
        '''
        box = self.frame.sender()
        if box.isChecked():
            self.frame.ui.labelBreachBack.setEnabled(True)
            self.frame.ui.checkBoxBreachBack.setEnabled(True)
            self.frame.ui.labelBreachSide.setEnabled(True)
            self.frame.ui.checkBoxBreachSide.setEnabled(True)
        else:
            self.frame.ui.labelBreachBack.setEnabled(False)
            self.frame.ui.checkBoxBreachBack.setEnabled(False)
            self.frame.ui.checkBoxBreachBack.setCheckState(0)
            self.frame.ui.labelBreachSide.setEnabled(False)
            self.frame.ui.checkBoxBreachSide.setEnabled(False)
            self.frame.ui.checkBoxBreachSide.setCheckState(0)

    def dive_clicked(self):
        '''
        Controls the checkboxes in the young-ones-group
        '''
        box = self.frame.sender()
        if box.isChecked():
            self.frame.ui.labelFlukeSight.setEnabled(True)
            self.frame.ui.checkBoxFlukeSight.setEnabled(True)
        else:
            self.frame.ui.checkBoxFlukeSight.setEnabled(False)
            self.frame.ui.checkBoxFlukeSight.setCheckState(0)

    def close_boat_clicked(self):
        '''
        Controls the checkboxes in the close-boat-group
        '''
        box = self.frame.sender()
        if box.isChecked():
            self.frame.ui.labelRideBack.setEnabled(True)
            self.frame.ui.labelRideDive.setEnabled(True)
            self.frame.ui.labelRideFront.setEnabled(True)
            self.frame.ui.labelRideSide.setEnabled(True)
            self.frame.ui.checkBoxRideBack.setEnabled(True)
            self.frame.ui.checkBoxRideDive.setEnabled(True)
            self.frame.ui.checkBoxRideFront.setEnabled(True)
            self.frame.ui.checkBoxRideSide.setEnabled(True)
        else:
            self.frame.ui.labelRideBack.setEnabled(False)
            self.frame.ui.labelRideDive.setEnabled(False)
            self.frame.ui.labelRideFront.setEnabled(False)
            self.frame.ui.labelRideSide.setEnabled(False)
            self.frame.ui.checkBoxRideBack.setEnabled(False)
            self.frame.ui.checkBoxRideBack.setCheckState(0)
            self.frame.ui.checkBoxRideDive.setEnabled(False)
            self.frame.ui.checkBoxRideDive.setCheckState(0)
            self.frame.ui.checkBoxRideFront.setEnabled(False)
            self.frame.ui.checkBoxRideFront.setCheckState(0)
            self.frame.ui.checkBoxRideSide.setEnabled(False)
            self.frame.ui.checkBoxRideSide.setCheckState(0)


class GuiHandler(object):
    def __init__(self, frame, language_dict):
        self.frame = frame
        self.language_dict = language_dict
        self.interface = frame.ui

    def set_labels(self):
        self.interface.comboBoxSea.setItemText(0, self.language_dict['calm'])
        self.interface.comboBoxSea.setItemText(1, self.language_dict['calm_plus'])
        self.interface.comboBoxSea.setItemText(2, self.language_dict['fair'])
        self.interface.comboBoxSea.setItemText(3, self.language_dict['calm_plus'])
        self.interface.comboBoxSea.setItemText(4, self.language_dict['slightly_uncalm'])
        self.interface.comboBoxSea.setItemText(5, self.language_dict['slightly_uncalm_plus'])
        self.interface.comboBoxSea.setItemText(6, self.language_dict['uncalm'])
        self.interface.comboBoxSea.setItemText(7, self.language_dict['slightly_to_very_uncalm'])
        self.interface.comboBoxSea.setItemText(8, self.language_dict['very_uncalm'])
        self.interface.comboBoxSea.setItemText(9, self.language_dict['uncalm_plus'])
        self.interface.comboBoxSea.setItemText(10, self.language_dict['stormy'])
        self.interface.comboBoxSea.setItemText(11, self.language_dict['stormy_plus'])
        
        self.interface.comboBoxSight.setItemText(0, self.language_dict['good'])
        self.interface.comboBoxSight.setItemText(1, self.language_dict['mediocer'])
        self.interface.comboBoxSight.setItemText(2, self.language_dict['bad'])
        
        self.interface.comboBoxWindStrength.setItemText(0, self.language_dict['smoke_straight'])
        self.interface.comboBoxWindStrength.setItemText(1, self.language_dict['very_quiet_draft'])
        self.interface.comboBoxWindStrength.setItemText(2, self.language_dict['quiet_draft'])
        self.interface.comboBoxWindStrength.setItemText(3, self.language_dict['very_quiet_breeze'])
        self.interface.comboBoxWindStrength.setItemText(4, self.language_dict['quiet_breeze'])
        self.interface.comboBoxWindStrength.setItemText(5, self.language_dict['very_weak_breeze'])
        self.interface.comboBoxWindStrength.setItemText(6, self.language_dict['weak_breeze'])
        self.interface.comboBoxWindStrength.setItemText(7, self.language_dict['very_mediocer_breeze'])
        self.interface.comboBoxWindStrength.setItemText(8, self.language_dict['mediocer_breeze'])
        self.interface.comboBoxWindStrength.setItemText(9, self.language_dict['very_fresh_breeze'])
        self.interface.comboBoxWindStrength.setItemText(10, self.language_dict['fresh_breeze'])
        self.interface.comboBoxWindStrength.setItemText(11, self.language_dict['strong_wind'])
        self.interface.comboBoxWindStrength.setItemText(12, self.language_dict['stiff_wind'])
        self.interface.comboBoxWindStrength.setItemText(13, self.language_dict['barely_stormy_wind'])
        self.interface.comboBoxWindStrength.setItemText(14, self.language_dict['stormy_wind'])
        self.interface.comboBoxWindStrength.setItemText(15, self.language_dict['storm'])
        self.interface.comboBoxWindStrength.setItemText(16, self.language_dict['heavy_storm'])
        self.interface.comboBoxWindStrength.setItemText(17, self.language_dict['small_hurrican'])
        self.interface.comboBoxWindStrength.setItemText(18, self.language_dict['hurrican'])
        
        self.interface.comboBoxWindDirection.setItemText(0, self.language_dict['no_wind'])
        self.interface.comboBoxWindDirection.setItemText(1, self.language_dict['E'])
        self.interface.comboBoxWindDirection.setItemText(2, self.language_dict['ENE'])
        self.interface.comboBoxWindDirection.setItemText(3, self.language_dict['ESE'])
        self.interface.comboBoxWindDirection.setItemText(4, self.language_dict['N'])
        self.interface.comboBoxWindDirection.setItemText(5, self.language_dict['NE'])
        self.interface.comboBoxWindDirection.setItemText(6, self.language_dict['NNE'])
        self.interface.comboBoxWindDirection.setItemText(7, self.language_dict['NW'])
        self.interface.comboBoxWindDirection.setItemText(8, self.language_dict['NNW'])
        self.interface.comboBoxWindDirection.setItemText(9, self.language_dict['S'])
        self.interface.comboBoxWindDirection.setItemText(10, self.language_dict['SE'])
        self.interface.comboBoxWindDirection.setItemText(11, self.language_dict['SSE'])
        self.interface.comboBoxWindDirection.setItemText(12, self.language_dict['SW'])
        self.interface.comboBoxWindDirection.setItemText(13, self.language_dict['SSE'])
        self.interface.comboBoxWindDirection.setItemText(14, self.language_dict['W'])
        self.interface.comboBoxWindDirection.setItemText(15, self.language_dict['WNW'])
        self.interface.comboBoxWindDirection.setItemText(16, self.language_dict['WSW'])
        
        self.interface.comboBoxTransectID.setItemText(0, self.language_dict['please_choose'])
        self.interface.comboBoxTransectID.setItemText(1, self.language_dict['A'])
        self.interface.comboBoxTransectID.setItemText(2, self.language_dict['probe_combo'])
        self.interface.comboBoxTransectID.setItemText(3, self.language_dict['Ak'])
        self.interface.comboBoxTransectID.setItemText(4, self.language_dict['Ako'])
        self.interface.comboBoxTransectID.setItemText(5, self.language_dict['begin'])
        self.interface.comboBoxTransectID.setItemText(6, self.language_dict['end'])
        self.interface.comboBoxTransectID.setItemText(7, self.language_dict['FS'])
        self.interface.comboBoxTransectID.setItemText(8, self.language_dict['course_change'])
        self.interface.comboBoxTransectID.setItemText(9, self.language_dict['S'])
        self.interface.comboBoxTransectID.setItemText(10, self.language_dict['ST'])
        self.interface.comboBoxTransectID.setItemText(11, self.language_dict['W'])
        self.interface.comboBoxTransectID.setItemText(12, self.language_dict['WA'])
        self.interface.comboBoxTransectID.setItemText(13, self.language_dict['WB'])
        self.interface.comboBoxSpecies.setItemText(0, self.language_dict['please_choose'])
        self.interface.comboBoxSpecies.setItemText(1, self.language_dict['av'])
        self.interface.comboBoxSpecies.setItemText(2, self.language_dict['Ba'])
        self.interface.comboBoxSpecies.setItemText(3, self.language_dict['Bp'])
        self.interface.comboBoxSpecies.setItemText(4, self.language_dict['Dd'])
        self.interface.comboBoxSpecies.setItemText(5, self.language_dict['Gg'])
        self.interface.comboBoxSpecies.setItemText(6, self.language_dict['Gm'])
        self.interface.comboBoxSpecies.setItemText(7, self.language_dict['Mf'])
        self.interface.comboBoxSpecies.setItemText(8, self.language_dict['Mn'])
        self.interface.comboBoxSpecies.setItemText(9, self.language_dict['ms'])
        self.interface.comboBoxSpecies.setItemText(10, self.language_dict['pe'])
        self.interface.comboBoxSpecies.setItemText(11, self.language_dict['Pm'])
        self.interface.comboBoxSpecies.setItemText(12, self.language_dict['Sc'])
        self.interface.comboBoxSpecies.setItemText(13, self.language_dict['Sf'])
        self.interface.comboBoxSpecies.setItemText(14, self.language_dict['so'])
        self.interface.comboBoxSpecies.setItemText(15, self.language_dict['Son'])
        self.interface.comboBoxSpecies.setItemText(16, self.language_dict['Tt'])
        self.interface.comboBoxSpecies.setItemText(17, self.language_dict['ubak'])
        self.interface.comboBoxSpecies.setItemText(18, self.language_dict['ubd'])
        self.interface.comboBoxSpecies.setItemText(19, self.language_dict['ubw'])
        self.interface.comboBoxSpecies.setItemText(20, self.language_dict['Zc'])
        
        self.interface.labelTitle.setText(self.language_dict['title'])
        self.interface.labelSights.setText(self.language_dict['sight_details'])
        self.interface.labelMetaTime.setText(self.language_dict['day'])
        self.interface.labelDate.setText(self.language_dict['date'])
        self.interface.labelTime.setText(self.language_dict['time'])
        self.interface.labelPosition.setText(self.language_dict['position'])
        self.interface.labelBreitenGrad.setText(self.language_dict['breiten_grad'])
        self.interface.labelBreitenminuten.setText(self.language_dict['breiten_min'])
        self.interface.labelLangenGrad.setText(self.language_dict['laengen_grad'])
        self.interface.labelLangenMinuten.setText(self.language_dict['laengen_min'])
        self.interface.labelMeteo.setText(self.language_dict['meteo'])
        self.interface.labelSea.setText(self.language_dict['sea'])
        self.interface.labelClouds.setText(self.language_dict['clouds'])
        self.interface.labelSight.setText(self.language_dict['sight'])
        self.interface.labelWindStrength.setText(self.language_dict['wind_strength'])
        self.interface.labelWindDirection.setText(self.language_dict['wind_dir'])
        self.interface.labelGeneral.setText(self.language_dict['misc'])
        self.interface.labelCourseWeek.setText(self.language_dict['course_week'])
        self.interface.labelGuide.setText(self.language_dict['guide'])
        self.interface.labelCourse.setText(self.language_dict['nautic_course'])
        self.interface.labelShipName.setText(self.language_dict['ship_name'])
        self.interface.labelAcoustic.setText(self.language_dict['acoustic'])
        self.interface.labelSail.setText(self.language_dict['sail'])
        self.interface.labelFotos.setText(self.language_dict['fotos'])
        self.interface.labelFotosMade.setText(self.language_dict['fotos_made'])
        self.interface.labelMilitaryActivity.setText(self.language_dict['military_activity'])

        self.interface.labelTransectType.setText(self.language_dict['transect_type'])

        self.interface.pushButtonPlanctonData.setText(self.language_dict['probe'])
        self.interface.pushButtonSightData.setText(self.language_dict['sight_data'])
        self.interface.labelMeasurementsPlancton.setText(self.language_dict['measurements'])
        self.interface.labelTemperaturePlancton.setText(self.language_dict['surface_temp'])
        self.interface.labelSalinityPlancton.setText(self.language_dict['salinity'])
        self.interface.labelTimeSightDepthPlancton.setText(self.language_dict['sight_depth'])
        self.interface.labelPlancton.setText(self.language_dict['plancton'])
        self.interface.labelPhytoPlancton.setText(self.language_dict['phyto_plancton'])
        self.interface.labelZooPlancton.setText(self.language_dict['zoo_plancton'])
        self.interface.labelWaterSample.setText(self.language_dict['water_sample'])
        self.interface.pushButtonGoBackPlancton.setText(self.language_dict['back_to_transect'])
        self.interface.pushButtonSendOffPlanctonData.setText(self.language_dict['save'])
        self.interface.labelMeasurementsSights.setText(self.language_dict['measurements'])
        self.interface.labelTemperatureSights.setText(self.language_dict['surface_temp'])
        self.interface.labelSalinitySights.setText(self.language_dict['salinity'])
        self.interface.labelTimeSightDepthSights.setText(self.language_dict['sight_depth'])
        self.interface.labelSpecies.setText(self.language_dict['kind'])
        self.interface.labelCourseWhale.setText(self.language_dict['course_whale'])
        self.interface.labelNumberMin.setText(self.language_dict['min_count'])
        self.interface.labelNumberMax.setText(self.language_dict['max_count'])
        self.interface.labelPositionWhale.setText(self.language_dict['position_whale'])
        self.interface.labelParamDistance.setText(self.language_dict['param_dist'])
        self.interface.labelDuration.setText(self.language_dict['duration_sight'])
        self.interface.labelDistanceToShip.setText(self.language_dict['dist_ship'])
        self.interface.labelOtherObservations.setText(self.language_dict['other_observations'])
        self.interface.labelSpecialBehaviour.setText(self.language_dict['other_behaviour'])

        self.interface.pushButtonGoBackSight.setText(self.language_dict['back_to_transect'])
        self.interface.pushButtonGoToDetailsSight.setText(self.language_dict['behaviour'])
        self.interface.labelLazy.setText(self.language_dict['stationary'])
        self.interface.labelSlowSwim.setText(self.language_dict['slow_swim'])
        self.interface.labelFastSwim.setText(self.language_dict['fast_swim'])
        self.interface.labelNotConstantSwim.setText(self.language_dict['swim_change'])
        self.interface.labelConstantSwim.setText(self.language_dict['swim_const'])
        self.interface.labelEating.setText(self.language_dict['eating'])
        self.interface.labelDive.setText(self.language_dict['dive'])
        self.interface.labelFlukeSight.setText(self.language_dict['fluke_sight'])
        self.interface.labelSpyHop.setText(self.language_dict['spy_hopping'])
        self.interface.labelFlukeHit.setText(self.language_dict['fluke_hit'])
        self.interface.labelMating.setText(self.language_dict['mate'])
        self.interface.labelPlaying.setText(self.language_dict['play'])
        self.interface.labelCurious.setText(self.language_dict['curious'])
        self.interface.labelLoud.setText(self.language_dict['loud'])
        self.interface.labelBlow.setText(self.language_dict['blow'])
        self.interface.labelBlowFrequency.setText(self.language_dict['blow_frequency'])
        self.interface.labelOtherSpecies.setText(self.language_dict['other_species_name'])
        self.interface.labelOtherSpeciesBox.setText(self.language_dict['with_other'])
        self.interface.labelJump.setText(self.language_dict['jump'])
        self.interface.labelBreachSide.setText(self.language_dict['breach_side'])
        self.interface.labelBreachBack.setText(self.language_dict['breach_back'])
        self.interface.labelYoungOnes.setText(self.language_dict['young_ones'])
        self.interface.labelChildren.setText(self.language_dict['calves'])
        self.interface.labelNewBorn.setText(self.language_dict['newborn'])
        self.interface.labelNumNewBorns.setText(self.language_dict['num_newborn'])
        self.interface.labelCloseBoat.setText(self.language_dict['swim_close'])
        self.interface.labelRideFront.setText(self.language_dict['ride'])
        self.interface.labelRideSide.setText(self.language_dict['side'])
        self.interface.labelRideBack.setText(self.language_dict['back_ride'])
        self.interface.labelRideDive.setText(self.language_dict['dive_ship'])
        self.interface.labelSocial.setText(self.language_dict['social_int'])
        self.interface.labelCompact.setText(self.language_dict['compact_group'])
        self.interface.labelNotCompact.setText(self.language_dict['non_compact_group'])
        self.interface.pushButtonGoBackSightDetails.setText(self.language_dict['back'])


    def set_sight_details_checkboxes_default(self):
        self.interface.checkBoxBlow.setCheckState(0)
        self.interface.checkBoxBreachBack.setCheckState(0)
        self.interface.checkBoxBreachSide.setCheckState(0)
        self.interface.checkBoxChildren.setCheckState(0)
        self.interface.checkBoxCloseBoat.setCheckState(0)
        self.interface.checkBoxCompact.setCheckState(0)
        self.interface.checkBoxConstantSwim.setCheckState(0)
        self.interface.checkBoxCurious.setCheckState(0)
        self.interface.checkBoxDive.setCheckState(0)
        self.interface.checkBoxEating.setCheckState(0)
        self.interface.checkBoxFlukeHit.setCheckState(0)
        self.interface.checkBoxFlukeSight.setCheckState(0)
        self.interface.checkBoxFotos.setCheckState(0)
        self.interface.checkBoxFotosMade.setCheckState(0)
        self.interface.checkBoxJump.setCheckState(0)
        self.interface.checkBoxLazy.setCheckState(0)
        self.interface.checkBoxLoud.setCheckState(0)
        self.interface.checkBoxMating.setCheckState(0)
        self.interface.checkBoxNewborn.setCheckState(0)
        self.interface.checkBoxNotCompact.setCheckState(0)
        self.interface.checkBoxOtherSpecies.setCheckState(0)
        self.interface.checkBoxPlaying.setCheckState(0)
        self.interface.checkBoxRideBack.setCheckState(0)
        self.interface.checkBoxRideDive.setCheckState(0)
        self.interface.checkBoxRideFront.setCheckState(0)
        self.interface.checkBoxRideSide.setCheckState(0)
        self.interface.checkBoxSlowSwim.setCheckState(0)
        self.interface.checkBoxSocial.setCheckState(0)
        self.interface.checkBoxSpyHop.setCheckState(0)
        self.interface.checkBoxYoungOnes.setCheckState(0)
        
    def set_sight_details_checkboxes__enabled_default(self):
        
        self.interface.checkBoxBreachBack.setEnabled(False)
        self.interface.checkBoxBreachSide.setEnabled(False)
        self.interface.checkBoxCompact.setEnabled(False)
        self.interface.checkBoxFotosMade.setEnabled(False)
        self.interface.checkBoxNewborn.setEnabled(False)
        self.interface.checkBoxNotCompact.setEnabled(False)
        self.interface.checkBoxRideBack.setEnabled(False)
        self.interface.checkBoxRideDive.setEnabled(False)
        self.interface.checkBoxRideFront.setEnabled(False)
        self.interface.checkBoxRideSide.setEnabled(False)
        self.interface.lineEditBlowFrequency.setEnabled(False)
        self.interface.lineEditOtherSpecies.setEnabled(False)
        self.interface.labelBlowFrequency.setEnabled(False)
        self.interface.labelOtherSpecies.setEnabled(False)
        self.interface.labelBreachBack.setEnabled(False)
        self.interface.labelBreachSide.setEnabled(False)
        self.interface.labelPlaying.setEnabled(False)
        self.interface.labelMating.setEnabled(False)
        self.interface.labelFotosMade.setEnabled(False)
        self.interface.labelRideBack.setEnabled(False)
        self.interface.labelRideDive.setEnabled(False)
        self.interface.labelRideFront.setEnabled(False)
        self.interface.labelRideSide.setEnabled(False)
        self.interface.labelCompact.setEnabled(False)
        self.interface.labelNotCompact.setEnabled(False)
    
    def set_sight_details_lineedits_default(self):
        self.interface.lineEditDuration.setText('')
        self.interface.lineEditNumNewBorns.setText('')
        self.interface.lineEditOtherSpecies.setText('')
        self.interface.lineEditBlowFrequency.setText('')
        

    
    def set_sight_combobox_default(self):
        self.interface.comboBoxSpecies.setCurrentIndex(0)
    
    def set_sight_lineedit_default(self):
        self.interface.lineEditTemperatureSights.setText('')
        self.interface.lineEditSalinitySights.setText('')
        self.interface.lineEditSightDepthSights.setText('')
        self.interface.lineEditCourseWhale.setText('')
        self.interface.lineEditNumberMin.setText('')
        self.interface.lineEditNumberMax.setText('')
        self.interface.lineEditPositionWhale.setText('')
        self.interface.lineEditParamDistance.setText('')
        self.interface.lineEditDuration.setText('')
        self.interface.lineEditDistanceToShip.setText('')
        self.interface.textEditOtherObservations.setText('')
        self.interface.textEditSpecialBehaviour.setText('')


    def set_plancton_lineedit_default(self):
        self.interface.lineEditSalinityPlancton.setText('')
        self.interface.lineEditSightDepthPlancton.setText('')
        self.interface.lineEditTemperaturePlancton.setText('')

    def set_plancton_checkboxes_default(self):
        self.interface.checkBoxZooPlancton.setCheckState(0)
        self.interface.checkBoxPhytoPlancton.setCheckState(0)
        self.interface.checkBoxWaterSamplePlancton.setCheckState(0)

    def set_main_frame_post_entry_lineedits(self):
        self.interface.lineEditBreitenGrad.setText('43')
        self.interface.lineEditBreitenMinuten.setText('')
        self.interface.lineEditLangenGrad.setText('')
        self.interface.lineEditLangenMinuten.setText('')
        self.interface.lineEditCourse.setText('')

    def set_main_frame_post_entry_checkboxes(self):
        self.interface.comboBoxClouds.setCurrentIndex(0)
        self.interface.comboBoxSight.setCurrentIndex(0)
        self.interface.comboBoxWindDirection.setCurrentIndex(0)
        self.interface.comboBoxWindStrength.setCurrentIndex(0)
        self.interface.checkBoxSail.setCheckState(0)
        self.interface.checkBoxMilitaryActivity.setCheckState(0)
        self.interface.comboBoxTransectID.setCurrentIndex(0)
        self.interface.comboBoxSea.setCurrentIndex(2)
        self.interface.checkBoxAcoustic.setCheckState(2)
        
    def set_main_frame_lineedits_default(self):
        self.interface.lineEditBreitenMinuten.setText('')
        self.interface.lineEditLangenGrad.setText('')
        self.interface.lineEditLangenMinuten.setText('')
        self.interface.lineEditCourseWeek.setText('')
        self.interface.lineEditGuide.setText('')
        self.interface.lineEditCourse.setText('')
        self.interface.lineEditShipName.setText('')

    def set_main_frame_boxes_default(self):
        
        self.interface.comboBoxClouds.setCurrentIndex(0)
        self.interface.comboBoxWindDirection.setCurrentIndex(0)
        self.interface.comboBoxWindStrength.setCurrentIndex(0)
        self.interface.checkBoxSail.setCheckState(0)
        self.interface.checkBoxMilitaryActivity.setCheckState(0)

    def set_defaults_lineedit(self):
        self.interface.lineEditBreitenGrad.setText('43')

    def set_defaults_boxes(self):
        self.interface.comboBoxSight.setCurrentIndex(0)
        self.interface.comboBoxSea.setCurrentIndex(2)
        self.interface.checkBoxAcoustic.setCheckState(2)
        self.interface.checkBoxFastSwim.setCheckState(2)
        self.interface.checkBoxNotConstantSwim.setCheckState(2)

    def set_date_defaults(self):
        '''
        Sets the GUI-fields representing date and time to default
        '''
        self.interface.dateEdit.setDate(
            Qt.QDate(
                int(time.strftime("%Y")),
                int(time.strftime("%m")),
                int(time.strftime("%d"))
                )
            )
        self.interface.timeEdit.setTime(
            Qt.QTime(
                int(time.strftime("%H")),
                int(time.strftime("%M"))
                )
            )
        
        
                
class EditGuiHander(GuiHandler):
    def __init__(self, frame, language_dict):
        GuiHandler.__init__(self, frame, language_dict)
        self.gui_lists = {
            'combo_boxes': [],
            'line_editors': [],
            'checkboxes': []}
        self.gui_lists['line_editors'].append(
            self.interface.lineEditBreitenGrad)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditBreitenMinuten)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditLangenGrad)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditLangenMinuten)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditCourseWeek)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditGuide)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditCourse)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditShipName)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditTemperaturePlancton)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditSalinityPlancton)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditSightDepthPlancton)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditTemperatureSights)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditSightDepthSights)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditSalinitySights)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditCourseWhale)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditNumberMin)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditNumberMax)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditPositionWhale)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditParamDistance)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditDuration)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditDistanceToShip)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditBlowFrequency)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditOtherSpecies)
        self.gui_lists['line_editors'].append(
            self.interface.lineEditNumNewBorns)

        self.gui_lists['checkboxes'] = []
        self.gui_lists['checkboxes'].append(self.interface.checkBoxAcoustic)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxSail)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxMilitaryActivity)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxZooPlancton)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxPhytoPlancton)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxWaterSamplePlancton)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxLazy)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxSlowSwim)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxFastSwim)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxNotConstantSwim)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxConstantSwim)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxEating)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxDive)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxFlukeSight)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxSpyHop)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxFlukeHit)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxMating)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxPlaying)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxCurious)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxLoud)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxFotos)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxFotosMade)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxBlow)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxOtherSpecies)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxJump)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxBreachBack)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxBreachSide)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxYoungOnes)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxChildren)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxNewborn)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxCloseBoat)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxRideBack)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxRideDive)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxRideFront)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxRideSide)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxSocial)
        self.gui_lists['checkboxes'].append(self.interface.checkBoxCompact)
        self.gui_lists['checkboxes'].append(
            self.interface.checkBoxNotCompact)

        self.gui_lists['combo_boxes'].append(self.interface.comboBoxSea)
        self.gui_lists['combo_boxes'].append(self.interface.comboBoxClouds)
        self.gui_lists['combo_boxes'].append(self.interface.comboBoxSight)
        self.gui_lists['combo_boxes'].append(
            self.interface.comboBoxWindStrength)
        self.gui_lists['combo_boxes'].append(
            self.interface.comboBoxWindDirection)
        self.gui_lists['combo_boxes'].append(self.interface.comboBoxSpecies)


    def set_labels(self):
        GuiHandler.set_labels(self)
        self.interface.pushButtonDeleteEntry.setText(self.language_dict['delete'])
        self.interface.pushButtonNextEntry.setText(self.language_dict['next'])
        self.interface.pushButtonPredecentEntry.setText(self.language_dict['previous'])
        self.interface.pushButtonSendOffSightData.setText(self.language_dict['save_transect'])
        self.interface.labelSubTitle.setText(self.language_dict['transect_details_title'])
        self.interface.pushButtonSailData.setText(self.language_dict['save_transect'])
        self.interface.pushButtonSendOffSightEarly.setText(self.language_dict['save'])
        self.interface.labelTransectID.setText(self.language_dict['transect_id'])

    def set_defaults(self):
        '''
        Sets all GUI-widgets to default
        '''
        self.set_sight_lineedit_default()
        self.set_plancton_lineedit_default()
        self.set_main_frame_lineedits_default()
        self.interface.lineEditBreitenGrad.setText('43')
        self.set_defaults_boxes()
        self.set_main_frame_boxes_default()
        self.set_sight_details_lineedits_default()
        self.set_sight_details_checkboxes__enabled_default()        
        self.interface.checkBoxChildren.setEnabled(False)
        self.interface.labelFlukeHit.setEnabled(False)
        self.interface.checkBoxRideFront.setEnabled(False)
        self.interface.checkBoxRideSide.setEnabled(False)
        self.interface.lineEditOtherSpecies.setEnabled(False)
        self.interface.labelBlowFrequency.setEnabled(False)
        self.set_plancton_checkboxes_default()
        self.interface.comboBoxSpecies.setCurrentIndex(0)
        self.set_sight_details_checkboxes_default()
        self.interface.dateEdit.setDate(Qt.QDate(int(0), int(0), 0))
        self.interface.timeEdit.setTime(Qt.QTime(int(0), int(0)))
        
class MainModeGuiHandler(GuiHandler):
    def __init__(self, frame, language_dict):
        GuiHandler.__init__(self, frame, language_dict)

    def set_labels(self):
        GuiHandler.set_labels(self)
        self.interface.pushButtonSendOffSightData.setText(self.language_dict['save'])
        self.interface.pushButtonSendOffSailData.setText(self.language_dict['save_transect'])
        self.interface.pushButtonSendOffBeforeDetails.setText(self.language_dict['save'])
        self.interface.label.setText(self.language_dict['transect_id'])
        self.interface.pushButtonSetFormToDefault.setText(self.language_dict['reset_form'])

    def set_sight_details_default(self):
        '''
        Sets default in the details part of the sight part of the GUI
        '''
        GuiHandler.set_sight_details_checkboxes__enabled_default(self)
        self.interface.checkBoxNewborn.setEnabled(False)
        self.interface.lineEditBlowFrequency.setEnabled(False)
        self.interface.labelCompact.setEnabled(False)
        self.interface.labelNotCompact.setEnabled(False)
        GuiHandler.set_sight_details_checkboxes_default(self)
        self.interface.checkBoxFastSwim.setCheckState(2)
        self.interface.checkBoxNotConstantSwim.setCheckState(2)
        GuiHandler.set_sight_details_lineedits_default(self)

    def set_sight_default(self):
        '''
        Sets defaults in the sight part of the GUI
        '''
        GuiHandler.set_sight_combobox_default(self)
        GuiHandler.set_sight_lineedit_default(self)

    def set_plancton_default(self):
        '''
        Sets defaults in the plancton part of the GUI
        '''
        GuiHandler.set_plancton_checkboxes_default(self)
        GuiHandler.set_plancton_lineedit_default(self)

    def set_main_frame_post_entry(self):
        '''
        Sets defaults in the main-frame of the GUI after an entry was made
        '''
        GuiHandler.set_main_frame_post_entry_checkboxes(self)
        GuiHandler.set_main_frame_post_entry_lineedits(self)
        GuiHandler.set_date_defaults(self)

    def set_main_frame_defaults(self):
        '''
        Sets defaults in the main-frame of the GUI
        '''
        GuiHandler.set_main_frame_boxes_default(self)
        self.interface.comboBoxSea.setCurrentIndex(2)
        self.interface.checkBoxAcoustic.setCheckState(2)
        self.interface.comboBoxSight.setCurrentIndex(0)
        GuiHandler.set_main_frame_lineedits_default(self)
        self.interface.lineEditBreitenGrad.setText('43')

    def set_defaults(self):
        '''
        Sets defaults wished by for customer
        '''
        GuiHandler.set_defaults_boxes(self)
        GuiHandler.set_defaults_lineedit(self)
