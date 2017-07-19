import datetime
import calendar
from enum import IntEnum

DAYS_IN_WEEK = 7

Weekday = IntEnum('Weekdays', 'monday tuesday wednesday thursday friday saturday sunday', start=0)

def getWeekday(date):
    return calendar.day_name[date.weekday()].lower()

def getLastDate(day):
    today = datetime.datetime.today()
    todayWeekday = today.weekday()
    offset = todayWeekday - Weekday[day]
    if(offset < 0):
        offset = DAYS_IN_WEEK - abs(offset)
    meetingDate = today - datetime.timedelta(days=offset)
    formattedMeetingDate = meetingDate.strftime('%m/%d/%y')
    return formattedMeetingDate
