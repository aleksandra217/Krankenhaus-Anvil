import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def query_database(query: str):
  with sqlite3.connect(data_files["krankenhaus_datenbank.db"]) as conn:
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return result

@anvil.server.callable
def query_database_dict(query: str, params=None):
  with sqlite3.connect(data_files["krankenhaus_datenbank.db"]) as conn:
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
  return [dict(row) for row in result]

@anvil.server.callable
def patienten_pro_abteilung_anzeigen():
  sql = """
        SELECT 
        Abteilung.Name AS Abteilungsname, COUNT(Patient.PatientenId) AS Anzahl
        FROM Abteilung 
        LEFT JOIN Patient ON Patient.AbteilungsId = Abteilung.AbteilungsId
        GROUP BY Abteilung.AbteilungsId, Abteilung.Name
        ORDER BY Abteilung.AbteilungsId
  """

  return query_database_dict(sql)

@anvil.server.callable
def medikamentenbestand():
    sql ="""
      SELECT
      m.Name AS medikament,
      l.Ort AS Lagerort,
      l.Kapazitaet AS max_kapazitaet,
      COUNT(l_m.MedikamentenId) AS aktueller_bestand
  FROM Medikament m
  LEFT JOIN Lager_Medikament l_m ON m.MedikamentenId = l_m.MedikamentenId
  LEFT JOIN Lager l ON l.LagerId = l_m.LagerId
  GROUP BY m.MedikamentenId, l.LagerId
  ORDER BY m.MedikamentenId;
    """
    

    return query_database_dict(sql)
 



