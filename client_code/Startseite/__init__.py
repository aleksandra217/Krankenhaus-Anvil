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

  @handle("Drop_Down_Menu_Abteilungen", "change")
  def Drop_Down_Menu_Abteilungen_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.Drop_Down_Menu_Abteilungen.selected_value is not None:
      self.data_grid_1.visible = True;
    
