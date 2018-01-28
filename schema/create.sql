CREATE EXTENSION postgis;

CREATE TABLE IF NOT EXISTS dt_art(
art_id character(3) PRIMARY KEY UNIQUE,
art character(50),
vulgaer character(50)
);

CREATE TABLE IF NOT EXISTS dt_bewoelkung(
bewoelkung_id integer NOT NULL PRIMARY KEY,
bewoelkungsgrad numeric(4,1)
);

CREATE TABLE IF NOT EXISTS dt_meer(
meer_id	character(3)
NOT NULL PRIMARY KEY,
meer_id_num	numeric(4,1),
zustand_meer	character(50)
);

CREATE TABLE IF NOT EXISTS dt_sicht(
sicht_id integer
NOT NULL PRIMARY KEY,
beschreibung	character(50)
);

CREATE TABLE IF NOT EXISTS dt_transekt(
transekt_id character(3) NOT NULL PRIMARY KEY,
transektvorgang character(50)
);

CREATE TABLE IF NOT EXISTS dt_wind(
wind_id	character(3)
NOT NULL PRIMARY KEY,
wind_id_num	numeric(4,1),
windbezeichnung	character(50),
windgeschwindigkeit	character(5)
);

CREATE TABLE IF NOT EXISTS dt_windrichtung(
windrichtung_id	character(3)
NOT NULL PRIMARY KEY,
windrichtung	character(50)
);

CREATE TABLE IF NOT EXISTS geometry_columns(
f_table_catalog	character varying(256)
NOT NULL,
f_table_schema	character varying(256)
NOT NULL,
f_table_name	character varying(256)
NOT NULL,
f_geometry_column	character varying(256)
NOT NULL,
coord_dimension	integer
NOT NULL,
srid	integer
NOT NULL,
type	character varying(30)
NOT NULL
, PRIMARY KEY(f_table_catalog, f_table_schema, f_table_name, f_geometry_column)
);

CREATE TABLE IF NOT EXISTS gt_bathymetrie(
feature_id	integer
NOT NULL PRIMARY KEY,
bathymetrie_id	integer	,
tiefe	character(20)	,
geom	geometry
);

CREATE TABLE IF NOT EXISTS gt_grid(
feature_id	integer
NOT NULL PRIMARY KEY,
grid_id	integer	,
geom	geometry
);

CREATE TABLE IF NOT EXISTS gt_grid_label(
feature_id	integer
NOT NULL PRIMARY KEY,
grid_id	integer	,
geom	geometry
);

CREATE TABLE IF NOT EXISTS gt_kuestendistanz(
feature_id	integer
NOT NULL PRIMARY KEY,
kuestendistanz_id	integer,
distanz	character(20),
geom	geometry
);

CREATE TABLE IF NOT EXISTS mt_fahrten(
fahrt_id	integer
NOT NULL PRIMARY KEY,
datum_b	date	,
datum_e	date	,
zeit_b	time without time zone,
zeit_e	time without time zone,
kurswoche	integer	,
guide	character(2),
schiff	character(50),
akustik	boolean	,
geom	geometry
);

CREATE TABLE IF NOT EXISTS mt_punkte(
punkt_id	integer
NOT NULL PRIMARY KEY,
datum	date,
zeit	time without time zone,
fahrt_id	integer,
FOREIGN KEY(fahrt_id) REFERENCES mt_fahrten(fahrt_id),
kurswoche	integer,
guide	character(2),
schiff	character(50),
transekt_id	character(3),
FOREIGN KEY (transekt_id) REFERENCES dt_transekt(transekt_id),
temperatur	numeric(3,1),
salinitaet	numeric(3,1),
messzeit	time without time zone,
breite	numeric(8,6),
laenge	numeric(9,6),
kurs	numeric(4,1),
meer_id	character(3),
FOREIGN KEY (meer_id) REFERENCES dt_meer(meer_id),
wind_id	character(3),
FOREIGN KEY (wind_id) REFERENCES dt_wind(wind_id),
windrichtung_id	character(3),
FOREIGN KEY (windrichtung_id) REFERENCES dt_windrichtung(windrichtung_id),
bewoelkung_id	integer,
FOREIGN KEY (bewoelkung_id) REFERENCES dt_bewoelkung(bewoelkung_id),
sicht_id	integer,
FOREIGN KEY (sicht_id) REFERENCES dt_sicht(sicht_id),
sichttiefe	numeric(3,1),
fotos	boolean,
akustik	boolean,
aufnahme	boolean,
zooplanktonprobe	boolean,
phytoplanktonprobe	boolean,
wasserprobe	boolean,
militaer	boolean,
segel	boolean,
art_id	character(3),
FOREIGN KEY (art_id) REFERENCES dt_art(art_id),
anzahl_min	numeric(4,1),
anzahl_max	numeric(4,1),
kurs_wal	numeric(4,1),
position_wal	numeric(4,1),
sichtungswinkel	numeric(4,1),
distanz_p	numeric(3,1),
distanz_m	numeric(6,1),
breite_wal	numeric(8,6),
laenge_wal	numeric(9,6),
dauer	numeric(5,2),
ruhend	boolean,
langsam	boolean,
schnell	boolean,
richtung_konstant	boolean,
richtung_wechselnd	boolean,
nahrungsaufnahme	boolean,
flukenschlagen	boolean,
spruenge	boolean,
breach_seitlich	boolean,
breach_rueckwaerts	boolean,
soziales_verhalten	boolean,
paarung	boolean,
spiel	boolean,
gruppe_kompakt	boolean,
gruppe_locker	boolean,
jungtiere	boolean,
anzahl_jungtiere	character(20),
kaelber	boolean,
neugeborene	boolean,
annaeherung	boolean,
schwimmen_nah	boolean,
bugwellen	boolean,
heckwellen	boolean,
seitlich	boolean,
unter_schiff	boolean,
tauchgang	boolean,
fluke_sichtbar	boolean,
lautgebung	boolean,
in_begleitung	boolean,
begleitende_spezies	character(20),
blas	boolean,
blasfrequenz	character(20),
spy_hopping	boolean,
anderes_verhalten	character(200),
zusaetzliche_beobachtungen	character(200),
geom	geometry
);

CREATE TABLE IF NOT EXISTS spatial_ref_sys(
srid	integer
NOT NULL PRIMARY KEY,
auth_name	character varying(256),
auth_srid	integer	,
srtext	character varying(2048),
proj4text	character varying(2048)
);

CREATE TABLE IF NOT EXISTS tt_andere(
fid	integer
NOT NULL PRIMARY KEY,
punkt_id	integer	,
datum	date	,
zeit	time without time zone	,
fahrt_id	integer	,
kurswoche	integer	,
guide	character(2),
schiff	character(50),
transekt_id	character(3)	,
transektvorgang	character(50),
temperatur	numeric(3,1)	,
salinitaet	numeric(3,1)	,
messzeit	time without time zone	,
breite	numeric(8,6)	,
laenge	numeric(9,6)	,
kurs	numeric(4,1)	,
meer_id	character(3)	,
meer_id_num	numeric(4,1),
zustand_meer	character(50)	,
wind_id	character(3)	,
wind_id_num	numeric(4,1),
windbezeichnung	character(50)	,
windgeschwindigkeit	character(5),
windrichtung_id	character(3)	,
windrichtung	character(50)	,
bewoelkung_id	integer	,
bewoelkungsgrad	numeric(4,1),
sicht_id	integer	,
sicht_beschreibung	character(50),
sichttiefe	numeric(3,1)	,
fotos	boolean	,
akustik	boolean	,
aufnahme	boolean	,
zooplanktonprobe	boolean	,
phytoplanktonprobe	boolean	,
wasserprobe	boolean	,
militaer	boolean	,
segel	boolean	,
zusaetzliche_beobachtungen	character(200),
kuestendistanz_id	integer	,
kuestendistanz	character(20),
bathymetrie_id	integer	,
meerestiefe	character(20),
grid_id	integer	,
geom	geometry
);

CREATE TABLE IF NOT EXISTS tt_beobachtungen(
fid	integer
NOT NULL PRIMARY KEY,
punkt_id	integer	,
datum	date	,
zeit	time without time zone	,
fahrt_id	integer	,
kurswoche	integer	,
guide	character(2),
schiff	character(50),
transekt_id	character(3),
transektvorgang	character(50),
temperatur	numeric(3,1)	,
salinitaet	numeric(3,1)	,
messzeit	time without time zone	,
breite	numeric(8,6)	,
laenge	numeric(9,6)	,
kurs	numeric(4,1)	,
meer_id	character(3)	,
meer_id_num	numeric(4,1),
zustand_meer	character(50),
wind_id	character(3)	,
wind_id_num	numeric(4,1),
windbezeichnung	character(50),
windgeschwindigkeit	character(5)	,
windrichtung_id	character(3)	,
windrichtung	character(50)	,
bewoelkung_id	integer	,
bewoelkungsgrad	numeric(4,1),
sicht_id	integer	,
sicht_beschreibung	character(50),
sichttiefe	numeric(3,1)	,
fotos	boolean	,
akustik	boolean	,
aufnahme	boolean	,
zooplanktonprobe	boolean	,
phytoplanktonprobe	boolean	,
wasserprobe	boolean	,
militaer	boolean	,
segel	boolean	,
art_id	character(3),
art	character(50)	,
vulgaer	character(50),
anzahl_min	numeric(4,1)	,
anzahl_max	numeric(4,1)	,
kurs_wal	numeric(4,1)	,
position_wal	numeric(4,1),
sichtungswinkel	numeric(4,1),
distanz_p	numeric(3,1)	,
distanz_m	numeric(6,1)	,
breite_wal	numeric(8,6)	,
laenge_wal	numeric(9,6)	,
dauer	numeric(5,2)	,
ruhend	boolean	,
langsam	boolean	,
schnell	boolean	,
richtung_konstant	boolean	,
richtung_wechselnd	boolean	,
nahrungsaufnahme	boolean	,
flukenschlagen	boolean	,
spruenge	boolean	,
breach_seitlich	boolean	,
breach_rueckwaerts	boolean	,
soziales_verhalten	boolean	,
paarung	boolean	,
spiel	boolean	,
gruppe_kompakt	boolean	,
gruppe_locker	boolean	,
jungtiere	boolean,
anzahl_jungtiere	character(20),
kaelber	boolean,
neugeborene	boolean,
annaeherung	boolean,
schwimmen_nah	boolean,
bugwellen	boolean,
heckwellen	boolean,
seitlich	boolean,
unter_schiff	boolean,
tauchgang	boolean,
fluke_sichtbar	boolean,
lautgebung	boolean,
in_begleitung	boolean,
begleitende_spezies	character(20),
blas	boolean,
blasfrequenz	character(20),
spy_hopping	boolean,
anderes_verhalten	character(200),
zusaetzliche_beobachtungen	character(200),
kuestendistanz_id	integer,
kuestendistanz	character(20),
bathymetrie_id	integer,
meerestiefe	character(20),
grid_id	integer,
geom geometry
);