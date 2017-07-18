#imports
from meeting_minutes.modules.club.Settings import Settings
import warnings
#Club

#Instance Data
#location-the default meeting place of the club
#startTime-the default start time of meetings
#endTime-the default end time of meetings
#author-The author of the meeting minutes, be it the vice president, the president, or the secretary
#weekday-The default meeting day of the week for the club
#members-list of all club members

def _isList(candidate):
    return (type(candidate) is list or type(candidate) is tuple)

class Club:

    LOCATION_KEY_VALUE = 'location'
    START_TIME_KEY_VALUE = 'startTime'
    END_TIME_KEY_VALUE = 'endTime'
    AUTHOR_KEY_VALUE = 'author'
    WEEKDAY_KEY_VALUE = 'weekday'
    MEMBERS_KEY_VALUE = 'members'

    #Methods
    def __init__(self):
        self.settings = Settings()

    def setLocation(self, location):
        self.settings.write(self.LOCATION_KEY_VALUE, location)

    def setStartTime(self, startTime):
        self.settings.write(self.START_TIME_KEY_VALUE, startTime)

    def setEndTime(self, endTime):
        self.settings.write(self.END_TIME_KEY_VALUE, endTime)

    def setAuthor(self, author):
        self.settings.write(self.AUTHOR_KEY_VALUE, author)

    def setWeekday(self, weekday):
        self.settings.write(self.WEEKDAY_KEY_VALUE, weekday)

    def setMembers(self, members):
        if(_isList(members)):
            members = ', '.join(members)
        self.settings.write(self.MEMBERS_KEY_VALUE, members)

    def setSetting(self, setting, value):
        if(setting == self.LOCATION_KEY_VALUE):
            self.setLocation(value)
        elif(setting == self.START_TIME_KEY_VALUE):
            self.setStartTime(value)
        elif(setting == self.END_TIME_KEY_VALUE):
            self.setEndTime(value)
        elif(setting == self.AUTHOR_KEY_VALUE):
            self.setAuthor(value)
        elif(setting == self.WEEKDAY_KEY_VALUE):
            self.setWeekday(value)
        elif(setting == self.MEMBERS_KEY_VALUE):
            self.setMembers(value)
        else:
            warnings.warn('Setting requested not a recognized setting!', UserWarning)

    def addToSettings(self, setting, addendum):
        self.settings.addTo(setting, addendum)

    def settingDefined(self, settingToCheck):
        if(self.settings is None or self.settings.read(settingToCheck) is None):
            return False
        else:
            return True

    def getLocation(self):
        return self.settings.read(Club.LOCATION_KEY_VALUE)

    def getStartTime(self):
        return self.settings.read(Club.START_TIME_KEY_VALUE)

    def getEndTime(self):
        return self.settings.read(Club.END_TIME_KEY_VALUE)

    def getAuthor(self):
        return self.settings.read(Club.AUTHOR_KEY_VALUE)

    def getWeekday(self):
        return self.settings.read(Club.WEEKDAY_KEY_VALUE)

    def getMembers(self):
        return self.settings.read(Club.MEMBERS_KEY_VALUE)
