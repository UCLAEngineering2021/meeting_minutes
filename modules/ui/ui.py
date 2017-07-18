from . import UIType

#Type can be either CLI (Command Line Interface), or GUI. GUI is unsupported as of 7/9/17, but may be added in the future
_type = UIType.UIType.CLI
#If debug is true, program crashes harder on an error
_debug = True

def getUIType():
    global _type
    return _type

def inDebugMode():
    global _debug
    return _debug

def displayError(error):
    print('Inside Display Error')
    if(getUIType() == ui.UIType.UIType.CLI):
        print(error)

# def logError(error):
