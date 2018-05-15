from TestHelperSuperClass import testHelperSuperClass
from RepetitionInterval import RepetitionIntervalClass, badModeException, badNumberOfModeParamaters, badParamater, unknownTimezone, missingTimezoneException, curDateTimeTimezoneNotUTCException
import datetime
from datetime import timedelta
import pytz

class test_RepetitionInterval(testHelperSuperClass):
  def checkNextRun(self, riOBj, curTime, expTime, msg=''):
    nextRun = riOBj.getNextOccuranceDatetime(curTime)
    if str(nextRun.tzinfo) != 'UTC':
      self.assertTrue(False, msg='Repetition Interval did not return next run in UTC (' + str(nextRun.tzinfo) + ')')
    expTimeUTC = expTime.astimezone(pytz.timezone('UTC'))
    if (nextRun != expTimeUTC):
      print("Next Run:" + str(nextRun) + ' (Always UTC)')
      print("Expected:" + str(expTime) + ' (Expected UTC=' + str(expTimeUTC) + ')')
      print(msg)
    self.assertEqual(nextRun, expTime)

#-----------------------------------------------
# Helpers above actual tests below
#-----------------------------------------------

# HOURLY TESTS
  def test_PassedInDatetimeMustBeTimezoneAwear(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    with self.assertRaises(Exception) as context:
      nextRun = ri.getNextOccuranceDatetime(datetime.datetime(2016,1,5,14,2,59,0,None))
    self.checkGotRightException(context,missingTimezoneException)

  def test_PassedInDatetimeMustBeUTC(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    with self.assertRaises(Exception) as context:
      nextRun = ri.getNextOccuranceDatetime(datetime.datetime(2016,1,5,14,2,59,0,pytz.timezone('Europe/London')))
    self.checkGotRightException(context,curDateTimeTimezoneNotUTCException)

  def test_nextdateHourlyModeJustBeforeMinute(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(
      ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,5,14,2,59,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,5,14,3,0,0))
    )
    self.assertEqual(ri.__str__(),'HOURLY:03')

  def test_nextdateHourlyModeExactlyInMinute(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,14,3,0,0)),pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,14,15,3,0,0)))

  def test_nextdateHourlyModeJustAfterMinute(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,14,3,1,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,14,15,3,0,0))
    )

  def test_nextdateHourlyModeLastMinuteDayBefore(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,
      curTime=pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,23,3,1,0)),
      expTime=pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,15,00,3,0,0))
    )

  def test_HourlyBeforeDSTJumpForward(self):
    #25 mar 2018 1am becomes 2am
    # there won't be a 1:03 so it should jump to 2:03
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,3,25,0,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,3,25,2,3,0,0))
    )

  def test_HourlyBeforeDSTJumpBack(self):
    #29 oct 2018 2am becomes 1am
    # there won't be a 1:03 so it should jump to 2:03`
    ri = RepetitionIntervalClass("HOURLY:03")
    # the time 1:03 can't be represented in Europe/London as it has two UTC values
    # so the test specifies a UTC time
    self.checkNextRun(ri,pytz.timezone('UTC').localize(datetime.datetime(2018,10,29,0,30,0,0)),pytz.timezone('UTC').localize(datetime.datetime(2018,10,29,1,3,0,0)))

  def test_hourlySingleDigitMinute(self):
    ri = RepetitionIntervalClass("HOURLY:3")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,23,3,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,15,00,3,0,0))
    )
    self.assertEqual(ri.__str__(),'HOURLY:03')


  def test_hourlyZeroMinute(self):
    ri = RepetitionIntervalClass("HOURLY:0")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,23,3,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,15,00,0,0,0))
    )
    self.assertEqual(ri.__str__(),'HOURLY:00')

  def test_hourlyDoubleZeroMinute(self):
    ri = RepetitionIntervalClass("HOURLY:00")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,23,3,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,15,00,0,0,0))
    )
    self.assertEqual(ri.__str__(),'HOURLY:00')

  def test_hourlyInvalidMinute(self):
    with self.assertRaises(Exception) as context:
      ri = RepetitionIntervalClass("HOURLY:60")
    self.checkGotRightException(context,badParamater)

  def test_hourlyFourTimesPerHour(self):
    ri = RepetitionIntervalClass("HOURLY:0,15,30,45")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,0,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,15,0,0))
    )
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,16,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,30,0,0))
    )
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,31,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,45,0,0))
    )
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,46,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,14,0,0,0))
    )
    self.assertEqual(ri.__str__(),'HOURLY:00,15,30,45')

  def test_hourlyFourTimesPerHourMutipleSameValues(self):
    ri = RepetitionIntervalClass("HOURLY:0,15,30,45,45")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,0,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,15,0,0))
    )
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,16,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,30,0,0))
    )
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,31,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,45,0,0))
    )
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,46,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,14,0,0,0))
    )
    self.assertEqual(ri.__str__(),'HOURLY:00,15,30,45')

  def test_hourlyFourTimesPerHourWrongORder(self):
    ri = RepetitionIntervalClass("HOURLY:0,30,15,45")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,0,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,15,0,0))
    )
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,16,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,30,0,0))
    )
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,31,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,45,0,0))
    )
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,13,46,1,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,14,0,0,0))
    )
    self.assertEqual(ri.__str__(),'HOURLY:00,15,30,45')

  def test_hourlyFourTimesPerHourInvalid(self):
    with self.assertRaises(Exception) as context:
      ri = RepetitionIntervalClass("HOURLY:0,30,61,45")
    self.checkGotRightException(context,badParamater)

# Daily Tests
## Every day of week
  def test_DailyEveryDayOnThatDay(self):
    ri = RepetitionIntervalClass("DAILY:03:15:+++++++:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,10,29,0,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,29,15,3,0,0))
    )

    #6 may 2018 is a sunday. Check at 4 o'clock for next 3 weeks we have correct next runs (always the next day)
    #  3 weeks won't go over month boundary
    days_of_week = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
    cur_day_of_week = 6
    for DayOfMonthBeforeRunIsDue in range(6,6+(3*7)):
      #cur_day_of_week = cur_day_of_week+1
      if cur_day_of_week > 6:
        cur_day_of_week = 0
      print(DayOfMonthBeforeRunIsDue)
      self.checkNextRun(ri,
        pytz.timezone('UTC').localize(datetime.datetime(2018,5,DayOfMonthBeforeRunIsDue,16,30,0,0)),
        pytz.timezone('Europe/London').localize(datetime.datetime(2018,5,(DayOfMonthBeforeRunIsDue+1),15,3,0,0)),
        'Test was for ' + days_of_week[cur_day_of_week]
      )
    self.assertEqual(ri.__str__(),'DAILY:03:15:+++++++:Europe/London')


  def test_DailyEveryDayOnPrevDay(self):
    ri = RepetitionIntervalClass("DAILY:03:15:+++++++:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,10,29,16,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,30,15,3,0,0))
    )

## Only on Wednesdays
  def test_DailyEveryDayOnWed(self):
    ri = RepetitionIntervalClass("DAILY:03:15:--+----:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,10,29,16,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,31,15,3,0,0))
    )

## Only on Fridays
  def test_DailyEveryDayOnFri(self):
    ri = RepetitionIntervalClass("DAILY:03:15:----+--:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,10,29,16,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,11,2,15,3,0,0))
    )

## Only on Sundays
  def test_DailyEveryDayOnSun(self):
    ri = RepetitionIntervalClass("DAILY:03:15:------+:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,10,29,16,30,0,0)),
      pytz.timezone('UTC').localize(datetime.datetime(2018,11,4,15,3,0,0))
    )

# MONTHLY Tests
  def test_MonthlyDayBefore(self):
    ri = RepetitionIntervalClass("MONTHLY:03:15:11:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,10,10,16,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,11,15,3,0,0))
    )
    self.assertEqual(ri.__str__(),'MONTHLY:03:15:11:Europe/London')

  def test_MonthlySingleDigitConversion(self):
    ri = RepetitionIntervalClass("MONTHLY:0:5:1:Europe/London")
    self.assertEqual(ri.__str__(),'MONTHLY:00:05:01:Europe/London')


  def test_MonthlyDayBeforeBST(self):
    ri = RepetitionIntervalClass("MONTHLY:03:15:11:Europe/London")
    # Next run Expected result is in Europe/London
    self.checkNextRun(
      ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,3,27,16,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,4,11,15,3,0,0))
    )

  def test_MonthlyOnDayTimeBefore(self):
    ri = RepetitionIntervalClass("MONTHLY:03:15:11:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,10,11,10,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,11,15,3,0,0))
    )

  def test_MonthlyOnDayTimeAfter(self):
    ri = RepetitionIntervalClass("MONTHLY:03:15:11:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,10,11,16,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,11,11,15,3,0,0))
    )

  def test_MonthlyDayAfter(self):
    ri = RepetitionIntervalClass("MONTHLY:03:15:11:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,10,12,16,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2018,11,11,15,3,0,0))
    )

  def test_MonthlyYearRollover(self):
    ri = RepetitionIntervalClass("MONTHLY:03:15:11:Europe/London")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2018,12,12,16,30,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2019,1,11,15,3,0,0))
    )

# class init tests
  def test_initWithNoneRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass(None)
    self.checkGotRightException(context,badModeException)
  def test_initWithNonsenseRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("Null mode")
    self.checkGotRightException(context,badModeException)

  def test_initWithEmptyStringRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("")
    self.checkGotRightException(context,badModeException)

  def test_initWithOneColonStringRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("aa:bb")
    self.checkGotRightException(context,badModeException)

  def test_initWithTwoColonStringRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("aa:bb:cc")
    self.checkGotRightException(context,badModeException)

  def test_initWithJustColonStringRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass(":")
    self.checkGotRightException(context,badModeException)

  def test_initWithJustDotStringRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass(".")
    self.checkGotRightException(context,badModeException)

  def test_initHourlyWithNoParamsRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("HOURLY")
    self.checkGotRightException(context,badNumberOfModeParamaters)

  def test_initHourlyWithOneParamHasNoException(self):
    a = RepetitionIntervalClass("HOURLY:12")

  def test_initModeTypeRecognisedIrrespectiveOfCase(self):
    a = RepetitionIntervalClass("HOuRLY:12")

  def test_initModeTypeRecognisedIrrespectiveOfPreSpaces(self):
    a = RepetitionIntervalClass("   HOuRLY:12")

  def test_initModeTypeRecognisedIrrespectiveOfPostSpaces(self):
    a = RepetitionIntervalClass("HOuRLY   :12")

  def test_initModeTypeRecognisedIrrespectiveOfPreandPostSpaces(self):
    a = RepetitionIntervalClass("   HOuRLY    :12")

  def test_initModeTypeWithTooManyParams(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("HOURLY:12:4:4:54:ffd:d4:34")
    self.checkGotRightException(context,badNumberOfModeParamaters)

  def test_iniInternalSpaceInFirstParamReturnsError(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("HOURLY:1 2")
    self.checkGotRightException(context,badParamater)

  def test_iniMinuteValueTooHigh(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("HOURLY:61")
    self.checkGotRightException(context,badParamater)

  def test_iniMinuteValueTooLow(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("HOURLY:-12")
    self.checkGotRightException(context,badParamater)

  def test_iniMinuteValueNotANumber(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("HOURLY:ABC")
    self.checkGotRightException(context,badParamater)

  def test_initMonthlyWithNoParamsRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY")
    self.checkGotRightException(context,badNumberOfModeParamaters)

  def test_initMonthlyWithOneParamRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY:12")
    self.checkGotRightException(context,badNumberOfModeParamaters)

  def test_initMonthlyWithTwoParamsRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY:12:12")
    self.checkGotRightException(context,badNumberOfModeParamaters)

  def test_initMonthlyOK(self):
    a = RepetitionIntervalClass("MONTHLY:59:23:11:UTC")

  def test_initInvalidMinuteRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY:61:01:11:UTC")
    self.checkGotRightException(context,badParamater)

  def test_initInvalidHourRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY:01:61:11:UTC")
    self.checkGotRightException(context,badParamater)

  def test_initInvalidDayRaisesException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY:01:01:32:UTC")
    self.checkGotRightException(context,badParamater)

  def test_initDatOfMonthNotIntException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY:01:01:ABC:UTC")
    self.checkGotRightException(context,badParamater)

  def test_initDatOfMonthWithSpaceException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY:01:01:1 1:UTC")
    self.checkGotRightException(context,badParamater)

  def test_initDatNotIntException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY:01:1 1:1:UTC")
    self.checkGotRightException(context,badParamater)

  def test_initDayWithSpaceException(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("MONTHLY:01:ABC:1:UTC")
    self.checkGotRightException(context,badParamater)

  def test_initDailyWithInvalidNumParams(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("DAILY:1:dd:£:$:5:6")
    self.checkGotRightException(context,badNumberOfModeParamaters)

  def test_initDaily(self):
    a = RepetitionIntervalClass("DAILY:1:11:+++++--:UTC")

  def test_initDailyWithInvalidTimezone(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("DAILY:1:11:+++++--:dfsf")
    self.checkGotRightException(context,unknownTimezone)

  def test_initDailyWithWrongNumberOfChars(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("DAILY:1:11:+++++:UTC")
    self.checkGotRightException(context,badParamater)

  def test_initDailyWithInvalidChar(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("DAILY:1:11:+++++XX:UTC")
    self.checkGotRightException(context,badParamater)

  def test_initDailyWithNoneTimezoneErrors(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("DAILY:1:11:+++++++:None")
    self.checkGotRightException(context,unknownTimezone)

  def test_initDailyWithNoDaysErrors(self):
    with self.assertRaises(Exception) as context:
      a = RepetitionIntervalClass("DAILY:1:11:-------:UTC")
    self.checkGotRightException(context,badParamater)



