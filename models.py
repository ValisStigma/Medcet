'''
Created on 16.09.2014

@author: rafael
'''
'''
Created on Jun 10, 2014

@author: rafael
'''
from sqlalchemy import Column, Integer, Boolean, String, Date, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class MtPunkte(Base):
    '''
    This class represents the mt_punkte-table
    '''
    __tablename__ = 'mt_punkte'
    punkt_id = Column(Integer, primary_key=True)
    datum = Column(Date)
    zeit = Column(DateTime)
    fahrt_id = Column(Integer)
    kurswoche = Column(Integer)
    guide = Column(String(2))
    schiff = Column(String(50))
    transekt_id = Column(String(3))
    temperatur = Column(Numeric(3, 1))
    salinitaet = Column(Numeric(3, 1))
    messzeit = Column(DateTime)
    breite = Column(Numeric(8, 6))
    laenge = Column(Numeric(9, 6))
    kurs = Column(Numeric(4, 1))
    meer_id = Column(String(3))
    wind_id = Column(String(3))
    windrichtung_id = Column(String(3))
    bewoelkung_id = Column(Integer)
    sicht_id = Column(Integer)
    sichttiefe = Column(Numeric(3, 1))
    fotos = Column(Boolean)
    akustik = Column(Boolean)
    aufnahme = Column(Boolean)
    zooplanktonprobe = Column(Boolean)
    phytoplanktonprobe = Column(Boolean)
    wasserprobe = Column(Boolean)
    militaer = Column(Boolean)
    segel = Column(Boolean)
    art_id = Column(String(3))
    anzahl_min = Column(Numeric(4,1))
    anzahl_max = Column(Numeric(4,1))
    kurs_wal = Column(Numeric(4,1))
    position_wal = Column(Numeric(4,1))
    sichtungswinkel = Column(Numeric(4,1))
    distanz_p = Column(Numeric(3,1))
    distanz_m = Column(Numeric(6,1))
    breite_wal = Column(Numeric(8,6))
    laenge_wal = Column(Numeric(9,6))
    dauer = Column(Numeric(5,2))
    ruhend = Column(Boolean)
    langsam = Column(Boolean)
    schnell = Column(Boolean)
    richtung_konstant = Column(Boolean)
    richtung_wechselnd = Column(Boolean)
    nahrungsaufnahme = Column(Boolean)
    flukenschlagen = Column(Boolean)
    spruenge = Column(Boolean)
    breach_seitlich = Column(Boolean)
    breach_rueckwaerts = Column(Boolean)
    soziales_verhalten = Column(Boolean)
    paarung = Column(Boolean)
    spiel = Column(Boolean)
    gruppe_kompakt = Column(Boolean)
    gruppe_locker = Column(Boolean)
    jungtiere = Column(Boolean)
    anzahl_jungtiere = Column(String(20))
    kaelber = Column(Boolean)
    neugeborene = Column(Boolean)
    annaeherung = Column(Boolean)
    schwimmen_nah = Column(Boolean)
    bugwellen = Column(Boolean)
    heckwellen = Column(Boolean)
    seitlich = Column(Boolean)
    unter_schiff = Column(Boolean)
    tauchgang = Column(Boolean)
    fluke_sichtbar = Column(Boolean)
    lautgebung = Column(Boolean)
    in_begleitung = Column(Boolean)
    begleitende_spezies = Column(String(20))
    blas = Column(Boolean)
    blasfrequenz = Column(String(20))
    spy_hopping = Column(Boolean)
    anderes_verhalten = Column(String(200))
    zusaetzliche_beobachtungen = Column(String(200))
    geom = Column(Geometry('Point'))

    def __repr__(self):
        '''
        Representation of a Point
        '''
        return "<Transect:  {:d}>".format(self.punkt_id)

class MtFahrten(Base):
    '''
    This class represents the mt_fahrten-table
    '''
    __tablename__ = 'mt_fahrten'
    fahrt_id = Column(Integer, primary_key=True)
    datum_b = Column(Date)
    datum_e = Column(Date)
    zeit_b = Column(DateTime)
    zeit_e = Column(DateTime)
    kurswoche = Column(Integer)
    guide = Column(String(2))
    schiff = Column(String(50))
    akustik = Column(Boolean)
    geom = Column(Geometry('LineString'))
    
    def __repr__(self):
        '''
        Representation of a Linestring
        '''
        return "<Linestring:  {:d}>".format(self.fahrt_id)
    
class TtAndere(Base):
    '''
    This class represents the tt_andere-table
    '''
    __tablename__ = 'tt_andere'
    fid = Column(Integer, primary_key=True)
    punkt_id = Column(Integer)
    datum = Column(Date)
    zeit = Column(DateTime)
    fahrt_id = Column(Integer)
    kurswoche = Column(Integer)
    guide = Column(String(2))
    schiff = Column(String(50))
    transekt_id = Column(String(3))
    transektvorgang = Column(String(50))
    temperatur = Column(Numeric(3, 1))
    salinitaet = Column(Numeric(3, 1))
    messzeit = Column(DateTime)
    breite = Column(Numeric(8, 6))
    laenge = Column(Numeric(9, 6))
    kurs = Column(Numeric(4, 1))
    meer_id = Column(String(3))
    meer_id_num = Column(Numeric(4, 1))
    zustand_meer = Column(String(50))
    wind_id = Column(String(3))
    wind_id_num = Column(Numeric(4, 1))
    windbezeichnung = Column(String(50))
    windgeschwindigkeit = Column(String(5))
    windrichtung_id = Column(String(3))
    windrichtung = Column(String(50))
    bewoelkung_id = Column(Integer)
    bewoelkungsgrad = Column(Numeric(4, 1))
    sicht_id = Column(Integer)
    sicht_beschreibung = Column(String(50))
    sichttiefe = Column(Numeric(3, 1))
    fotos = Column(Boolean)
    akustik = Column(Boolean)
    aufnahme = Column(Boolean)
    zooplanktonprobe = Column(Boolean)
    phytoplanktonprobe = Column(Boolean)
    wasserprobe = Column(Boolean)
    militaer = Column(Boolean)
    segel = Column(Boolean)
    zusaetzliche_beobachtungen = Column(String(200))
    kuestendistanz_id = Column(Integer)
    kuestendistanz = Column(String(20))
    bathymetrie_id = Column(Integer)
    meerestiefe = Column(String(20))
    grid_id = Column(Integer)
    geom = Column(Geometry('Point'))
    
    def __repr__(self):
        '''
        Representation of a tt_others
        '''
        return "<tt_andere:  {:d}>".format(self.fid)

class TtBeobachtungen(Base):
    '''
    This class represents the tt_beobachtungen-table
    '''
    __tablename__ = 'tt_beobachtungen'
    fid = Column(Integer, primary_key=True)
    punkt_id = Column(Integer)
    datum = Column(Date)
    zeit = Column(DateTime)
    fahrt_id = Column(Integer)
    kurswoche = Column(Integer)
    guide = Column(String(2))
    schiff = Column(String(50))
    transekt_id = Column(String(3))
    transektvorgang = Column(String(50))
    temperatur = Column(Numeric(3, 1))
    salinitaet = Column(Numeric(3, 1))
    messzeit = Column(DateTime)
    breite = Column(Numeric(8, 6))
    laenge = Column(Numeric(9, 6))
    kurs = Column(Numeric(4, 1))
    meer_id = Column(String(3))
    meer_id_num = Column(Numeric(4, 1))
    zustand_meer = Column(String(50))
    wind_id = Column(String(3))
    wind_id_num = Column(Numeric(4, 1))
    windbezeichnung = Column(String(50))
    windgeschwindigkeit = Column(String(5))
    windrichtung_id = Column(String(3))
    windrichtung = Column(String(50))
    bewoelkung_id = Column(Integer)
    bewoelkungsgrad = Column(Numeric(4, 1))
    sicht_id = Column(Integer)
    sicht_beschreibung = Column(String(50))
    sichttiefe = Column(Numeric(3, 1))
    fotos = Column(Boolean)
    akustik = Column(Boolean)
    aufnahme = Column(Boolean)
    zooplanktonprobe = Column(Boolean)
    phytoplanktonprobe = Column(Boolean)
    wasserprobe = Column(Boolean)
    militaer = Column(Boolean)
    segel = Column(Boolean)
    art_id = Column(String(3))
    art = Column(String(50))
    vulgaer = Column(String(50))
    anzahl_min = Column(Numeric(4,1))
    anzahl_max = Column(Numeric(4,1))
    kurs_wal = Column(Numeric(4,1))
    position_wal = Column(Numeric(4,1))
    sichtungswinkel = Column(Numeric(4,1))
    distanz_p = Column(Numeric(3,1))
    distanz_m = Column(Numeric(6,1))
    breite_wal = Column(Numeric(8,6))
    laenge_wal = Column(Numeric(9,6))
    dauer = Column(Numeric(5,2))
    ruhend = Column(Boolean)
    langsam = Column(Boolean)
    schnell = Column(Boolean)
    richtung_konstant = Column(Boolean)
    richtung_wechselnd = Column(Boolean)
    nahrungsaufnahme = Column(Boolean)
    flukenschlagen = Column(Boolean)
    spruenge = Column(Boolean)
    breach_seitlich = Column(Boolean)
    breach_rueckwaerts = Column(Boolean)
    soziales_verhalten = Column(Boolean)
    paarung = Column(Boolean)
    spiel = Column(Boolean)
    gruppe_kompakt = Column(Boolean)
    gruppe_locker = Column(Boolean)
    jungtiere = Column(Boolean)
    anzahl_jungtiere = Column(String(20))
    kaelber = Column(Boolean)
    neugeborene = Column(Boolean)
    annaeherung = Column(Boolean)
    schwimmen_nah = Column(Boolean)
    bugwellen = Column(Boolean)
    heckwellen = Column(Boolean)
    seitlich = Column(Boolean)
    unter_schiff = Column(Boolean)
    tauchgang = Column(Boolean)
    fluke_sichtbar = Column(Boolean)
    lautgebung = Column(Boolean)
    in_begleitung = Column(Boolean)
    begleitende_spezies = Column(String(20))
    blas = Column(Boolean)
    blasfrequenz = Column(String(20))
    spy_hopping = Column(Boolean)
    anderes_verhalten = Column(String(200))
    zusaetzliche_beobachtungen = Column(String(200))
    kuestendistanz_id = Column(Integer)
    kuestendistanz = Column(String(20))
    bathymetrie_id = Column(Integer)
    meerestiefe = Column(String(20))
    grid_id = Column(Integer)
    geom = Column(Geometry('Point'))
    
    def __repr__(self):
        '''
        Representation of a tt_beobachtungen
        '''
        return "<tt_beobachtungen:  {:d}>".format(self.fid)    
