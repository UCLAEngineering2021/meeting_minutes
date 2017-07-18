import sys
import os.path
sys.path.append('~/Desktop')
from meeting_minutes.modules.input.MeetingInputParser import MeetingInputParser
from meeting_minutes.modules.MeetingDocument import MeetingDocument
from meeting_minutes.modules.upload.DriveUploader import DriveUploader

ip = MeetingInputParser()
ip.parseCommand(['--proceedings', 'President Julia Moseyko discussed Neural Networks and Artificial Intelligence, helping the club to code the backprogagation portion of their neural networks.  Progress was made on multiple drone swarm control by club member Jaiden Aengus.',
'--students', 'Julia Moseyko,Will Fehrnstrom,Phoenix Kang,Isaac Pugh,Will Stenzel,Jordan Grelling,Athan Chan,Chaz Michaels Michaels'])
#ip.parseCommand(['--settings', '--club_weekday', 'tuesday'])
if(not ip.settingsQuery()):
    md = MeetingDocument.MeetingDocument(ip)
    md.populate()
    if(not ip.noUpload()):
        du = DriveUploader()
        du.upload(md)
