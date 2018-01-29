import unittest
from RepetitionInterval import RepetitionIntervalClass, badModeException, badNumberOfModeParamaters, badParamater, unknownTimezone
import datetime
 

class test_RepetitionInterval(unittest.TestCase):
  def checkGotRightException(self, context, ExpectedException):
    if (context.exception != None):
      if (context.exception != ExpectedException):
        raise context.exception
    self.assertTrue(ExpectedException == context.exception)

  def checkNextRun(self, riOBj, curTime, expTime):
    nextRun = riOBj.getNextOccuranceDatetime(curTime)
    self.assertEqual(nextRun, expTime)

#-----------------------------------------------
# Helpers above actual tests below
#-----------------------------------------------

  def test_nextdateHourlyModeJustBeforeMinute(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,datetime.datetime(2016,1,5,14,2,59,0,None),datetime.datetime(2016,1,5,14,3,0,0,None))

  def test_nextdateHourlyModeExactlyInMinute(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,datetime.datetime(2016,1,14,14,3,0,0,None),datetime.datetime(2016,1,14,15,3,0,0,None))

  def test_nextdateHourlyModeJustAfterMinute(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,datetime.datetime(2016,1,14,14,3,1,0,None),datetime.datetime(2016,1,14,15,3,0,0,None))

  def test_nextdateHourlyModeLastMinuteDayBefore(self):
    ri = RepetitionIntervalClass("HOURLY:03")
    self.checkNextRun(ri,datetime.datetime(2016,1,14,23,3,1,0,None),datetime.datetime(2016,1,15,00,3,0,0,None))


#		//Daily Tests
#		numErrors += runNextDateTest("January 14, 2016 14:01:02","ND Daily","DAILY:15:07","January 14, 2016 15:07:00");
#		numErrors += runNextDateTest("January 14, 2016 16:01:02","ND Daily","DAILY:15:07","January 15, 2016 15:07:00");
#		numErrors += runNextDateTest("January 14, 2016 16:01:02","ND Daily","DAILY:15:07","January 15, 2016 15:07:00");


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


#public class RepetitionIntervalTest {
#	//Code Only for testing below ***********************************
#	//Expire 35 minutes past each hour
#	//Expire 1pm every day
#	//Expire 1pm every monday
#	//Expire 1pm every weekday
#	//Expire 1pm every Mon
#	//Expire 1pm every 1st of the month
#	//Expire 1pm every 5th of Jan, Nov
#	
#	//Returns number of errors
#	private static boolean  m_outputon = false;	
#	private static DateFormat m_dateFormat = new SimpleDateFormat("MMMM d, yyyy h:m:s", Locale.ENGLISH);
#	public static void equivTest(String p_in) throws Exception {
#		RepetitionInterval ri = new RepetitionInterval(p_in);
#		if (!ri.equals(new RepetitionInterval(ri.toString()))) throw new Exception("Equilivance Mismatch");
#	}


#	public static int runNextDateTest(String p_testAtDate, String p_testNam, String p_in, String p_expectedResult) {
#		int r = 0;
#		String output = "Test start:" + p_testNam;
#		RepetitionInterval ri = null;

#		try {
#			Date testAtDate = m_dateFormat.parse(p_testAtDate);
#			Date exp = m_dateFormat.parse(p_expectedResult);
#			ri = new RepetitionInterval(p_in);
#			
#			Date got = ri.getNextDate(testAtDate);
#			if (got==null) throw new Exception("Returned null string");
#			
#			if (!got.equals(exp)) throw new Exception(" Fail, start:" + testAtDate.toLocaleString() + " int:" + p_in + " expected:" + exp.toLocaleString() + " got:" + got.toLocaleString());
#			equivTest(p_in);
#		} catch (Exception e) {
#			//e.printStackTrace();
#			output += " ERR->" + e.getMessage() + " ******************";
#			r++;
#		}
#		
#		
#		if ((r>0) || m_outputon) {
#			System.out.println(output);
#		}
#		
#		return r;
#	}	

#		//MONTHLY Tests
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
#		
#		//OnMon Tests 
#		numErrors += runNextDateTest("January 13, 2016 11:07:00","ND ONMON TB","ONMON:15:07","January 18, 2016 15:07:00");
#		numErrors += runNextDateTest("January 13, 2016 18:07:00","ND ONMON TA","ONMON:15:07","January 18, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 11:07:00","ND ONMON d TB","ONMON:15:07","January 18, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 18:07:00","ND ONMON d TA","ONMON:15:07","January 25, 2016 15:07:00");

#		//OnTue Tests
#		numErrors += runNextDateTest("January 13, 2016 11:07:00","ND ONTUE TB","ONTUE:15:07","January 19, 2016 15:07:00");
#		numErrors += runNextDateTest("January 13, 2016 18:07:00","ND ONTUE TA","ONTUE:15:07","January 19, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 11:07:00","ND ONTUE d TB","ONTUE:15:07","January 19, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 18:07:00","ND ONTUE d TA","ONTUE:15:07","January 19, 2016 15:07:00");

#		//OnWed Tests
#		numErrors += runNextDateTest("January 13, 2016 11:07:00","ND ONWED TB","ONWED:15:07","January 13, 2016 15:07:00");
#		numErrors += runNextDateTest("January 13, 2016 18:07:00","ND ONWED TA","ONWED:15:07","January 20, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 11:07:00","ND ONWED d TB","ONWED:15:07","January 20, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 18:07:00","ND ONWED d TA","ONWED:15:07","January 20, 2016 15:07:00");

#		//OnThu Tests
#		numErrors += runNextDateTest("January 13, 2016 11:07:00","ND ONTHU TB","ONTHU:15:07","January 14, 2016 15:07:00");
#		numErrors += runNextDateTest("January 13, 2016 18:07:00","ND ONTHU TA","ONTHU:15:07","January 14, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 11:07:00","ND ONTHU d TB","ONTHU:15:07","January 21, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 18:07:00","ND ONTHU d TA","ONTHU:15:07","January 21, 2016 15:07:00");

#		//OnFri Tests
#		numErrors += runNextDateTest("January 13, 2016 11:07:00","ND ONFRI TB","ONFRI:15:07","January 15, 2016 15:07:00");
#		numErrors += runNextDateTest("January 13, 2016 18:07:00","ND ONFRI TA","ONFRI:15:07","January 15, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 11:07:00","ND ONFRI d TB","ONFRI:15:07","January 22, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 18:07:00","ND ONFRI d TA","ONFRI:15:07","January 22, 2016 15:07:00");

#		//OnSat Tests
#		numErrors += runNextDateTest("January 13, 2016 11:07:00","ND ONSAT TB","ONSAT:15:07","January 16, 2016 15:07:00");
#		numErrors += runNextDateTest("January 13, 2016 18:07:00","ND ONSAT TA","ONSAT:15:07","January 16, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 11:07:00","ND ONSAT d TB","ONSAT:15:07","January 23, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 18:07:00","ND ONSAT d TA","ONSAT:15:07","January 23, 2016 15:07:00");

#		//OnSun Tests
#		numErrors += runNextDateTest("January 13, 2016 11:07:00","ND ONSUN TB","ONSUN:15:07","January 17, 2016 15:07:00");
#		numErrors += runNextDateTest("January 13, 2016 18:07:00","ND ONSUN TA","ONSUN:15:07","January 17, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 11:07:00","ND ONSUN d TB","ONSUN:15:07","January 24, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 18:07:00","ND ONSUN d TA","ONSUN:15:07","January 24, 2016 15:07:00");

#		//Weekday Tests 
#		numErrors += runNextDateTest("January 17, 2016 11:07:00","ND WEEKDAY SUN TB","WEEKDAY:15:07","January 18, 2016 15:07:00");
#		numErrors += runNextDateTest("January 17, 2016 18:07:00","ND WEEKDAY SUN TA","WEEKDAY:15:07","January 18, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 11:07:00","ND WEEKDAY MON TB","WEEKDAY:15:07","January 18, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 18:07:00","ND WEEKDAY MON TA","WEEKDAY:15:07","January 19, 2016 15:07:00");
#		numErrors += runNextDateTest("January 22, 2016 11:07:00","ND WEEKDAY FRI TB","WEEKDAY:15:07","January 22, 2016 15:07:00");
#		numErrors += runNextDateTest("January 22, 2016 18:07:00","ND WEEKDAY FRI TA","WEEKDAY:15:07","January 25, 2016 15:07:00");
#		numErrors += runNextDateTest("January 23, 2016 11:07:00","ND WEEKDAY SAT TB","WEEKDAY:15:07","January 25, 2016 15:07:00");
#		numErrors += runNextDateTest("January 23, 2016 18:07:00","ND WEEKDAY SAT TA","WEEKDAY:15:07","January 25, 2016 15:07:00");
#		
#		//Weekend Tests
#		numErrors += runNextDateTest("January 17, 2016 11:07:00","ND WEEKEND SUN TB","WEEKEND:15:07","January 17, 2016 15:07:00");
#		numErrors += runNextDateTest("January 17, 2016 18:07:00","ND WEEKEND SUN TA","WEEKEND:15:07","January 23, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 11:07:00","ND WEEKEND MON TB","WEEKEND:15:07","January 23, 2016 15:07:00");
#		numErrors += runNextDateTest("January 18, 2016 18:07:00","ND WEEKEND MON TA","WEEKEND:15:07","January 23, 2016 15:07:00");
#		numErrors += runNextDateTest("January 22, 2016 11:07:00","ND WEEKEND FRI TB","WEEKEND:15:07","January 23, 2016 15:07:00");
#		numErrors += runNextDateTest("January 22, 2016 18:07:00","ND WEEKEND FRI TA","WEEKEND:15:07","January 23, 2016 15:07:00");
#		numErrors += runNextDateTest("January 23, 2016 11:07:00","ND WEEKEND SAT TB","WEEKEND:15:07","January 23, 2016 15:07:00");
#		numErrors += runNextDateTest("January 23, 2016 18:07:00","ND WEEKEND SAT TA","WEEKEND:15:07","January 24, 2016 15:07:00");
#		
#		
#		System.out.println("");
#		if (numErrors>0) {
#			fail(numErrors + " Tests failed!!!!!!!!!!!!!!!!");
#		}		
#	}


