import TestHelperSuperClass
from RepetitionInterval import ModeType, RepetitionIntervalClass, badModeException, badNumberOfModeParamaters, badParamater, unknownTimezone, missingTimezoneException, curDateTimeTimezoneNotUTCException
import datetime
from datetime import timedelta
import pytz
from test_RepetitionInterval import repetitionIntervalHelper
from sortedcontainers import SortedDict

#@TestHelperSuperClass.wipd
class test_RepetitionIntercal_SetHourMode(repetitionIntervalHelper):
  def test_WrongNumberOfParams(self):
    with self.assertRaises(Exception) as context:
      ri = RepetitionIntervalClass("SETHOUR:03:1,2,3:UTC:A:B:C")
    self.checkGotRightException(context,badNumberOfModeParamaters)

  def test_PassedInDatetimeMustHaveHours(self):
    with self.assertRaises(Exception) as context:
      ri = RepetitionIntervalClass("SETHOUR:03::UTC")
    self.checkGotRightException(context,badParamater)

  def test_PassedInDatetimeMustHaveTimezoneType(self):
    with self.assertRaises(Exception) as context:
      ri = RepetitionIntervalClass("SETHOUR:03:1:")
    self.checkGotRightException(context,unknownTimezone)

  def test_PassedInDatetimeMustBeUTC(self):
    ri = RepetitionIntervalClass("SETHOUR:03:1,2,3:UTC")
    with self.assertRaises(Exception) as context:
      nextRun = ri.getNextOccuranceDatetime(datetime.datetime(2016,1,5,14,2,59,0,pytz.timezone('Europe/London')))
    self.checkGotRightException(context,curDateTimeTimezoneNotUTCException)

  def test_InitValueCheck(self):
    ri = RepetitionIntervalClass("SETHOUR:03:1,2,3:UTC")
    self.assertEqual(ri.mode, ModeType.SETHOUR)
    self.assertEqual(ri.minute, 3)
    self.assertEqual(ri.sethourModeHours, SortedDict({1: 1, 2: 2, 3: 3}))
    self.assertEqual(ri.timezone, pytz.timezone("UTC"))
    self.assertEqual(str(ri), "SETHOUR:03:01,02,03:UTC")

  def test_HourOrderNotMatter(self):
    ri = RepetitionIntervalClass("SETHOUR:03:1,5,3:UTC")
    self.assertEqual(ri.mode, ModeType.SETHOUR)
    self.assertEqual(ri.minute, 3)
    self.assertEqual(ri.sethourModeHours, SortedDict({1: 1, 3: 3, 5: 5}))
    self.assertEqual(ri.timezone, pytz.timezone("UTC"))
    self.assertEqual(str(ri), "SETHOUR:03:01,03,05:UTC")

  def test_RepeatedHoursRemoved(self):
    ri = RepetitionIntervalClass("SETHOUR:03:1,5,3,1,1,1,3,5:UTC")
    self.assertEqual(ri.mode, ModeType.SETHOUR)
    self.assertEqual(ri.minute, 3)
    self.assertEqual(ri.sethourModeHours, SortedDict({1: 1, 3: 3, 5: 5}))
    self.assertEqual(ri.timezone, pytz.timezone("UTC"))
    self.assertEqual(str(ri), "SETHOUR:03:01,03,05:UTC")

  def test_oneHourInterval_startingbeforehour_shouldPushForwardSameDay(self):
    ri = RepetitionIntervalClass("SETHOUR:03:15:UTC")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,14,3,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,14,15,3,0,0))
    )

  def test_oneHourInterval_exacttime_shouldPushForwardToNextDay(self):
    ri = RepetitionIntervalClass("SETHOUR:03:15:UTC")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,15,3,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,15,15,3,0,0))
    )

  def test_oneHourInterval_after_shouldPushForwardToNextDay(self):
    ri = RepetitionIntervalClass("SETHOUR:03:15:UTC")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,15,3,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,15,15,3,0,0))
    )

  def test_twoHourInterval_startingbeforehour_shouldPushForwardSameDay(self):
    ri = RepetitionIntervalClass("SETHOUR:03:15,18:UTC")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,14,3,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,14,15,3,0,0))
    )

  def test_twoHourInterval_middletime_shouldPushForwardToNextHour(self):
    ri = RepetitionIntervalClass("SETHOUR:03:15,18:UTC")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,16,3,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,14,18,3,0,0))
    )

  def test_twoHourInterval_after_shouldPushForwardToNextDay(self):
    ri = RepetitionIntervalClass("SETHOUR:03:15,18:UTC")
    self.checkNextRun(ri,
      pytz.timezone('UTC').localize(datetime.datetime(2016,1,14,19,3,0,0)),
      pytz.timezone('Europe/London').localize(datetime.datetime(2016,1,15,15,3,0,0))
    )
