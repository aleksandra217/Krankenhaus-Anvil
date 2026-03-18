from ._anvil_designer import Dashboard_2Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Dashboard_2(Dashboard_2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.zurueck.background = "black"
    daten_holen = anvil.server.call('medikamentenbestand')

    x_labels = [row['medikament'] for row in daten_holen]
    y_values = [row['aktueller_bestand'] for row in daten_holen]

    farben_balken = ["FFD1DC",  "B5EAD7",  "FFDAC1",  "E2F0CB",  "C7CEEA",  "FBE7C6",  "D5A6BD"]
    self.plot_1.data = [{
      "x": x_labels,
      "y": y_values,
      "type": "bar",
      "marker": {
        'color':farben_balken
      }
    }]

    
    self.plot_1.layout = {
      'title': 'Lagerbestand der Medikamente (Stück)',
      'xaxis': {'title': 'Medikament'},
      'yaxis': {'title': 'Befüllung in Stück'},
      
    }

  @handle("zurueck", "click")
  def zurueck_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Startseite')

