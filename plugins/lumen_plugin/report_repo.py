import json
import re
import abc

from airflow.models import Variable
from plugins.lumen_plugin.report import Report

class ReportRepo(abc.ABC):
    @abc.abstractmethod
    def list(self):
        pass

    @abc.abstractmethod
    def get(self):
        pass

class VariablesReportRepo(ReportRepo):
    report_prefix = 'lumen_report_'

    def __init__(self, session):
        self._session = session

    def list(self):
        reports = []
        for (name, val) in self.each_from_db():
            r = self.to_report(name, val)
            reports.append(r)

        return reports

    def get(self, name):
        for (n, val) in self.each_from_db():
            if n == name:
                return self.to_report(n, val) 

    def each_from_db(self):
        variables = self._session.query(Variable).all()
        for var in variables:
            n = self.parse_variable_name(var.key)
            if n is None:
                continue

            v = self.parse_variable_val(var.val)
            yield (n, v)

    def to_report(self, name, v):
        r = Report(name)
        r.emails = v['emails']
        r.tests = v['tests']
        r.schedule = v['schedule']

        return r

    @staticmethod
    def parse_variable_name(key):
        m = re.search(r'^%s(.*)$' % VariablesReportRepo.report_prefix, key, re.I)
        if m is None:
            return None

        name = m.group(1)
        return name        

    @staticmethod
    def parse_variable_val(json_val):
        try:
            return json.loads(json_val)
        except json.decoder.JSONDecodeError:
            return None


