from flask_admin.model import BaseModelView, Form


class ReportModel(BaseModelView):
    """
    The BaseModelView class's __init__ takes in a model
    which is then defined as self.model
    """

    # Implementing the required BaseModelView functions
    def __init__(
        self,
        model,
        session,
        name=None,
        category=None,
        endpoint=None,
        url=None,
        static_folder=None,
        menu_class_name=None,
        menu_icon_type=None,
        menu_icon_value=None
    ):
        self.session = session
        super().__init__(
            model,
            name,
            category,
            endpoint,
            url,
            static_folder,
            menu_class_name=menu_class_name,
            menu_icon_type=menu_icon_type,
            menu_icon_value=menu_icon_value
        )

    def get_pk_value(self, model):
        """
            Return the primary key value from a model object.
            If there are multiple primary keys, they're
            encoded into string representation.
        """
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

    def delete_model(self, model):
        return True

    def is_valid_filter(self, filter):
        return None

    def scaffold_filters(self, name):
        return None
