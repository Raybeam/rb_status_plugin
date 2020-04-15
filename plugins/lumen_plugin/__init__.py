import json

from airflow.models import Variable
from airflow.plugins_manager import AirflowPlugin

class LumenPlugin(AirflowPlugin):
    name = 'lumen'
    operators = []
    flask_blueprints = []
    hooks = []
    executors = []
    macros = []
    admin_views = []
    menu_links = []
    appbuilder_views = []
    appbuilder_menu_items = []


def each_lumen_config(session):
    configs = {}
    with session:
        qry = session.query(Variable).all()

        data = json.JSONDecoder()
        for var in qry:
            try:
                val = data.decode(var.val)
            except Exception:  # pylint: disable=broad-except
                val = var.val

            if var.key.startswith('lumen_report_'):
                configs[var.key] = val
    
    return configs