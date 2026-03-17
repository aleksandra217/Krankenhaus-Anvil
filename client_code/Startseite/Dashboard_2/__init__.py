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

    daten_holen = anvil.server.call('medikamentenbestand')

    x_labels = [row['medikament'] for row in daten_holen]
    y_values = [row['prozent'] for row in daten_holen]

    self.plot_1.data = [{
      "x": x_labels,
      "y": y_values,
      "type": "bar"
    }]

    self.plot_1.layout = {
      'title': 'Lagerbestand der Medikamente (%)',
      'xaxis': {'title': 'Medikament'},
      'yaxis': {'title': 'Befüllung in %'},
      'y_axis_range': [0,100]
    }