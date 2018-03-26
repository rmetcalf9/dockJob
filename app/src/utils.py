import pytz
import dateutil.parser



def from_iso8601(when=None, tz=pytz.timezone("UTC")):
  _when = dateutil.parser.parse(when)
  if not _when.tzinfo:
    _when = tz.localize(_when)
  if (str(_when.tzinfo) != 'tzutc()'):
    raise Exception('Error - Only conversion of utc times from iso8601 is supported')
  return _when


