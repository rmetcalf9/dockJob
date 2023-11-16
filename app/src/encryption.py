from Crypto.Cipher import AES
####from Crypto.Random import OSRNG Deprecated in pycryptodome https://pycryptodome.readthedocs.io/en/latest/src/vs_pycrypto.html
from base64 import b64decode, b64encode
import Crypto.Random

class WrongPasswordException(Exception):
  pass

'''
Test code put in console to make sure Javascript and Python matches
Python Encryption

2020-04-14 - Replaced pycrypto with PyCryptodome
In future I want to look at the new python crypto library which may be simplier to use
https://pypi.org/project/cryptography/
See https://theartofmachinery.com/2017/02/02/dont_use_pycrypto.html

from Crypto.Cipher import AES
from Crypto.Random import OSRNG
from base64 import b64decode, b64encode
from encryption import pad, unpad, __INT__get32BytesFromSalt

passphraseBase64 = b64encode('tyttt'.encode())
passphrase = __INT__get32BytesFromSalt(b64decode(passphraseBase64))
plainText='aa'
IV=b'\xffH\x93\xdeh\xd1\xcd\xab1;ZSB\x08\x19\n'

##print(bytes(IV).hex())

aes = AES.new(passphrase, AES.MODE_CBC, IV)
cipherText = aes.encrypt(pad(plainText))

print("Base64 IV:", b64encode(IV).decode("utf-8"))
print("HEX IV:", bytes(IV).hex())
print("Result cipherText = ", b64encode(cipherText).decode("utf-8"))


##  Fbv+GmrmrO+YeLfm/g2kVw==


Javascript Encryption

console.log('CryptoJS:', CryptoJS)
function get32BytesFromSalt (salt) {
  var retBytes = ''
  for (let i = 0; i < 32; i++) {
    retBytes += salt[i % salt.length]
  }
  // idx = x % len(salt)
  // retBytes = retBytes + salt[idx:(idx+1)]
  return retBytes
}

var passphraseBase64=btoa('tyttt')
var passphrase = get32BytesFromSalt(atob(passphraseBase64))
var plainText = 'aa'
// var IV = CryptoJS.lib.WordArray.random(16)
var IV = CryptoJS.enc.Base64.parse("/0iT3mjRzasxO1pTQggZCg==")
var passphraseWordArray = CryptoJS.enc.Base64.parse(btoa(passphrase))

var enc_options = {
  iv: IV,
  mode: CryptoJS.mode.CBC,
  padding: CryptoJS.pad.Pkcs7,
}
var encrypted = CryptoJS.AES.encrypt(plainText, passphraseWordArray, enc_options)

console.log("Result IV = ", IV.toString(CryptoJS.enc.Base64))
console.log("Result cipherText = ", encrypted.ciphertext.toString(CryptoJS.enc.Base64))


// Fbv+GmrmrO+YeLfm/g2kVw==


'''

def __INT__get32BytesFromSalt(salt):
  retBytes = b''
  for x in range(0,32):
    idx = x % len(salt)
    retBytes = retBytes + salt[idx:(idx+1)]

  return retBytes


BLOCK_SIZE = 16

#Pad with a number that is the length of the padding that is added
def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + chr(length)*length

def unpad(data):
    return data[:-ord(data[-1])]

def _getPassPhrase(bcrypt, salt, password):
  return __INT__get32BytesFromSalt(bcrypt.hashpw(password, salt))

# Based on https://stackoverflow.com/questions/11567290/cryptojs-and-pycrypto-working-together
def encryptPassword(bcrypt, plainText, safeSaltString, safePasswordString):
  if (type(safeSaltString)) is not str:
    raise Exception("Not a safe salt string - " + (type(safeSaltString)))

  salt = getSaltFromSafeSaltString(safeSaltString)
  password = getPasswordFromSafePasswordString(safePasswordString)
  passphrase = _getPassPhrase(bcrypt, salt, password)

  ##IV = OSRNG.posix.new().read(BLOCK_SIZE)
  IV = Crypto.Random.get_random_bytes(BLOCK_SIZE)

  aes = AES.new(passphrase, AES.MODE_CBC, IV)

  cipherText = aes.encrypt(pad(plainText).encode("utf-8"))

  return b64encode(IV).decode("utf-8") + ":" + b64encode(cipherText).decode("utf-8")
#  return (b64encode(iv).decode("utf-8"), b64encode(ciphertext).decode("utf-8"))

def decryptPassword(bcrypt, cypherText, safeSaltString, safePasswordString):
  if (type(safeSaltString)) is not str:
    raise Exception("Not a safe salt string - " + (type(safeSaltString)))

  salt = getSaltFromSafeSaltString(safeSaltString)
  password = getPasswordFromSafePasswordString(safePasswordString)
  passphrase = _getPassPhrase(bcrypt, salt, password)

  [iv, cypherTextSep] = cypherText.split(":")

  #iv and cypherText are base64 encoded strings
  ivi=b64decode(iv)
  cypherTexti=b64decode(cypherTextSep)

  ##passphrase="12345678901234567890123456789012"

  #print("Decrypting Password:")
  #print("ivi", ivi)
  #print("cypherTexti", cypherTexti)
  #print("passphrase", passphrase)

  aes = AES.new(passphrase, AES.MODE_CBC, ivi)
  try:
    unpaddedPlainText = unpad(aes.decrypt(cypherTexti).decode())
  except:
    raise WrongPasswordException()

  #print("Res:", unpaddedPlainText)

  return unpaddedPlainText

# Pass in appObj.bcrypt

def getSalt(bcrypt):
  return bcrypt.gensalt()
def getSafeSaltString(bcrypt, salt=None):
  if salt is None:
    return str(b64encode(getSalt(bcrypt)), 'utf-8')
  return str(b64encode(salt), 'utf-8')

def getSaltFromSafeSaltString(safeSaltString):
  return b64decode(safeSaltString)

def getSafePasswordString(password):
  return b64encode(password.encode('utf-8'))

def getPasswordFromSafePasswordString(safePasswordString):
  return b64decode(safePasswordString)

