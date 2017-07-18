#imports
#from docx import *
#import datetime

#MeetingDocument

#Instance Data
###############
#docPath: string stores path to the document.  Defined relative to the placement of MeetingDocument.py for portability
#timeCreated: string stores the timestamp marking when the meeting document was created
#author: string name of the author 'creating' the meeting document
#proceedings: string describes the events of the meeting
#location: string describes the location of the meeting
#date: string formatted like so: MM/DD/YY
#startTime: string stores the meeting's start time HH:MM
#endTime: string stores the time when the meeting ended HH:MM
#financialMsg: string/string array stores potential financial transactions between last meeting and now

#Static Class Data
#const AUTHOR_STUB
#const TITLE
#const TIME_BEGIN_STUB
#const TIME_END_STUB
#const DATE_STUB
#const FINANCES_STUB
#const LOCATION_STUB
#const PROCEEDINGS_STUB
#const FILE_STORAGE_PATH
#const DEAFULLT_MEETING_NOTES_NAME

#Methods

#constructor_method
#__init__()
    # get the author
    # get the date
    # get the beginning time
    # get the ending time
    # get financial messages, if any
    # get the location
    # get the proceedings
    # retrieve the current timestamp to append to this document's new filename
    # make the name
    # initialize + open the document
    # check that the document is opened and in a good state
    # if it is not, throw a BadDocumentState Error
    # save the document
    # get the current time, and store this into timeCreated

#returns true if all necessary fields have been supplied to this document by the argument parser
#returns false otherwise
#readyToWrite()

#write(msg, fontSize = 12, centering, bold, underline)
    # add a paragraph with msg to the document
    # adjust the font size of the paragraph's run
    # adjust the centering
    # make the message bold, if necessary
    # underline the message, if necessary

#writeAuthor()
    # define author message
    # write it (author message, 12 font size right alignment, no bold, no underline)
    # write a line break

#writeTitle()
    # define title message
    # write it (title message, 18 font size, center alignment, bold, no underline)
    # write a line break x2

#writeSectionHeader(headerMessage)
    # write header message (message, 14 font suze left alignment, bold, underline)
    #write a line break

#writeLineBreak()
    # write a message just containing a newline character, with no special formatting

#writeBulletList(stringArray)
    # append a newline onto every element except the last element of the stringArray
    # concatenate all the items together
    # write a new paragraph with the style 'ListBullet' (Bullet List)

#getTimeCreated()
    # return timeCreated

#getAuthor()
    # return author
    
#getTitle()
    # return title
