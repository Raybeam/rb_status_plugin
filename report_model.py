from flask_admin.model import BaseModelView
from flask_admin import expose

from wtforms.validators import DataRequired, Email
from wtforms_components import TimeField
from wtforms.form import Form
from wtforms import (
    StringField,
    TextAreaField,
    SelectMultipleField,
    SelectField,
    HiddenField,
)

from lumen_plugin.helpers.list_tasks_helper import get_all_test_choices
from lumen_plugin.report_repo import VariablesReportRepo
from lumen_plugin.report_form_saver import ReportFormSaver

import logging


# from flask_admin.form import BaseForm
# from wtforms import widgets

# class BS3TextFieldWidget(widgets.TextInput):
#     def __call__(self, field, **kwargs):
#         kwargs["class"] = u"form-control"
#         if field.label:
#             kwargs["placeholder"] = field.label.text
#         if "name_" in kwargs:
#             field.name = kwargs["name_"]
#         return super(BS3TextFieldWidget, self).__call__(field, **kwargs)


# class BS3TextAreaFieldWidget(widgets.TextArea):
#     def __call__(self, field, **kwargs):
#         kwargs["class"] = u"form-control"
#         kwargs["rows"] = 3
#         if field.label:
#             kwargs["placeholder"] = field.label.text
#         return super(BS3TextAreaFieldWidget, self).__call__(field, **kwargs)


# class Select2Widget(widgets.Select):
#     extra_classes = None

#     def __init__(self, extra_classes=None, style=None):
#         self.extra_classes = extra_classes
#         self.style = style or u"width:250px"
#         return super(Select2Widget, self).__init__()

#     def __call__(self, field, **kwargs):
#         kwargs["class"] = u"my_select2 form-control"
#         if self.extra_classes:
#             kwargs["class"] = kwargs["class"] + " " + self.extra_classes
#         kwargs["style"] = self.style
#         if "name_" in kwargs:
#             field.name = kwargs["name_"]
#         return super(Select2Widget, self).__call__(field, **kwargs)


# class Select2ManyWidget(widgets.Select):
#     extra_classes = None

#     def __init__(self, extra_classes=None, style=None):
#         self.extra_classes = extra_classes
#         self.style = style or u"width:250px"
#         return super(Select2ManyWidget, self).__init__()

#     def __call__(self, field, **kwargs):
#         kwargs["class"] = u"my_select2 form-control"
#         if self.extra_classes:
#             kwargs["class"] = kwargs["class"] + " " + self.extra_classes
#         kwargs["style"] = self.style
#         kwargs["multiple"] = u"true"
#         if "name_" in kwargs:
#             field.name = kwargs["name_"]
#         return super(Select2ManyWidget, self).__call__(field, **kwargs)


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
        Returns the unique report_id from the report object
        """
        return model.report_id

    def scaffold_list_columns(self):
        return [
            "report_id",
            "report_title",
            "report_title_url",
            "description",
            "owner_name",
            "owner_email",
            "subscribers",
            "tests",
            "schedule_type",
            "schedule_time",
            "schedule_week_day",
            "schedule"
        ]

    def scaffold_sortable_columns(self):
        return None

    def init_search(self):
        return False

    def scaffold_form(self):
        class ReportForm(Form):
            report_id = HiddenField()
            title = StringField(
                ("Title"),
                description="Title will be used as the report's name",
                # widget=BS3TextFieldWidget(),
                validators=[DataRequired()],
            )
            description = TextAreaField(
                ("Description"),
                # widget=BS3TextAreaFieldWidget(),
                validators=[DataRequired()]
            )
            owner_name = StringField(
                ("Owner Name"),
                # widget=BS3TextFieldWidget(),
                validators=[DataRequired()]
            )
            owner_email = StringField(
                ("Owner Email"),
                description="Owner email will be added to the subscribers list",
                # widget=BS3TextFieldWidget(),
                validators=[DataRequired(), Email()],
            )
            subscribers = StringField(
                ("Subscribers"),
                description=(
                    "List of comma separeted emails that should receive email\
                     notifications. Automatically adds owner email to this list."
                ),
                # widget=BS3TextFieldWidget(),
            )
            tests = SelectMultipleField(
                ("Tests"),
                description=(
                    "List of the tests to include in the report. Only includes\
                 tasks that have ran in airflow."
                ),
                choices=get_all_test_choices(),
                # widget=Select2ManyWidget(),
                validators=[DataRequired()],
            )
            schedule_type = SelectField(
                ("Schedule"),
                description=("Select how you want to schedule the report"),
                choices=[
                    ("manual", "None (Manual triggering)"),
                    ("daily", "Daily"),
                    ("weekly", "Weekly"),
                    ("custom", "Custom (Cron)"),
                ],
                # widget=widgets.Select(),
                validators=[DataRequired()],
            )
            schedule_time = TimeField(
                "Time",
                render_kw={"class": "form-control"},
                validators=[DataRequired()]
            )
            schedule_week_day = SelectField(
                ("Day of week"),
                description=("Select day of a week you want to schedule the report"),
                choices=[
                    ("0", "Sunday"),
                    ("1", "Monday"),
                    ("2", "Tuesday"),
                    ("3", "Wednesday"),
                    ("4", "Thursday"),
                    ("5", "Friday"),
                    ("6", "Saturday"),
                ],
                # widget=Select2Widget(),
                validators=[DataRequired()],
            )
            schedule_custom = StringField(
                ("Cron schedule"),
                description='Enter cron schedule (e.g. "0 0 * * *")',
                # widget=BS3TextFieldWidget(),
                validators=[DataRequired()],
            )

        # Do something
        return ReportForm

    def get_list(self, page, sort_field, sort_desc, search, filters, page_size=None):
        return None, VariablesReportRepo.list()

    def get_one(self, id):
        report = VariablesReportRepo.get_report(id)
        if not report:
            return None

        return report

    def create_model(self, form):
        form = self.scaffold_form()
        logging.error("Creating model")
        logging.info(form)
        # report_saver = ReportFormSaver(form)
        # form_submitted = report_saver.extract_report_data_into_airflow(
        #     report_exists=False
        # )
        # if form_submitted:
        #     return self

    def update_model(self, form, model):
        return None

    def delete_model(self, model):
        return True

    def is_valid_filter(self, filter):
        return None

    def scaffold_filters(self, name):
        return None
