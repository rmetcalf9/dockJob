import TestHelperSuperClass
from appObj import appObj
from encryption import decryptPassword, encryptPassword, getSafeSaltString, getSafePasswordString, getSalt, getSaltFromSafeSaltString, WrongPasswordException
import pytest


@pytest.mark.encryption
class test_encryption(TestHelperSuperClass.testHelperSuperClass):
  def test_saltGen(self):
      salt = getSalt(appObj.bcrypt)
      safeSalt = getSafeSaltString(appObj.bcrypt, salt)
      origSalt = getSaltFromSafeSaltString(safeSalt)

      self.assertEqual(salt, origSalt)

  def test_passwordEncrypt(self):
    for origPlainText in ["AAAAA","A", "AA", "AAA", "", "AAAAA\n\n\n", "AAAAA\0\0\0", "AAAAA\0\0\0sadrgfrg"]:
        password=getSafePasswordString("my simple password string")
        wrong_password=getSafePasswordString("my simple password stXring")
        salt=getSafeSaltString(appObj.bcrypt)

        cypherText = encryptPassword(appObj.bcrypt, origPlainText, salt, password)
        self.assertEqual(decryptPassword(appObj.bcrypt, cypherText, salt, password), origPlainText)
        wrongPasswordThrown = False
        try:
            self.assertNotEqual(decryptPassword(appObj.bcrypt, cypherText, salt, wrong_password), origPlainText)
        except WrongPasswordException:
            wrongPasswordThrown = True
        self.assertTrue(wrongPasswordThrown)
