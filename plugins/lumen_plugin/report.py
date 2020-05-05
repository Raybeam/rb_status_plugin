import inflection


class Report:
    """
    Report holds a Lumen report configuration.  It is used to build
    Lumen report DAGs
    """

    def __init__(self, name):
        self.name = name
        self.__report_title = None
        self.__description = None
        self.__owner_name = None
        self.__owner_email = None
        self.__subscribers = None
        self.__tests = None
        self.__schedule_type = None
        self.__schedule_time = None
        self.__schedule_week_day = None
        self.__schedule = None

    @property
    def report_title(self):
        """ Title of the report """
        return self.__report_title

    @report_title.setter
    def report_title(self, val):
        self.__report_title = val

    @property
    def description(self):
        """ Description of the report """
        return self.__description

    @description.setter
    def description(self, val):
        self.__description = val

    @property
    def owner_name(self):
        """ Name of the report owner """
        return self.__owner_name

    @owner_name.setter
    def owner_name(self, val):
        self.__owner_name = val

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
    def schedule_type(self):
        """ Type of schedule (daily, weekly, custom) """
        return self.__schedule_type

    @schedule_type.setter
    def schedule_type(self, val):
        self.__schedule_type = val

    @property
    def schedule_time(self):
        """ Hour:Min of the schedule (for daily and weekly) """
        return self.__schedule_time

    @schedule_time.setter
    def schedule_time(self, val):
        self.__schedule_time = val

    @property
    def schedule_week_day(self):
        """ Day of week (0-6) for weekly schedule """
        return self.__schedule_week_day

    @schedule_week_day.setter
    def schedule_week_day(self, val):
        self.__schedule_week_day = val

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
