import sys
import os.path
sys.path.append('~/Desktop')
from meeting_minutes.modules.input.MeetingInputParser import MeetingInputParser

ip = MeetingInputParser()
# test for all valid inputs
print('TEST 1: ALL VALID.\n')
ip.parseCommand(['--date', '10/10/10', '--start', '10:10', '--end', '10:40', '--proceedings', 'Not too much.', '--location', 'Orinda', '--uploader', 'Will Fehrnstrom', '--students', 'Julia Moseyko, Will Fehrnstrom, Phoenix Kang'])
#    print('All Valid Inputs Test: Pass.')
#    print('All Valid Inputs Test: Fail.')
print('\n')
# test for a beginning time less than an end time
print('TEST 2: START TIME AFTER END TIME.\n')
try:
    ip.parseCommand(['--date', '10/10/10', '--start', '10:40', '--end', '10:10', '--proceedings', 'Not too much.', '--location', 'Orinda', '--uploader', 'Will Fehrnstrom', '--students', 'Julia Moseyko, Will Fehrnstrom, Phoenix Kang'])
    print('End Time Before Start Time Inputs Test: Pass.')
except:
    print('End Time Before Start Time Inputs Test: Fail.')
print('\n')
#test for the case where no finances are passed
print('TEST 3: NO FINANCES GIVEN\n')
try:
    ip.parseCommand(['--date', '10/10/10', '--start', '10:10', '--end', '10:40', '--proceedings', 'Not too much.', '--location', 'Orinda', '--uploader', 'Will Fehrnstrom', '--students', 'Julia Moseyko, Will Fehrnstrom, Phoenix Kang'])
except:
    print('No Finances Given: Fail.')
