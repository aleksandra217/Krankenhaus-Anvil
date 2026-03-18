from ._anvil_designer import Dashboard_1Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Dashboard_1(Dashboard_1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.zurueck.background = "black"

    # Any code you write here will run before the form opens.
    daten_holen = anvil.server.call('patienten_pro_abteilung_anzeigen')
    farben_balken = ["A3C4F3",  "C6DFB9",  "F7C5CC",  "F9E79F",  "F0D9E0",  "C2E9FB", "FAD7A0"]
    x_labels = [row['Abteilungsname'] for row in daten_holen]
    y_values = [row['Anzahl'] for row in daten_holen]
    self.plot_patienten.data = [{
      'x': x_labels,
      'y': y_values,
      'type': 'bar',
      "marker": {
        'color':farben_balken
      }
    }]

    self.plot_patienten.layout = {
      'title': 'Anzahl Patienten pro Abteilung',
      'xaxis': {'title': 'Abteilung'},
      'yaxis': {'title': 'Anzahl Patienten'}
    }

  @handle("zurueck", "click")
  def zurueck_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')
