// Created to hold global functions that are required in mutiple places

function getPostCompletionJobTypeList () {
  var t = [{
    id: 'StateChangeSuccess',
    text: 'State change Success'
  }, {
    id: 'StateChangeFail',
    text: 'State change Fail'
  }, {
    id: 'StateChangeUnknown',
    text: 'State change Unknown'
  }, {
    id: 'AfterSuccess',
    text: 'After Success'
  }, {
    id: 'AfterFail',
    text: 'After Fail'
  }, {
    id: 'AfterUnknown',
    text: 'After Unknown'
  }]
  return t.map(function (x) {
    return {
      id: x.id,
      text: x.text,
      guidFieldName: x.id + 'JobGUID',
      nameFieldName: x.id + 'JobNAME'
    }
  })
}

export default {
  getPostCompletionJobTypeList
}
