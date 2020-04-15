from airflow.plugins_manager import AirflowPlugin


class LumenPlugin(AirflowPlugin):
    name = "lumen"
    operators = []
    flask_blueprints = []
    hooks = []
    executors = []
    macros = []
    admin_views = []
    menu_links = []
    appbuilder_views = []
    appbuilder_menu_items = []
