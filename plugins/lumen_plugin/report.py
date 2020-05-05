import inflection


class Report:
    """
    Report holds a Lumen report configuration.  It is used to build
    Lumen report DAGs
    """

    def __init__(self, name):
        self.name = name
        self.__owner_email = None
        self.__subscribers = None
        self.__tests = None
        self.__schedule = None

    @property
    def owner_email(self):
        """ Email address of the report owner """
        return self.__owner_email

    @owner_email.setter
    def owner_email(self, val):
        self.__owner_email = val

    @property
    def subscribers(self):
        """ Emails that the report will go to """
        return self.__subscribers

    @subscribers.setter
    def subscribers(self, val):
        self.__subscribers = val

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
