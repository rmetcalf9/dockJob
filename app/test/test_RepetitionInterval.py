import unittest
from RepetitionInterval import RepetitionIntervalClass, badModeException, badNumberOfModeParamaters, badParamater, unknownTimezone, missingTimezoneException
import datetime
from datetime import timedelta
import pytz

class test_RepetitionInterval(unittest.TestCase):
  def checkGotRightException(self, context, ExpectedException):
    if (context.exception != None):
      if (context.exception != ExpectedException):
        raise context.exception
    self.assertTrue(ExpectedException == context.exception)

  def checkNextRun(self, riOBj, curTime, expTime):
    nextRun = riOBj.getNextOccuranceDatetime(curTime)
    if (nextRun != expTime):
      print("Next Run:" + str(nextRun))
      print("Expected:" + str(expTime))
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

  def test_nextdateHourlyModeJustBeforeMinute(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,datetime.datetime(2016,1,5,14,2,59,0,pytz.timezone('Europe/London')),datetime.datetime(2016,1,5,14,3,0,0,pytz.timezone('Europe/London')))

  def test_nextdateHourlyModeExactlyInMinute(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,datetime.datetime(2016,1,14,14,3,0,0,pytz.timezone('Europe/London')),datetime.datetime(2016,1,14,15,3,0,0,pytz.timezone('Europe/London')))

  def test_nextdateHourlyModeJustAfterMinute(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,datetime.datetime(2016,1,14,14,3,1,0,pytz.timezone('Europe/London')),datetime.datetime(2016,1,14,15,3,0,0,pytz.timezone('Europe/London')))

  def test_nextdateHourlyModeLastMinuteDayBefore(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,datetime.datetime(2016,1,14,23,3,1,0,pytz.timezone('Europe/London')),datetime.datetime(2016,1,15,00,3,0,0,pytz.timezone('Europe/London')))

  def test_HourlyBeforeDSTJumpForward(self):
    #25 mar 2018 1am becomes 2am
    # there won't be a 1:03 so it should jump to 2:03
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,pytz.timezone('Europe/London').localize(datetime.datetime(2018,3,25,0,30,0,0)),pytz.timezone('Europe/London').localize(datetime.datetime(2018,3,25,2,3,0,0)))

  def test_HourlyBeforeDSTJumpBack(self):
    #29 oct 2018 2am becomes 1am
    # there won't be a 1:03 so it should jump to 2:03`
    ri = RepetitionIntervalClass("HOURLY:03")
    # the time 1:03 can't be represented in Europe/London as it has two UTC values
    # so the test specifies a UTC time
    self.checkNextRun(ri,pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,29,0,30,0,0)),pytz.timezone('UTC').localize(datetime.datetime(2018,10,29,1,3,0,0)))


# Daily Tests
## Every day of week
  def test_DailyEveryDayOnThatDay(self):
    ri = RepetitionIntervalClass("DAILY:03:15:+++++++:Europe/London")
    self.checkNextRun(ri,pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,29,0,30,0,0)),pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,29,15,3,0,0)))

  def test_DailyEveryDayOnPrevDay(self):
    ri = RepetitionIntervalClass("DAILY:03:15:+++++++:Europe/London")
    self.checkNextRun(ri,pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,29,16,30,0,0)),pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,30,15,3,0,0)))

## Only on Wednesdays
  def test_DailyEveryDayOnWed(self):
    ri = RepetitionIntervalClass("DAILY:03:15:--+----:Europe/London")
    self.checkNextRun(ri,pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,29,16,30,0,0)),pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,31,15,3,0,0)))

## Only on Fridays
  def test_DailyEveryDayOnFri(self):
    ri = RepetitionIntervalClass("DAILY:03:15:----+--:Europe/London")
    self.checkNextRun(ri,pytz.timezone('Europe/London').localize(datetime.datetime(2018,10,29,16,30,0,0)),pytz.timezone('Europe/London').localize(datetime.datetime(2018,11,2,15,3,0,0)))

# MONTHLY Tests
#		numErrors += runNextDateTest("January 13, 2016 14:01:02","ND Monthly day before TB","MONTHLY:15:07:14","January 14, 2016 15:07:00");
#		numErrors += runNextDateTest("January 14, 2016 14:01:02","ND Monthly same day TB","MONTHLY:15:07:14","January 14, 2016 15:07:00");
#		numErrors += runNextDateTest("January 15, 2016 14:01:02","ND Monthly day after TB","MONTHLY:15:07:14","February 14, 2016 15:07:00");

#		numErrors += runNextDateTest("January 13, 2016 15:07:00","ND Monthly day before TM","MONTHLY:15:07:14","January 14, 2016 15:07:00");
#		numErrors += runNextDateTest("January 14, 2016 15:07:00","ND Monthly same day TM","MONTHLY:15:07:14","February 14, 2016 15:07:00");
#		numErrors += runNextDateTest("January 15, 2016 15:07:00","ND Monthly day after TM","MONTHLY:15:07:14","February 14, 2016 15:07:00");
#		
#		numErrors += runNextDateTest("January 13, 2016 16:07:00","ND Monthly day before TA","MONTHLY:15:07:14","January 14, 2016 15:07:00");
#		numErrors += runNextDateTest("January 14, 2016 16:07:00","ND Monthly same day TA","MONTHLY:15:07:14","February 14, 2016 15:07:00");
#		numErrors += runNextDateTest("January 15, 2016 16:07:00","ND Monthly day after TA","MONTHLY:15:07:14","February 14, 2016 15:07:00");


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



