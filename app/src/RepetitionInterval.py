from enum import Enum
import datetime
from datetime import timedelta
import pytz

badModeException = Exception('Bad Mode')
badNumberOfModeParamaters = Exception('Bad number of paramaters passed to mode')
badParamater = Exception('Bad paramater value')
unknownTimezone = Exception('Unknown Timezone')
missingTimezoneException = Exception('datetime objects passed must be timezone awear')

class ModeType(Enum):
  HOURLY = 1 #Single paramater which is the minute past the error
  DAILY = 2  #three params, minute, hour, days (+-+-+-- Each char represents DOW mon-sun + means include day, - do not), final paramater is the timezone the passed in date is
  MONTHLY = 3	#Same hour and minute each day of the month (24 hour clock)	"MONTHLY:13:39:3" = Run at 1:39pm each 3rd of month, final paramater is the timezone the passed in date is
  # params are always minute:hour:day

  #                       | HOURLY  | DAILY  | MONTHLY |
  # Has Day of month      |   no    |   no   |   yes   |
  # Has Days of week      |   no    |   yes  |   no    |
  # Cares about timezone  |   no    |   yes  |   yes   |

  def getExpectedNumParams(self):
    if (self == ModeType.HOURLY):
      return 1
    if (self == ModeType.DAILY):
      return 4
    if (self == ModeType.MONTHLY):
      return 4
    return -1

class RepetitionIntervalClass():
  mode = None;
  minute = -1;
  hour = -1; #hour in 24 hour format
  dayOfMonth = -1; #only used in monthly mode
  timezone = pytz.timezone("UTC")

  ##Array represent days to run pos 0 = Monday, 1 = Tuesday .. 6 = Sunday
  ## matches datetime.weekday function
  daysForDaily = [False,False,False,False,False,False,False]

  def __init__(self, intervalString):
    if (None == intervalString):
      raise badModeException
    a = intervalString.split(":")
    if (len(a) == 0):
      raise badModeException
    modeType = None
    a[0] = a[0].upper().strip()
    for name, curModeType in ModeType.__members__.items():
      if (curModeType.name == a[0]):
        modeType = curModeType
    if (None == modeType):
      raise badModeException
    if ((1+modeType.getExpectedNumParams()) != len(a)):
      raise badNumberOfModeParamaters
    self.mode = modeType

    #minute is always there and is always first param
    self.minute = a[1].strip()
    if (" " in self.minute):
      raise badParamater
    try:
      self.minute = int(self.minute)
    except ValueError:
      raise badParamater
    if (self.minute < 0):
      raise badParamater
    if (self.minute > 59):
      raise badParamater

    #work out hour always second param if it is there
    if (modeType.getExpectedNumParams() > 1):
      self.hour = a[2].strip()
      if (" " in self.hour):
        raise badParamater
      try:
        self.hour = int(self.hour)
      except ValueError:
        raise badParamater
      if (self.hour < 0):
        raise badParamater
      if (self.hour > 23):
        raise badParamater

    #work out thrid paramater if it is there
    if (modeType.getExpectedNumParams() > 2):
      if (modeType == modeType.DAILY):
        daysOfWeek = a[3].strip()
        if (len(daysOfWeek) != 7):
          raise badParamater
        numDays = 0
        for x in range(0, 6):
          if (daysOfWeek[x]=="+"):
            self.daysForDaily[x] = True
            numDays = numDays + 1
          elif (daysOfWeek[x]=="-"):
           self. daysForDaily[x] = False
          else:
            raise badParamater
        if (numDays == 0):
          raise badParamater
      else:
        self.dayOfMonth = a[3].strip()
        if (" " in self.dayOfMonth):
          raise badParamater
        try:
          self.dayOfMonth = int(self.dayOfMonth)
        except ValueError:
          raise badParamater
        if (self.dayOfMonth < 0):
          raise badParamater
        if (self.dayOfMonth > 31):
          raise badParamater

    #if it is there the 4th paramter is always the timezone the passed in date is.
    if (modeType.getExpectedNumParams() > 3):
      try:
        self.timezone = pytz.timezone(a[4].strip())
      except pytz.exceptions.UnknownTimeZoneError:
        raise unknownTimezone

  #We must do arethmetic in UTC only or datetime gives wrong answer
  def addTimeInUTC(self, time, amount):
    utctime = time.astimezone(pytz.timezone('UTC'))
    utctime += amount
    return utctime.astimezone(time.tzinfo)


  #Return True if the day passed in is present in the array
  def isValidDay(self, datetimeVal):
    return self.daysForDaily[datetimeVal.weekday()]

  #Returns the next time that the repetition interval defines according to the current datetime passed in
  def getNextOccuranceDatetime(self, curDateTime):
    if (curDateTime.tzinfo == None):
      raise missingTimezoneException
    if (self.mode == ModeType.HOURLY):
      # Tried using localize method here but it dosen't seem to work that way
      #  this way passes the tests
      nd = datetime.datetime(
        curDateTime.year,
        curDateTime.month,
        curDateTime.day,
        curDateTime.hour,
        self.minute,
        0,
        0,
        curDateTime.tzinfo
      )
      if (nd <= curDateTime):
        nd = self.addTimeInUTC(nd, timedelta(hours=1))
      return nd
    if (self.mode == ModeType.DAILY):
      nd = self.timezone.localize(datetime.datetime(
        curDateTime.year,
        curDateTime.month,
        curDateTime.day,
        self.hour,
        self.minute,
        0,
        0
      ))
      if (nd <= curDateTime):
        nd = self.addTimeInUTC(nd, timedelta(days=1))
      #keep incrementing the day value until it falls on a valid day
      while (self.isValidDay(nd) != True):
        nd = self.addTimeInUTC(nd, timedelta(days=1))
      return nd

    if (self.mode == ModeType.MONTHLY):
      nd = self.timezone.localize(datetime.datetime(
        curDateTime.year,
        curDateTime.month,
        self.dayOfMonth,
        self.hour,
        self.minute,
        0,
        0
      ))
      if (nd <= curDateTime):
        year = curDateTime.year
        month = curDateTime.month + 1
        if (month > 12):
          year = year + 1
          month = 1
        nd = self.timezone.localize(datetime.datetime(
          year,
          month,
          self.dayOfMonth,
          self.hour,
          self.minute,
          0,
          0
        ))
      return nd


    raise Exception('Mode Not Implemented')


