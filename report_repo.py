import json
import re
import abc

from airflow.utils.db import provide_session
from airflow.models import Variable
from lumen_plugin.report import Report


class ReportRepo(abc.ABC):
    """
    ReportRepo is an abstract class that all classes must inherit from if
    they intend on returning lists of reports from a repository.
    """

    @classmethod
    @abc.abstractmethod
    def list(self):
        """ Returns all reports from the repo """
        pass

    @classmethod
    @abc.abstractmethod
    def get(self):
        """ Gets a particular report from the repo """
        pass


class VariablesReportRepo(ReportRepo):
    """
    VariablesReportRepo uses Airflow variables as a repository for
    report configurations.  It can read JSON from variables and
    output report objects.
    """

    # Only variables with this prefix will be parsed
    report_prefix = "lumen_report_"

    @classmethod
    @provide_session
    def list(cls, session=None):
        """ Return a list of all matching reports in variables """
        reports = []
        for (name, val) in cls.each_from_db(session):
            r = cls.to_report(name, val)
            reports.append(r)

        return reports

    @classmethod
    @provide_session
    def get(cls, name, session=None):
        """ Get a single report from variables """
        for (n, val) in cls.each_from_db(session):
            if n == name:
                return cls.to_report(n, val)

    @classmethod
    def each_from_db(cls, session):
        """ Iterator for Airflow variables """
        variables = session.query(Variable).all()
        for var in variables:
            n = cls.parse_variable_name(var.key)
            if n is None:
                continue

            v = cls.parse_variable_val(var.val)
            yield (n, v)

    @staticmethod
    def to_report(name, v):
        """ Generates report objects from variable data """
        r = Report(name)
        r.report_title = v["report_title"]
        r.report_title_url = v["report_title_url"]
        r.description = v["description"]
        r.owner_name = v["owner_name"]
        r.owner_email = v["owner_email"]
        r.subscribers = v["subscribers"]
        r.tests = v["tests"]
        r.schedule_type = v["schedule_type"]
        if ("daily" in r.schedule_type):
            r.schedule_time = v["schedule_time"]
        if ("weekly" in r.schedule_type):
            r.schedule_time = v["schedule_time"]
            r.schedule_week_day = v["schedule_week_day"]
        r.schedule = v["schedule"]
        return r

    @staticmethod
    def parse_variable_name(key):
        """
        Returns a parsed variable name.  Returns None if the
        variable is not a Lumen report variable
        """
        m = re.search(r"^%s(.*)$" % VariablesReportRepo.report_prefix, key, re.I)
        if m is None:
            return None

        name = m.group(1)
        return name

    @staticmethod
    def parse_variable_val(json_val):
        """ Returns JSON from a Lumen report variable """
        try:
            return json.loads(json_val)
        except json.decoder.JSONDecodeError:
            return None