from meeting_minutes.modules.input.MeetingInputParser import MeetingInputParser
from meeting_minutes.modules.MeetingDocument import MeetingDocument
from meeting_minutes.modules.upload.DriveUploader import DriveUploader

ip = MeetingInputParser()
ip.parseCommand()
if(not ip.settingsQuery()):
    md = MeetingDocument.MeetingDocument(ip)
    md.populate()
    if(not ip.noUpload()):
        du = DriveUploader()
        du.upload(md)
