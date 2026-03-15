from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Startseite(StartseiteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    abteilungen = anvil.server.call('query_database', "SELECT AbteilungsId, Name FROM Abteilung")
    self.Drop_Down_Menu_Abteilungen.items = [
      (row[1], row[0]) for row in abteilungen]

    #if self.Drop_Down_Menu_Abteilungen.items:
      #self.Drop_Down_Menu_Abteilungen.selected_value = self.Drop_Down_Menu_Abteilungen.items[0][1]



      
    self.Drop_Down_Menu_Abteilungen_change()

    
    
  @handle("Drop_Down_Menu_Abteilungen", "change")
  def Drop_Down_Menu_Abteilungen_change(self, **event_args):
    """This method is called when an item is selected"""
    abteilung_id = self.Drop_Down_Menu_Abteilungen.selected_value
    #print("ID:", abteilung_id)
    if abteilung_id is None:
      self.data_grid_1.clear()
      self.repeating_panel_1.items = []
      self.InformationenMedikament.visible = False
      return
    
      
    #datenanzeigen = anvil.server.call('query_database_dict', sql)
    #self.repeating_panel_1.items = datenanzeigen

  

      
    self.data_grid_1.clear()
    self.data_grid_1.visible = True
    self.InformationenMedikament.visible = True

    abteilung_id = self.Drop_Down_Menu_Abteilungen.selected_value
    


    sql= f"""
            SELECT DISTINCT
           ab.AbteilungsId,
            ab.Name AS Abteilungsname,
            ab.Stockwerk AS Stockwerk,
            ar.ArztId,
            ar.Name AS NamedesArztes,
            ar.Fachgebiet AS FachgebietdesArztes,
            pf.Personalnummer AS PersonalnummerPflegekraft,
            pf.Name AS NamedesPflegekraftes,
            p.PatientenId,
            p.Name AS NamedesPatienten,
            p.Geschlecht AS GeschlechtdesPatienten,
            p.Geburtsdatum AS GeburtsdatumdesPatienten,
            b.BehandlungsId,
            b.Behandlungsart AS Behandlungsart,
            b.Datum AS DatumderBehandlung,
            m.MedikamentenId,
            m.Name AS NamedesMedikamentes,
            m.Dosierung AS DosierungdesMedikamentes,
            l.LagerId,
            l.Ort AS OrtdesLagers,
            l.Kapazität AS Kapazität,
            h.HerstellerId,
            h.Name AS NamedesHerstellers,
            h.Adresse AS AdressedesHerstellers
        FROM Abteilung ab
        LEFT JOIN Abteilung_Arzt a_a ON ab.AbteilungsId = a_a.AbteilungsId
        LEFT JOIN Arzt ar ON a_a.ArztId = ar.ArztId
        LEFT JOIN Abteilung_Pflegekraft a_pf ON ab.AbteilungsId = a_pf.AbteilungsId
        LEFT JOIN Pflegekraft pf ON a_pf.Personalnummer = pf.Personalnummer
        LEFT JOIN Patient p ON p.AbteilungsId = ab.AbteilungsId
        LEFT JOIN Patient_Behandlung p_b ON p_b.PatientenId = p.PatientenId
        LEFT JOIN Behandlung b ON b.BehandlungsId = p_b.BehandlungsId
        LEFT JOIN Patient_Medikament p_m ON p_m.PatientenId = p.PatientenId
        LEFT JOIN Medikament m ON m.MedikamentenId = p_m.MedikamentenId
        LEFT JOIN Lager_Medikament l_m ON l_m.MedikamentenId = m.MedikamentenId
        LEFT JOIN Lager l on l.LagerId = l_m.LagerId
        LEFT JOIN Hersteller_Medikament h_m ON h_m.MedikamentenId = m.MedikamentenId
        LEFT JOIN Hersteller h ON h.HerstellerId = h_m.HerstellerId
        WHERE ab.AbteilungsId = {abteilung_id}
        AND b.Behandlungsart IS NOT NULL;
    """

    datenanzeigen = anvil.server.call('query_database_dict', sql)
    print("SQL:", datenanzeigen)
    self.repeating_panel_1.items = datenanzeigen
   
    header = GridPanel()
    header.add_component(Label(text="Arzt", bold=True),col_xs=0, width_xs=2)
    header.add_component(Label(text="Pflegekraft", bold=True),col_xs=2, width_xs=2)
    header.add_component(Label(text="Patient", bold=True),col_xs=4, width_xs=2)
    header.add_component(Label(text="Behandlung", bold=True),col_xs=6, width_xs=2)
    header.add_component(Label(text="Medikament", bold=True),col_xs=8, width_xs=2)
    header.add_component(Label(text="Dosierung", bold=True), col_xs=10, width_xs=2)
    #header.add_component(Label(text="Informationen Medikament", bold=True), col_xs=11, width_xs=1)
    self.data_grid_1.add_component(header)


    for row in datenanzeigen:
      zeile = GridPanel()
      zeile.add_component(Label(text=row['NamedesArztes']), col_xs=0, width_xs=2)
      zeile.add_component(Label(text=row['NamedesPflegekraftes']), col_xs=2, width_xs=2)
      zeile.add_component(Label(text=row['NamedesPatienten']), col_xs=4 ,width_xs=2)
      zeile.add_component(Label(text=row['Behandlungsart']), col_xs=6, width_xs=2)
      zeile.add_component(Label(text=row['NamedesMedikamentes']), col_xs=8, width_xs=2) 
      zeile.add_component(Label(text=row['DosierungdesMedikamentes']),col_xs=10, width_xs=2)
      #zeile.add_component(Label(text=row.get('Informationen Medikament','')),col_xs=11, width_xs=1)
      self.data_grid_1.add_component(zeile)
      #self.data_grid_1.columns = [
        #{"id": "arzt", "title": "Arzt", "data_key" :"NamedesArztes", "width": "10%"},
        #{"id": "pflege", "title": "Pflegekraft", "data_key": "NamedesPflegekraftes", "width": "10%"},
        #{"id": "patient", "title": "Patient", "data_key" :"NamedesPatientes", "width": "10%"},
        #{"id": "behandlung", "title": "Behandlung", "data_key" :"Behanldungart", "width": "10%"},
        #{"id": "medikament", "title": "Medikament", "data_key" :"NamedesMedikamentes", "width": "10%"},
        #{"id": "dosierung", "title": "Dosierung", "data_key" :"DosierungdesMedikamentes", "width": "10%"},
      #]
    

    #self.data_grid_1
     
    self.repeating_panel_1.items = datenanzeigen

    
  # print(self.Drop_Down_Menu_Abteilungen.selected_value)

    # :abteilung_id. :-> ist der SChutz vor der SQL-Injection.
    
    #self.repeating_panel_1.items = anvil.server.call('query_database_dict', sql)

  @handle("InformationenMedikament", "click")
  def InformationenMedikament_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite.Medikamente', row_dict=self.item, abteilungs_id=self.Drop_Down_Menu_Abteilungen.selected_value)
  
  @handle("zurueck", "click")
  def zurueck_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')
