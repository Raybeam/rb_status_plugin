
class Report:
    def __init__(self, name):
        self.name = name
        self.__emails = None
        self.__tasks = None
        self.__schedule = None

    @property 
    def emails(self):
        return self.__emails

    @emails.setter
    def emails(self, val):
        self.__emails == val

    @property
    def schedule(self):
        return self.__schedule

    @schedule.setter
    def schedule(self, val):
        self.__schedule = val

    @property
    def tasks(self):
        return self.__tasks
    
    @tasks.setter
    def tasks(self, val):
        self.__tasks = val