import sqlite3

# ===========================
# Verbindung und DB erstellen
# ===========================
conn = sqlite3.connect("krankenhaus_datenbank.db")
cursor = conn.cursor()

# ===========================
# Tabellen erstellen
# ===========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Abteilung (
    AbteilungsId INTEGER PRIMARY KEY,
    Name TEXT,
    Stockwerk TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Arzt (
    ArztId INTEGER PRIMARY KEY,
    Name TEXT,
    Fachgebiet TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Pflegekraft (
    Personalnummer INTEGER PRIMARY KEY,
    Name TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient (
    PatientenId INTEGER PRIMARY KEY,
    Name TEXT,
    Geschlecht TEXT,
    Geburtsdatum DATE,
    AbteilungsId INTEGER,
    FOREIGN KEY (AbteilungsId) REFERENCES Abteilung(AbteilungsId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Behandlung (
    BehandlungsId INTEGER PRIMARY KEY,
    Behandlungsart TEXT,
    Datum DATE,
    ArztId INTEGER,
    FOREIGN KEY (ArztId) REFERENCES Arzt(ArztId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Medikament (
    MedikamentenId INTEGER PRIMARY KEY,
    Name TEXT,
    Dosierung TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Lager (
    LagerId INTEGER PRIMARY KEY,
    Ort TEXT,
    Kapazitaet INTEGER
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Hersteller (
    HerstellerId INTEGER PRIMARY KEY,
    Name TEXT,
    Adresse TEXT
);
""")

# ===========================
# Zwischentabellen N:M
# ===========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient_Behandlung (
    PatientenId INTEGER,
    BehandlungsId INTEGER,
    PRIMARY KEY (PatientenId, BehandlungsId),
    FOREIGN KEY (PatientenId) REFERENCES Patient(PatientenId),
    FOREIGN KEY (BehandlungsId) REFERENCES Behandlung(BehandlungsId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient_Medikament (
    PatientenId INTEGER,
    MedikamentenId INTEGER,
    PRIMARY KEY (PatientenId, MedikamentenId),
    FOREIGN KEY (PatientenId) REFERENCES Patient(PatientenId),
    FOREIGN KEY (MedikamentenId) REFERENCES Medikament(MedikamentenId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Arzt_Medikament (
    ArztId INTEGER,
    MedikamentenId INTEGER,
    PRIMARY KEY (ArztId, MedikamentenId),
    FOREIGN KEY (ArztId) REFERENCES Arzt(ArztId),
    FOREIGN KEY (MedikamentenId) REFERENCES Medikament(MedikamentenId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Lager_Medikament (
    LagerId INTEGER,
    MedikamentenId INTEGER,
    PRIMARY KEY (LagerId, MedikamentenId),
    FOREIGN KEY (LagerId) REFERENCES Lager(LagerId),
    FOREIGN KEY (MedikamentenId) REFERENCES Medikament(MedikamentenId)
);
""")

# ✅ **HIER war der Fehler — jetzt korrekt**
cursor.execute("""
CREATE TABLE IF NOT EXISTS Hersteller_Medikament (
    HerstellerId INTEGER,
    MedikamentenId INTEGER,
    PRIMARY KEY (HerstellerId, MedikamentenId),
    FOREIGN KEY (HerstellerId) REFERENCES Hersteller(HerstellerId),
    FOREIGN KEY (MedikamentenId) REFERENCES Medikament(MedikamentenId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Abteilung_Arzt (
    AbteilungsId INTEGER,
    ArztId INTEGER,
    PRIMARY KEY (AbteilungsId, ArztId),
    FOREIGN KEY (AbteilungsId) REFERENCES Abteilung(AbteilungsId),
    FOREIGN KEY (ArztId) REFERENCES Arzt(ArztId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Abteilung_Pflegekraft (
    AbteilungsId INTEGER,
    Personalnummer INTEGER,
    PRIMARY KEY (AbteilungsId, Personalnummer),
    FOREIGN KEY (AbteilungsId) REFERENCES Abteilung(AbteilungsId),
    FOREIGN KEY (Personalnummer) REFERENCES Pflegekraft(Personalnummer)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient_Pflegekraft (
    PatientenId INTEGER,
    Personalnummer INTEGER,
    PRIMARY KEY (PatientenId, Personalnummer),
    FOREIGN KEY (PatientenId) REFERENCES Patient(PatientenId),
    FOREIGN KEY (Personalnummer) REFERENCES Pflegekraft(Personalnummer)
);
""")

# ===========================
# Daten einfügen
# ===========================

# Abteilungen
abteilungen = [
    (1, 'Neurologie', '2. Stock'),
    (2, 'Innere Medizin', '3. Stock'),
    (3, 'Kardiologie', '4. Stock'),
    (4, 'Allgemeinchirurgie', '1. Stock'),
    (5, 'Anästhesiologie', '1. Stock'),
    (6, 'HNO', '2. Stock')
]
cursor.executemany("INSERT OR IGNORE INTO Abteilung VALUES (?,?,?)", abteilungen)

# Ärzte
aerzte = [
    (1, 'Dr. Thomas Müller', 'Neurologie'),
    (2, 'Dr. Julia Fischer', 'Neurologie'),
    (3, 'Dr. Mia Schmidt', 'Innere Medizin'),
    (4, 'Dr. Paul Weber', 'Innere Medizin'),
    (5, 'Dr. Lisa Maier', 'Kardiologie'),
    (6, 'Dr. Jonas Richter', 'Kardiologie'),
    (7, 'Dr. Johanna Meier', 'Allgemeinchirurgie'),
    (8, 'Dr. Sophie Wagner', 'Anästhesiologie'),
    (9, 'Dr. Lukas Becker', 'HNO')
]
cursor.executemany("INSERT OR IGNORE INTO Arzt VALUES (?,?,?)", aerzte)

# Pflegekräfte
pflegekraefte = [
    (1, 'Anna Klein'),
    (2, 'Luca Markovic'),
    (3, 'Natalie Meyer'),
    (4, 'Marie Schmidt'),
    (5, 'Marc Hoffmann'),
    (6, 'Lea Krause'),
    (7, 'Ben Wolf'),
    (8, 'Clara Neumann'),
    (9, 'Tom Berger')
]
cursor.executemany("INSERT OR IGNORE INTO Pflegekraft VALUES (?,?)", pflegekraefte)

# Patienten
patienten = [
    (1, 'Lukas Maier', 'M', '1980-01-01', 1),
    (2, 'Laura Becker', 'W', '1990-05-12', 1),
    (3, 'Paul Koch', 'M', '2000-05-11', 2),
    (4, 'Anna Klein', 'W', '1985-07-21', 2),
    (5, 'Thomas Müller', 'M', '1980-06-19', 3),
    (6, 'Lara Maierhofer', 'W', '2012-03-12', 3),
    (7, 'Tim Bauer', 'M', '1992-09-05', 4),
    (8, 'Emma Schulz', 'W', '1975-11-11', 4),
    (9, 'Jonas Weber', 'M', '1988-08-08', 5),
    (10, 'Lea Hoffmann', 'W', '1995-12-30', 5),
    (11, 'Nina Fischer', 'W', '1999-01-15', 6)
]
cursor.executemany("INSERT OR IGNORE INTO Patient VALUES (?,?,?,?,?)", patienten)

# Behandlungen
behandlungen = [
    (1, 'Routinecheck', '2026-03-10', 1),
    (2, 'Blutdruckkontrolle', '2026-03-11', 2),
    (3, 'Herzuntersuchung', '2026-03-12', 5),
    (4, 'Operation', '2026-03-13', 7),
    (5, 'Anästhesie Vorbereitung', '2026-03-14', 8),
    (6, 'Neurodiagnostik', '2026-03-15', 1),
    (7, 'Kardiologische Kontrolle', '2026-03-16', 6),
    (8, 'HNO Untersuchung', '2026-03-17', 9),
    (9, 'Chirurgische Nachkontrolle', '2026-03-18', 7),
    (10, 'Medikamentenabgabe', '2026-03-19', 3),
    (11, 'Blutuntersuchung', '2026-03-20', 4)
]
cursor.executemany("INSERT OR IGNORE INTO Behandlung VALUES (?,?,?,?)", behandlungen)

# Patient_Behandlung
patient_behandlung = [(i, i) for i in range(1, 12)]
cursor.executemany("INSERT OR IGNORE INTO Patient_Behandlung VALUES (?,?)", patient_behandlung)

# Medikamente
medikamente = [
    (1, 'Antikoagulanzien', '1000mg'),
    (2, 'Aspirin', '100mg'),
    (3, 'Elektrolytlösungen', '500ml'),
    (4, 'Amoxicillin', '12ml'),
    (5, 'Propofol + Fentagnyl', '14ml + 1,4ml'),
    (6, 'Penicillin', '10ml'),
    (7, 'Ibuprofen', '200mg')
]
cursor.executemany("INSERT OR IGNORE INTO Medikament VALUES (?,?,?)", medikamente)

# Lager
lager = [
    (1, 'Lager A', 100),
    (2, 'Lager B', 250),
    (3, 'Lager C', 180),
    (4, 'Lager D', 120),
    (5, 'Lager E', 300),
    (6, 'Lager F', 90)
]
cursor.executemany("INSERT OR IGNORE INTO Lager VALUES (?,?,?)", lager)

# Hersteller
hersteller = [
    (1, 'Pharma AG', 'Hauptstraße 12'),
    (2, 'Medicare GmbH', 'Lindenweg 5'),
    (3, 'Gesundheit Inc.', 'Bahnhofstraße 7'),
    (4, 'BioPharm Ltd.', 'Gartenweg 3'),
    (5, 'Heilmittel AG', 'Rosenallee 9'),
    (6, 'VitalPharma', 'Birkenweg 15')
]
cursor.executemany("INSERT OR IGNORE INTO Hersteller VALUES (?,?,?)", hersteller)

# Zwischentabellen N:M (Medikamente zu Patienten, Ärzten, Lager, Hersteller)
patient_med = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 1), (9, 2), (10, 3), (11, 4)]
cursor.executemany("INSERT OR IGNORE INTO Patient_Medikament VALUES (?,?)", patient_med)

arzt_med = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 1), (9, 2)]
cursor.executemany("INSERT OR IGNORE INTO Arzt_Medikament VALUES (?,?)", arzt_med)

lager_med = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (1, 7)]
cursor.executemany("INSERT OR IGNORE INTO Lager_Medikament VALUES (?,?)", lager_med)

hersteller_med = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (6, 7)]
cursor.executemany("INSERT OR IGNORE INTO Hersteller_Medikament VALUES (?,?)", hersteller_med)

# Abteilung_Arzt
abteilung_arzt = [(1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (3, 6), (4, 7), (5, 8), (6, 9)]
cursor.executemany("INSERT OR IGNORE INTO Abteilung_Arzt VALUES (?,?)", abteilung_arzt)

# Abteilung_Pflegekraft
abteilung_pflegekraft = [(1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (6, 9)]
cursor.executemany("INSERT OR IGNORE INTO Abteilung_Pflegekraft VALUES (?,?)", abteilung_pflegekraft)

# Patient_Pflegekraft
patient_pflegekraft = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 7), (9, 8), (10, 9), (11, 9)]
cursor.executemany("INSERT OR IGNORE INTO Patient_Pflegekraft VALUES (?,?)", patient_pflegekraft)

# ===========================
# Änderungen speichern und DB schließen
# ===========================
conn.commit()
conn.close()

print("Datenbank 'krankenhaus_db.db' erfolgreich erstellt und vollständig befüllt!")

import sqlite3

# ===========================
# Verbindung und DB erstellen
# ===========================
conn = sqlite3.connect("krankenhaus.db")
cursor = conn.cursor()

# ===========================
# Tabellen erstellen
# ===========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Abteilung (
    AbteilungsId INTEGER PRIMARY KEY,
    Name TEXT,
    Stockwerk TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Arzt (
    ArztId INTEGER PRIMARY KEY,
    Name TEXT,
    Fachgebiet TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Pflegekraft (
    Personalnummer INTEGER PRIMARY KEY,
    Name TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient (
    PatientenId INTEGER PRIMARY KEY,
    Name TEXT,
    Geschlecht TEXT,
    Geburtsdatum DATE,
    AbteilungsId INTEGER,
    FOREIGN KEY (AbteilungsId) REFERENCES Abteilung(AbteilungsId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Behandlung (
    BehandlungsId INTEGER PRIMARY KEY,
    Behandlungsart TEXT,
    Datum DATE,
    ArztId INTEGER,
    FOREIGN KEY (ArztId) REFERENCES Arzt(ArztId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Medikament (
    MedikamentenId INTEGER PRIMARY KEY,
    Name TEXT,
    Dosierung TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Lager (
    LagerId INTEGER PRIMARY KEY,
    Ort TEXT,
    Kapazitaet INTEGER
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Hersteller (
    HerstellerId INTEGER PRIMARY KEY,
    Name TEXT,
    Adresse TEXT
);
""")

# ===========================
# Zwischentabellen N:M
# ===========================
cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient_Behandlung (
    PatientenId INTEGER,
    BehandlungsId INTEGER,
    PRIMARY KEY (PatientenId, BehandlungsId),
    FOREIGN KEY (PatientenId) REFERENCES Patient(PatientenId),
    FOREIGN KEY (BehandlungsId) REFERENCES Behandlung(BehandlungsId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient_Medikament (
    PatientenId INTEGER,
    MedikamentenId INTEGER,
    PRIMARY KEY (PatientenId, MedikamentenId),
    FOREIGN KEY (PatientenId) REFERENCES Patient(PatientenId),
    FOREIGN KEY (MedikamentenId) REFERENCES Medikament(MedikamentenId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Arzt_Medikament (
    ArztId INTEGER,
    MedikamentenId INTEGER,
    PRIMARY KEY (ArztId, MedikamentenId),
    FOREIGN KEY (ArztId) REFERENCES Arzt(ArztId),
    FOREIGN KEY (MedikamentenId) REFERENCES Medikament(MedikamentenId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Lager_Medikament (
    LagerId INTEGER,
    MedikamentenId INTEGER,
    PRIMARY KEY (LagerId, MedikamentenId),
    FOREIGN KEY (LagerId) REFERENCES Lager(LagerId),
    FOREIGN KEY (MedikamentenId) REFERENCES Medikament(MedikamentenId)
);
""")

# ✅ **HIER war der Fehler — jetzt korrekt**
cursor.execute("""
CREATE TABLE IF NOT EXISTS Hersteller_Medikament (
    HerstellerId INTEGER,
    MedikamentenId INTEGER,
    PRIMARY KEY (HerstellerId, MedikamentenId),
    FOREIGN KEY (HerstellerId) REFERENCES Hersteller(HerstellerId),
    FOREIGN KEY (MedikamentenId) REFERENCES Medikament(MedikamentenId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Abteilung_Arzt (
    AbteilungsId INTEGER,
    ArztId INTEGER,
    PRIMARY KEY (AbteilungsId, ArztId),
    FOREIGN KEY (AbteilungsId) REFERENCES Abteilung(AbteilungsId),
    FOREIGN KEY (ArztId) REFERENCES Arzt(ArztId)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Abteilung_Pflegekraft (
    AbteilungsId INTEGER,
    Personalnummer INTEGER,
    PRIMARY KEY (AbteilungsId, Personalnummer),
    FOREIGN KEY (AbteilungsId) REFERENCES Abteilung(AbteilungsId),
    FOREIGN KEY (Personalnummer) REFERENCES Pflegekraft(Personalnummer)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Patient_Pflegekraft (
    PatientenId INTEGER,
    Personalnummer INTEGER,
    PRIMARY KEY (PatientenId, Personalnummer),
    FOREIGN KEY (PatientenId) REFERENCES Patient(PatientenId),
    FOREIGN KEY (Personalnummer) REFERENCES Pflegekraft(Personalnummer)
);
""")

# ===========================
# Daten einfügen
# ===========================

# Abteilungen
abteilungen = [
    (1, 'Neurologie', '2. Stock'),
    (2, 'Innere Medizin', '3. Stock'),
    (3, 'Kardiologie', '4. Stock'),
    (4, 'Allgemeinchirurgie', '1. Stock'),
    (5, 'Anästhesiologie', '1. Stock'),
    (6, 'HNO', '2. Stock')
]
cursor.executemany("INSERT OR IGNORE INTO Abteilung VALUES (?,?,?)", abteilungen)

# Ärzte
aerzte = [
    (1, 'Dr. Thomas Müller', 'Neurologie'),
    (2, 'Dr. Julia Fischer', 'Neurologie'),
    (3, 'Dr. Mia Schmidt', 'Innere Medizin'),
    (4, 'Dr. Paul Weber', 'Innere Medizin'),
    (5, 'Dr. Lisa Maier', 'Kardiologie'),
    (6, 'Dr. Jonas Richter', 'Kardiologie'),
    (7, 'Dr. Johanna Meier', 'Allgemeinchirurgie'),
    (8, 'Dr. Sophie Wagner', 'Anästhesiologie'),
    (9, 'Dr. Lukas Becker', 'HNO')
]
cursor.executemany("INSERT OR IGNORE INTO Arzt VALUES (?,?,?)", aerzte)

# Pflegekräfte
pflegekraefte = [
    (1, 'Anna Klein'),
    (2, 'Luca Markovic'),
    (3, 'Natalie Meyer'),
    (4, 'Marie Schmidt'),
    (5, 'Marc Hoffmann'),
    (6, 'Lea Krause'),
    (7, 'Ben Wolf'),
    (8, 'Clara Neumann'),
    (9, 'Tom Berger')
]
cursor.executemany("INSERT OR IGNORE INTO Pflegekraft VALUES (?,?)", pflegekraefte)

# Patienten
patienten = [
    (1, 'Lukas Maier', 'M', '1980-01-01', 1),
    (2, 'Laura Becker', 'W', '1990-05-12', 1),
    (3, 'Paul Koch', 'M', '2000-05-11', 2),
    (4, 'Anna Klein', 'W', '1985-07-21', 2),
    (5, 'Thomas Müller', 'M', '1980-06-19', 3),
    (6, 'Lara Maierhofer', 'W', '2012-03-12', 3),
    (7, 'Tim Bauer', 'M', '1992-09-05', 4),
    (8, 'Emma Schulz', 'W', '1975-11-11', 4),
    (9, 'Jonas Weber', 'M', '1988-08-08', 5),
    (10, 'Lea Hoffmann', 'W', '1995-12-30', 5),
    (11, 'Nina Fischer', 'W', '1999-01-15', 6)
]
cursor.executemany("INSERT OR IGNORE INTO Patient VALUES (?,?,?,?,?)", patienten)

# Behandlungen
behandlungen = [
    (1, 'Routinecheck', '2026-03-10', 1),
    (2, 'Blutdruckkontrolle', '2026-03-11', 2),
    (3, 'Herzuntersuchung', '2026-03-12', 5),
    (4, 'Operation', '2026-03-13', 7),
    (5, 'Anästhesie Vorbereitung', '2026-03-14', 8),
    (6, 'Neurodiagnostik', '2026-03-15', 1),
    (7, 'Kardiologische Kontrolle', '2026-03-16', 6),
    (8, 'HNO Untersuchung', '2026-03-17', 9),
    (9, 'Chirurgische Nachkontrolle', '2026-03-18', 7),
    (10, 'Medikamentenabgabe', '2026-03-19', 3),
    (11, 'Blutuntersuchung', '2026-03-20', 4)
]
cursor.executemany("INSERT OR IGNORE INTO Behandlung VALUES (?,?,?,?)", behandlungen)

# Patient_Behandlung
patient_behandlung = [(i, i) for i in range(1, 12)]
cursor.executemany("INSERT OR IGNORE INTO Patient_Behandlung VALUES (?,?)", patient_behandlung)

# Medikamente
medikamente = [
    (1, 'Antikoagulanzien', '1000mg'),
    (2, 'Aspirin', '100mg'),
    (3, 'Elektrolytlösungen', '500ml'),
    (4, 'Amoxicillin', '12ml'),
    (5, 'Propofol + Fentagnyl', '14ml + 1,4ml'),
    (6, 'Penicillin', '10ml'),
    (7, 'Ibuprofen', '200mg')
]
cursor.executemany("INSERT OR IGNORE INTO Medikament VALUES (?,?,?)", medikamente)

# Lager
lager = [
    (1, 'Lager A', 100),
    (2, 'Lager B', 250),
    (3, 'Lager C', 180),
    (4, 'Lager D', 120),
    (5, 'Lager E', 300),
    (6, 'Lager F', 90)
]
cursor.executemany("INSERT OR IGNORE INTO Lager VALUES (?,?,?)", lager)

# Hersteller
hersteller = [
    (1, 'Pharma AG', 'Straße 1'),
    (2, 'Medicare GmbH', 'Straße 2'),
    (3, 'Gesundheit Inc.', 'Straße 3'),
    (4, 'BioPharm Ltd.', 'Straße 4'),
    (5, 'Heilmittel AG', 'Straße 5'),
    (6, 'VitalPharma', 'Straße 6')
]
cursor.executemany("INSERT OR IGNORE INTO Hersteller VALUES (?,?,?)", hersteller)

# Zwischentabellen N:M (Medikamente zu Patienten, Ärzten, Lager, Hersteller)
patient_med = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 1), (9, 2), (10, 3), (11, 4)]
cursor.executemany("INSERT OR IGNORE INTO Patient_Medikament VALUES (?,?)", patient_med)

arzt_med = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 1), (9, 2)]
cursor.executemany("INSERT OR IGNORE INTO Arzt_Medikament VALUES (?,?)", arzt_med)

lager_med = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (1, 7)]
cursor.executemany("INSERT OR IGNORE INTO Lager_Medikament VALUES (?,?)", lager_med)

hersteller_med = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (6, 7)]
cursor.executemany("INSERT OR IGNORE INTO Hersteller_Medikament VALUES (?,?)", hersteller_med)

# Abteilung_Arzt
abteilung_arzt = [(1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (3, 6), (4, 7), (5, 8), (6, 9)]
cursor.executemany("INSERT OR IGNORE INTO Abteilung_Arzt VALUES (?,?)", abteilung_arzt)

# Abteilung_Pflegekraft
abteilung_pflegekraft = [(1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (6, 9)]
cursor.executemany("INSERT OR IGNORE INTO Abteilung_Pflegekraft VALUES (?,?)", abteilung_pflegekraft)

# Patient_Pflegekraft
patient_pflegekraft = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 7), (9, 8), (10, 9), (11, 9)]
cursor.executemany("INSERT OR IGNORE INTO Patient_Pflegekraft VALUES (?,?)", patient_pflegekraft)

# ===========================
# Änderungen speichern und DB schließen
# ===========================
conn.commit()
conn.close()

print("Datenbank 'krankenhaus_db.db' erfolgreich erstellt und vollständig befüllt!")

