from flask_admin.model import BaseModelView

class ReportModel(BaseModelView):
  #The BaseModelView class's __init__ takes in a model which is then defined as self.model
  
  # Implementing the required BaseModelView functions
  def get_pk_value(self):
    return None

  def scaffold_list_columns(self):
    return None

  def scaffold_sortable_columns(self):
    return None

  def init_search(self):
    return None

  def scaffold_form(self):
    class MyForm(Form):
      pass
    # Do something
    return MyForm

  def get_list(self):
    return None
  
  def get_one(self):
    return None
  
  def create_model(self):
    return None
  
  def update_model(self):
    return None
  
  def delete_model(self)
    return None
  
  def is_valid_filter(self):
    return None
  
  def scaffold_filters(self):
    return None

