from flask_admin.model import BaseModelView

class ReportModel(BaseModelView):
  #The BaseModelView class's __init__ takes in a model which is then defined as self.model
  
  # Implementing the required BaseModelView functions
  def get_pk_value(self, model):
    return None

  def scaffold_list_columns(self):
    return None

  def scaffold_sortable_columns(self):
    return None

  def init_search(self):
    return False

  def scaffold_form(self):
    class MyForm(Form):
      pass
    # Do something
    return MyForm

  def get_list(self, page, sort_field, sort_desc, search, filters, page_size=None):
    return []
  
  def get_one(self, id):
    return None
  
  def create_model(self, form):
    return None
  
  def update_model(self, form, model):
    return None
  
  def delete_model(self, model)
    return True
  
  def is_valid_filter(self, filter):
    return None
  
  def scaffold_filters(self, name):
    return None

