import inflection

from airflow.models.dag import Dag


class Report:
    """
    Report holds a Lumen report configuration.  It is used to build
    Lumen report DAGs
    """

    def __init__(self, name):
        self.name = name
        self.__emails = None
        self.__tests = None
        self.__schedule = None

    @property
    def emails(self):
        """ Emails that the report will go to """
        return self.__emails

    @emails.setter
    def emails(self, val):
        self.__emails == val

    @property
    def schedule(self):
        """ The schedule when the report will run """
        return self.__schedule

    @schedule.setter
    def schedule(self, val):
        self.__schedule = val

    @property
    def dag_id(self):
        """ Returns a DAG ID based on the name of this report """
        return inflection.underscore(inflection.parameterize("lumen %s" % self.name))

    @property
    def tests(self):
        """ The tests run in the report """
        return self.__tests

    @tests.setter
    def tests(self, val):
        self.__tests = val

    def get_last_dagrun(self, session, include_externally_triggered=True):
        """
        Gets the last DagRun for this report.

        NOTE: The include_externally_triggered is set to True, which is
        the opposite of the Dag object method of the same name.
        """
        return Dag.get_last_dagrun(self.dag_id, session, include_externally_triggered)
