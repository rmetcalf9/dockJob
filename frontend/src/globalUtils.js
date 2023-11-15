// Created to hold global functions that are required in mutiple places

function getPostCompletionJobTypeList () {
  var t = [{
    id: 'StateChangeSuccess',
    text: 'State change Success',
    createDialogLabel: 'Job to call when State changes to Success'
  }, {
    id: 'StateChangeFail',
    text: 'State change Fail',
    createDialogLabel: 'Job to call when State changes to Fail'
  }, {
    id: 'StateChangeUnknown',
    text: 'State change Unknown',
    createDialogLabel: 'Job to call when State changes to Unknown'
  }, {
    id: 'AfterSuccess',
    text: 'After Success',
    createDialogLabel: 'Job to call after sucessful completion'
  }, {
    id: 'AfterFail',
    text: 'After Fail',
    createDialogLabel: 'Job to call after fail completion'
  }, {
    id: 'AfterUnknown',
    text: 'After Unknown',
    createDialogLabel: 'Job to call after unknown completion'
  }]
  return t.map(function (x) {
    return {
      id: x.id,
      text: x.text,
      createDialogLabel: x.createDialogLabel,
      guidFieldName: x.id + 'JobGUID',
      nameFieldName: x.id + 'JobNAME',
      jobModelFieldName: x.id + 'JobModel'
    }
  })
}

export default {
  getPostCompletionJobTypeList
}
