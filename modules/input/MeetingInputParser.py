#imports
import sys
import string

#add user defined submodules to python path
sys.path.append('..')

import argparse
import warnings
import datetime
import calendar
from meeting_minutes.modules.club.Club import Club
from meeting_minutes.modules.input.week import getLastDate
from .. import ui
from . import InputError

#CONSTANT DATA INITIALIZATION
NO_FINANCES_MESSAGE = 'No Financial Transactions to Report'
AUTHOR_UNKNOWN_MESSAGE = 'Author Unknown'
SETTINGS_PREFIX = 'club_'
LIST_DELIMITER = ','

def _isList(candidate):
    return (type(candidate) is list or type(candidate) is tuple)

def _stringValid(string, isEmptyValid):
    # Check that the string is actually a string
    if(not _isList(string)):
        if(isinstance(string, str)):
            # If the string is empty
            if(_stringEmpty(string)):
                return isEmptyValid
            else:
                return True
        else:
            return False
    else:
        for i in range(0, len(string)):
            if(not _stringValid(string[i])):
                return False
        return True

def _stringEmpty(string):
    return not (string and string.strip())

def _dateValid(date, warn_enable):
    # Check that the format given is MM/DD/YY   ``
    try:
        # assert that date string was passed in MM/DD/YY format
        datetime.datetime.strptime(date, '%m/%d/%y')
        return True
    # initiate error handling if date is invalid
    except ValueError:
        # Dates should be formatted like: Month/Date/Year, with two digits for each.
        if(warn_enable):
            warnings.warn('Invalid Date Format. Dates should be formatted like: MM/DD/YY : ', UserWarning)
        return False
    except TypeError:
        if(warn_enable):
            warnings.warn('Invalid Date datatype: ', UserWarning)
        return False

def _timeValid(time, warn_enable):
    # Check that the time given is military time HH:MM
    try:
        # Check that the Start Time is valid
        # Times of day must be entered in military time to be valid
        # assert that the time string was passed in HH:MM format
        datetime.datetime.strptime(time, '%H:%M')
        return True
    # If invalid value, initiate error handling
    except ValueError:
        # Times should be formatted like: HH:MM, two digits for each
        if(warn_enable):
            warnings.warn('Your format is incorrect. Times should be formatted like HH:MM : ', UserWarning)
        return False
    except TypeError:
        if(warn_enable):
            warnings.warn('You did not enter a valid type, or you entered nothing at all where a time was expected : ', UserWarning)
        return False

def _removeArrayWhitespace(array):
    for i in range(0, len(array)):
        array[i] = array[i].strip()

class MeetingInputParser:

    #Instance Data:
    #date: a string date formatted mm/dd/yy
    #
    #startTime: a string meeting start time in format HH:MM
    #
    #endTime: a string meeting end time in format HH:MM
    #
    #finances: a string or string array describing financial transactions the club has made between now
    #             and the past meeting
    #
    #location: a string describing the location of the meeting
    #
    #proceedings: a string describing the meeting's events.  This is the meat of the report
    #
    #uploaderName: the name of the uploader
    #
    #parser: internal built in argument parser
    #
    #students: list of students that attended the meeting

    #METHODS

    def __init__(self):
        # initialize internal argument parser
        self.parser = argparse.ArgumentParser(description = 'Generate Meeting Minutes')
        # add potential arguments to the argument parser, along with their codes
        self.parser.add_argument('--date', '-d', action='store', dest='date', help='The date of the meeting.  Should be formatted like MM/DD/YY')
        self.parser.add_argument('--start', '-s', action='store', dest='startTime', help="The meeting's start time.  Formatted like HH:MM (Military Time)")
        self.parser.add_argument('--end', '-e', action='store', dest='endTime', help="The meeting's end time.  Formatted like HH:MM (Military Time)")
        self.parser.add_argument('--uploader', '-u', action='store', dest='uploaderName', help='The name of the person uploading the meeting minutes')
        self.parser.add_argument('--proceedings', '-p', action='store', dest='proceedings', help='The events of the meeting')
        self.parser.add_argument('--finances', '-f', action='store', dest='finances', help='Financial matters that occurred during the meeting')
        self.parser.add_argument('--location', '-l', action='store', dest='location', help="The meeting's location")
        self.parser.add_argument('--students', action='store', dest='students', help='A list of students present at the meeting')
        self.parser.add_argument('--settings', action='store_true', dest='settingsProvided', default=False, help='Provide this flag if you want to configure club settings.')
        # define settings related arguments
        self.parser.add_argument('--club_members', action='store', dest='club_members', help='configure which names are members in the club')
        self.parser.add_argument('--club_location', action='store', dest='club_location', help='configure where the default meeting location is')
        self.parser.add_argument('--club_startTime', action='store', dest='club_startTime', help='configure the default beginning time of meetings')
        self.parser.add_argument('--club_endTime', action='store', dest='club_endTime', help='configure the default end time of meetings')
        self.parser.add_argument('--club_author', action='store', dest='club_author', help='configure the defalt club author/scribe')
        self.parser.add_argument('--club_weekday', action='store', dest='club_weekday', help='configure the default day the club meets on.')
        # define auxiliary switches
        self.parser.add_argument('--no_upload', action='store_true', dest='noUpload', default=False)
        self.date = ''
        self.startTime = ''
        self.endTime = ''
        self.finances = ''
        self.location = ''
        self.proceedings = ''
        self.uploaderName = ''
        self.students = []
        self.absentStudents = []
        self.settingsProvided = False
        self.upload = True

    # ALL SET COMMANDS CHECK THE VALIDITY
    # OF THEIR INPUTS BY DESIGN

    #BEGIN PRIVATE METHODS

    def settingsQuery(self):
        return self.settingsProvided

    def noUpload(self):
        return (not self.upload)

    def _setDate(self, date):
        club = Club()
        # Check that the date is valid, and if it isn't keep looping until it is
        if not _dateValid(date, False) and club.settingDefined(Club.WEEKDAY_KEY_VALUE):
            date = getLastDate(club.getWeekday())
        while not _dateValid(date, True):
            # ask for a valid date again until we get one
            date = input('Enter a valid date.  Date should be Formatted like MM/DD/YY:')
        # If the date is valid, store in the date member
        self.date = date

    def _setStartTime(self, startTime):
        club = Club()
        if not _timeValid(startTime, False) and club.settingDefined(Club.START_TIME_KEY_VALUE):
            startTime = club.getStartTime()
        while not _timeValid(startTime, True):
            # ask for a valid start time again until we get one
            startTime = input('Enter a valid meeting start time.  Time should be formatted like HH:MM :')
        # If the time is valid, store this time in the meeting start time member
        self.startTime = startTime

    def _setEndTime(self, endTime):
        club = Club()
        if not _timeValid(endTime, False) and club.settingDefined(Club.END_TIME_KEY_VALUE):
            endTime = club.getEndTime()
        # Check that the End Time is valid
        while not _timeValid(endTime, True):
            #ask for a valid end time again until we get one
            endTime = input('Enter a valid meeting end time. Time should be formatted like HH:MM :')
        # If the time is valid, store this time in the meeting end time member
        self.endTime = endTime


    def _setFinances(self, msg):
        # Check if FinancesMsg is 'None' indicating that nothing has been passed
        if(msg == None):
            msg = 'No Financial Matters to Report.'
        # Check that the FinancesMsg is a valid string
        # If the financial message is valid, store it in the financial msg member
        if(_stringValid(msg, False)):
            self.finances = msg
        # Otherwise, if the FinancesMsg is an empty string, invalid, or not passed, construct a new string indicating no financial matters were discussed
        else:
            self.finances = NO_FINANCES_MESSAGE

    def _setLocation(self, location):
        club = Club()
        if not _stringValid(location, False) and club.settingDefined(Club.LOCATION_KEY_VALUE):
            location = club.getLocation()
        # Check that the location is a valid string
        # Check that the Location is not an empty string
        while(not _stringValid(location, False)):
            #initiate error handling.
            warnings.warn('Location specified is invalid.  You must specify a location.', UserWarning)
            location = input('Enter a valid meeting Location: ')
        # If it's valid, store it in the location member
        self.location = location

    def _setProceedings(self, proceedings):
        # Check that proceedings is a valid string
        while(not _stringValid(proceedings, False) or proceedings == None):
            warnings.warn('Proceedings string is invalid.  You must specify the events of the meeting.', UserWarning)
            proceedings = input('Enter the events of the meeting: ')
        # Set the proceedings member data
        self.proceedings = proceedings

    def _setUploaderName(self, uploaderName):
        club = Club()
        if(not _stringValid(uploaderName, False) and club.settingDefined(Club.AUTHOR_KEY_VALUE)):
            uploaderName = club.getAuthor()
        # Check that uploaderName is a valid string
        while(not _stringValid(uploaderName, False)):
        # If given an empty string, or nothing, convert to 'Unknown Author'
            uploaderName = AUTHOR_UNKNOWN_MESSAGE
        # Set the member Data
        self.uploaderName = uploaderName

    def _setStudents(self, students):
        # check that students is a valid string array
        while(not _isList(students) and (not _stringValid(students, False))):
            # issue a warning
            warnings.warn('List of students specified is invalid.', UserWarning)
            # ask the user for a list input of students that attended the meeting. Separate each name by a comma
            student_raw_list = raw_input('Enter the students present at the meeting.  Each name delimited by a comma : ')
            # form the list from a string delimited with commas
            students = student_raw_list.split(',')
        # set the member data
        self.students = students.split(',')
        #remove any leading or trailing whitespace for student names
        _removeArrayWhitespace(self.students)

    def _startTimeBeforeEndTime(self, startTime, endTime):
        # check that the end time is further along in the day than the start time
        # this assumes that both the start time and the end time HAVE been properly set by the user
        if(startTime is not None and endTime is not None):
            meetingStartTime = startTime
            meetingEndTime = endTime
            while True:
                try:
                    meetingStartTime = datetime.datetime.strptime(meetingStartTime, '%H:%M')
                    meetingEndTime = datetime.datetime.strptime(meetingEndTime, '%H:%M')
                except (TypeError, ValueError) as err:
                    warnings.warn('Times inputted were invalid!', UserWarning)
                # if the meeting started later than it ended, then there has been an input error
                if(meetingStartTime <= meetingEndTime):
                    break
                # if the start time is greater than the end time, let's ask for some valid input
                print('Your end time occurs before your start time! Refusing to continue!')
                meetingStartTime = input('Enter the meeting start time.  It should occur before the end time, and be a properly formatted string(HH:MM) (Military Time) : ')
                meetingEndTime = input('Enter the meeting end time.  It should occur after the start time, and be a properly formatted string(HH:MM) (Military Time) : ')

    #END PRIVATE METHODS

    def getDate(self):
        return self.date

    def getStartTime(self):
        return self.startTime

    def getEndTime(self):
        return self.endTime

    def getFinances(self):
        return self.finances

    def getLocation(self):
        return self.location

    def getProceedings(self):
        return self.proceedings

    def getUploaderName(self):
        return self.uploaderName

    def getStudents(self):
        return self.students

    # None indicates that there was an issue with settings.txt, and the members setting could not be retrieved
    # [] indicates there were no absent students
    # any other string will contain absent students
    # getAbsentStudents ASSUMES THAT SELF.STUDENTS IS POPULATED
    def getAbsentStudents(self):
        club = Club()
        # initialize a list to hold students that are absent from today's meeting
        absentStudents = []
        # grab a copy of the list of all the students present at the meeting
        studentsPresent = list(self.getStudents())
        # if there exists a club member list in settings
        if(club.settingDefined(club.MEMBERS_KEY_VALUE)):
            for i in range(0, len(studentsPresent)):
                # remove all whitespace, and convert to lowercase
                studentsPresent[i] = ''.join(studentsPresent[i].split()).lower()
            # grab a list of all the club's members
            studentsInClub = club.getMembers()
            # iterate through all the students in the club
            for student in studentsInClub:
                # remove all spaces
                # define a student_alias so we can keep the formatting of the original name
                student_alias = ''.join(student.split()).lower()
                # if the member was not one of the students present at the meeting
                if student_alias not in studentsPresent:
                    # they must be an absent student
                    # append their name to the list of absent students
                    absentStudents.append(student)
            if(not absentStudents):
                return ['No Student Absences to Report.']
            return absentStudents
        else:
            # return a consolation message in an array
            return ['Absent student data is not available for this meeting.']

    def getNewMembers(self):
        club = Club()
        # initialize a list to hold new members of the club
        newClubMembers = []
        # retrieve a list of all the club members
        studentsPresent = self.students
        #if the club's member field is defined in the club's settings
        if(club.settingDefined(club.MEMBERS_KEY_VALUE)):
            # retrieve a list of all the people present at the meeting
            studentsInClub = club.getMembers()
            # for each of the club member names, remove all whitespace.  Convert them to lower case
            for i in range(0, len(studentsInClub)):
                studentsInClub[i] = ''.join(studentsInClub[i].split()).lower()
            # for each of the students present, remove all whitespace.  Convert their names to lower case
            for student in studentsPresent:
                # define student alias so we can keep a properly formatted name for the list of new club members
                student_alias = ''.join(student.split()).lower()
                # if the student present is not a club member, they must be a new club member.
                if(student_alias not in studentsInClub):
                    # append their name to the list of new members
                    newClubMembers.append(student)
            # return the list
            return newClubMembers
        else:
            # return everyone that was present at the meeting
            return studentsPresent

    def _logNewMembers(self):
        # initialize a club object
        club = Club()
        # get a list of the new members of the club
        newMembers = self.getNewMembers()
        # if there are any, write these new members into settings
        if(len(newMembers) > 0):
            club.addToSettings(club.MEMBERS_KEY_VALUE, newMembers)

    def _setInstanceVariables(self, cliOptions):
        # ALL SET COMMANDS CHECK THE VALIDITY
        # OF THEIR INPUTS BY DESIGN
        self.upload = not cliOptions.noUpload
        # set the meeting's date
        self._setDate(cliOptions.date)
        # set the meeting's start time
        self._setStartTime(cliOptions.startTime)
        # set the meeting's end time
        self._setEndTime(cliOptions.endTime)
        # set the financial transactions
        self._setFinances(cliOptions.finances)
        # set the meeting's location
        self._setLocation(cliOptions.location)
        # set the events of the meeting
        self._setProceedings(cliOptions.proceedings)
        # set the name of the meeting note's author
        self._setUploaderName(cliOptions.uploaderName)
        # put down the students that attended the meeting
        self._setStudents(cliOptions.students)

    def _settingValid(self, key, value):
        # validate it using a time check
        formattedOptionValue = value.strip().lower()
        formattedKey = key.strip().lower()
        if('time' in formattedKey):
            return _timeValid(formattedOptionValue, True)
        else:
            return _stringValid(formattedOptionValue, False)

    def configureSettings(self, club, cliOptions):
        optionsDict = vars(cliOptions)
        for key in optionsDict:
            # if the key contains club, indicating that it is a settings flag, and it's not set to None
            optionValue = optionsDict[key]
            cliOptionDefined = optionValue is not None
            isSettingsOption = key.find(SETTINGS_PREFIX) is not -1
            if(isSettingsOption and (cliOptionDefined)):
                while(not self._settingValid(key, optionValue)):
                    optionValue = input('Enter a valid setting formatted correctly for setting: ' + key + ': ')
                # if the cli Option value provided has a comma in the string, it's a list
                if(optionValue.find(LIST_DELIMITER)):
                    # convert the value specified on the CLI to a list
                    optionValue = optionValue.split(LIST_DELIMITER)
                indexBeyondEndOfSettingsPrefix = key.find(SETTINGS_PREFIX) + len(SETTINGS_PREFIX)
                settings_key = key[indexBeyondEndOfSettingsPrefix:].strip()
                club.setSetting(settings_key, optionValue)

    def parseCommand(self):
        # command the internal argument parser to parse the arguments the user has supplied
        # grab the argparser namespace
        userSuppliedOptions = self.parser.parse_args()
        self.settingsProvided = userSuppliedOptions.settingsProvided
        if(not self.settingsProvided):
            self._setInstanceVariables(userSuppliedOptions)
            self._logNewMembers()
        else:
            # configure club settings stored in settings file under logs
            club = Club()
            self.configureSettings(club, userSuppliedOptions)
