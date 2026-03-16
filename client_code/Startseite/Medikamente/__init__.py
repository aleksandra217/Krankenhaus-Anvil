from ._anvil_designer import MedikamenteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class Medikamente(MedikamenteTemplate):
  def __init__(self,abteilungs_id=None, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.data_grid_1.clear()
    # Any code you write here will run before the form opens.

    #abteilungs_id = 1
    sql= f"""
            SELECT DISTINCT
            m.Name AS Medikament,
            h.Name AS Herstellername,
            h.Adresse AS Herstelleradresse,
            l.Ort AS Lagerort,
            l.Kapazitaet AS Lagerkapazitaet
          FROM Patient p
          JOIN Patient_Medikament p_m ON p.PatientenId =p_m.PatientenId
          JOIN Medikament m ON p_m.MedikamentenId = m.MedikamentenId
          LEFT JOIN Hersteller_Medikament h_m ON m.MedikamentenId = h_m.MedikamentenId
          LEFT JOIN Hersteller h ON h_m.HerstellerId = h.HerstellerId
          LEFT JOIN Lager_Medikament l_m ON m.MedikamentenId = l_m.MedikamentenId
          LEFT JOIN Lager l ON l_m.LagerId = l.LagerId
          WHERE p.AbteilungsId = {abteilungs_id}
          ORDER BY m.Name;
    """
  
    datenanzeigen = anvil.server.call('query_database_dict', sql)
    print("SQL:", datenanzeigen)
    #self.repeating_panel_1.items = datenanzeigen

    header = GridPanel()
    header.add_component(Label(text="Medikament", bold=True),col_xs=0, width_xs=2)
    header.add_component(Label(text="Name des Herstellers", bold=True),col_xs=2, width_xs=2)
    header.add_component(Label(text="Adresse des Herstellers", bold=True),col_xs=4, width_xs=2)
    header.add_component(Label(text="Lagerort", bold=True),col_xs=6, width_xs=2)
    header.add_component(Label(text="Lagerkapazität", bold=True),col_xs=8, width_xs=2)
    #header.add_component(Label(text="Informationen Medikament", bold=True), col_xs=11, width_xs=1)
    self.data_grid_1.add_component(header)
  
  
    for row in datenanzeigen:
      zeile = GridPanel()
      zeile.add_component(Label(text=row['Medikament']), col_xs=0, width_xs=2)
      zeile.add_component(Label(text=row['Herstellername']), col_xs=2, width_xs=2)
      zeile.add_component(Label(text=row['Herstelleradresse']), col_xs=4 ,width_xs=2)
      zeile.add_component(Label(text=row['Lagerort']), col_xs=6, width_xs=2)
      zeile.add_component(Label(text=row['Lagerkapazitaet']), col_xs=8, width_xs=2) 
      #zeile.add_component(Label(text=row.get('Informationen Medikament','')),col_xs=11, width_xs=1)
      self.data_grid_1.add_component(zeile)
    self.repeating_panel_1.items = datenanzeigen
      #self.data_grid_1.columns = [
      #{"id": "arzt", "title": "Arzt", "data_key" :"NamedesArztes", "width": "10%"},
    #{"id": "pflege", "title": "Pflegekraft", "data_key": "NamedesPflegekraftes", "width": "10%"},
    #{"id": "patient", "title": "Patient", "data_key" :"NamedesPatientes", "width": "10%"},
    #{"id": "behandlung", "title": "Behandlung", "data_key" :"Behanldungart", "width": "10%"},
    #{"id": "medikament", "title": "Medikament", "data_key" :"NamedesMedikamentes", "width": "10%"},
    #{"id": "dosierung", "title": "Dosierung", "data_key" :"DosierungdesMedikamentes", "width": "10%"},
    #]
  
  
  #self.data_grid_1
  
  
  
  
  # print(self.Drop_Down_Menu_Abteilungen.selected_value)
  
    # :abteilung_id. :-> ist der SChutz vor der SQL-Injection.
  
    #self.repeating_panel_1.items = anvil.server.call('query_database_dict', sql)

  @handle("zurueck", "click")
  def zurueck_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')

