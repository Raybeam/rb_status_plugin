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
    def list(cls):
        """ Return a list of all matching reports in variables """
        reports = []
        for (name, val) in cls.each_from_db():
            r = cls.to_report(name, val)
            reports.append(r)

        return reports

    @classmethod
    def get(cls, name):
        """ Get a single report from variables """
        for (n, val) in cls.each_from_db():
            if n == name:
                return cls.to_report(n, val)

    @classmethod
    @provide_session
    def each_from_db(cls, session=None):
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
        r.emails = v["emails"]
        r.tests = v["tests"]
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
