import { date } from 'quasar'

function timeString (iso8601String) {
  if (typeof (iso8601String) === 'undefined') {
    return undefined
  }
  if (iso8601String === null) {
    return null
  }
  var d = Date.parse(iso8601String)
  // During testing this displayed in my local timezone
  // decided to allow the quasar/browser formatting to determine the timezone
  // and not make it user selectable.
  return date.formatDate(d, 'YYYY-MM-DD HH:mm:ss Z')
}

export default {
  timeString
}
