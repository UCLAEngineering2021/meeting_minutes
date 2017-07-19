# imports
import os
import sys
import warnings
import string

# SettingsHandler takes information from .txt settings file, and can pipe it into club instance data
SETTINGS_FILE_NAME = 'settings.txt'
TEMP_SETTINGS_FILE_NAME = 'newSettings.txt'
HOME_DIR = '~'
SETTINGS_FILE_PATH = '/Desktop/meeting_minutes/logs/'
SETTINGS_ASSIGNMENT_OP = '='
LIST_DELIMITER = ','

# Instance variables:
# dict: a dictionary mapping setting names to their respective values
#   members : a string list of all the club members
#   author: default meeting minutes author
#   weekday: enumerated value representing the day of the week
#   startTime: default start time
#   endTime: default end time
#   location: default meeting location, string room number

def _isList(candidate):
    return (type(candidate) is list or type(candidate) is tuple)

def _listToString(list):
    return LIST_DELIMITER.join(list)

class Settings:

    def __init__(self):
        home_dir = os.path.expanduser(HOME_DIR)
        # if the file exists
        if(os.path.isfile(home_dir + SETTINGS_FILE_PATH + SETTINGS_FILE_NAME)):
            # initialize dict by reading text file
            self.dict = self._readFile()
        # otherwise set dict values to None
        else:
            self.dict = None

    # return a dictionary
    def _readFile(self):
        dictionary = dict()
        home_dir = os.path.expanduser(HOME_DIR)
        full_file_path = home_dir + SETTINGS_FILE_PATH + SETTINGS_FILE_NAME
        # if the file exists
        if(os.path.isfile(full_file_path)):
            # open file
            with open(full_file_path, 'r') as f:
                # read all the lines of the file, storing the lines in an array
                lines = f.readlines()
                for line in lines:
                    if(SETTINGS_ASSIGNMENT_OP in line):
                        indexOfAssignmentOp = line.find(SETTINGS_ASSIGNMENT_OP)
                        key = (line[0:indexOfAssignmentOp]).strip()
                        value = (line[(indexOfAssignmentOp + 1):]).strip()
                        if(value.find(LIST_DELIMITER) is not -1):
                            value = value.split(LIST_DELIMITER)
                            for i in range(0, len(value)):
                                value[i] = value[i].strip()
                        dictionary[key] = value
            return dictionary
        # otherwise, stop
        else:
            warnings.warn('Settings File Does Not Exist.  Cannot Read.', UserWarning)
            return dict()

    # read returns a dictionary containing the key:value pairs that comprise dict
    def _readSettingsValue(self, setting):
        home_dir = os.path.expanduser(HOME_DIR)
        full_file_path = home_dir + SETTINGS_FILE_PATH + SETTINGS_FILE_NAME
        setting = setting.strip()
        if(os.path.isfile(full_file_path)):
            with open(full_file_path, 'r') as f:
                # read all the lines in the file, and store them into a list lines
                lines = f.readlines()
                for line in lines:
                    if((setting + SETTINGS_ASSIGNMENT_OP) in line):
                        # string.find() should never return -1, since it was found previously in order to enter this loop
                        settingValue = line[(line.find(SETTINGS_ASSIGNMENT_OP) + 1):].strip()
                        # if the value is a list
                        if(settingValue.find(LIST_DELIMITER) is not -1):
                            settingValues = settingValue.split(LIST_DELIMITER)
                            for i in range(0, len(settingValues)):
                                settingValues[i] = settingValues[i].strip()
                            return settingValues
                        return settingValue
        return None

    # read selected for a specific key returns the corresponding value from the instance variable dict
    def read(self, setting):
        if(setting is None):
            # if we've defined dict, then we shouldn't take the time to read the settings file, we should just
            # return dict itself
            if(self.dict is not None):
                return self.dict
            # if we haven't defined dict's values, then parse them from the settings file
            else:
                return self._readFile()
        else:
            if(self.dict is None):
                self.dict = dict()
            homeDir = os.path.expanduser(HOME_DIR)
            filePath = homeDir + SETTINGS_FILE_PATH + SETTINGS_FILE_NAME
            fileFound = os.path.isfile(filePath)
            if(fileFound):
                if(setting not in self.dict):
                    settings_value = self._readSettingsValue(setting)
                    return settings_value
                # if the dictionary setting has been defined
                else:
                    return self.dict[setting]
            else:
                return None
    # write finds the setting (key) specified clears the corresponding value of the settings file if needed, and inserts the new value inside
    def write(self, setting, value):
        # if member variable dict has not been initialized, initialize it so we can store new values in it
        if(self.dict is None):
            self.dict = dict()
        # find the actual name for the home directory, expanded from HOME_DIR (which is ~ on mac os x)
        homeDir = os.path.expanduser(HOME_DIR)
        # we are only writing to the new file, and overwriting any files with the same name
        newFilePermissions = 'w+'
        # now construct the full path to the old settings file and new settings file
        fullOldFilePath = homeDir + SETTINGS_FILE_PATH + SETTINGS_FILE_NAME
        fullNewFilePath = homeDir + SETTINGS_FILE_PATH + TEMP_SETTINGS_FILE_NAME
        # if the old file exists
        oldSettingsFileFound = os.path.isfile(fullOldFilePath)
        if(oldSettingsFileFound):
            # read all the values from the file into the dictionary
            self.dict = self._readFile()
        # replace or add the new settings value
        self.dict[setting] = value
        try:
            # open a new settings file or an existing one
            with open(fullNewFilePath, newFilePermissions) as f:
                # for every setting in our settings dictionary
                for settingKey in self.dict:
                    # write that setting key and value into the settings file
                    settingValue = self.dict[settingKey]
                    if(_isList(settingValue)):
                        settingValue = _listToString(settingValue)
                    f.write(settingKey + SETTINGS_ASSIGNMENT_OP + settingValue + '\n')
            # if we found an old settings file, then let's delete it
            if(oldSettingsFileFound):
                os.remove(fullOldFilePath)
            # now let's rename our temporary settings file that we wrote to into the permanent settings file
            os.rename(fullNewFilePath, fullOldFilePath)
            return True
        except:
            warnings.warn('File write operation unable to proceed.  Aborting file write operation.')
            return False

    def addTo(self, setting, addendum):
        # grab the current definition
        valueAtSetting = self._readSettingsValue(setting)
        if(not _isList(valueAtSetting) and valueAtSetting is not None):
            warnings.warn('At setting: ' + setting + '.  You may not add to a nonlist value!')
            return False
        elif(valueAtSetting is None):
            valueAtSetting = []
        try:
            for addendumItem in addendum:
                valueAtSetting.append(addendumItem)
            self.write(setting, valueAtSetting)
            return True
        except:
            warnings.warn('Value could not be appended to settings file!')
            return False

    def dictionary(self):
        return self.dict
