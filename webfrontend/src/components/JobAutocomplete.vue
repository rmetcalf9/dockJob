<template>
  <div>
    <q-input
      v-model="jobName"
      type="text"
      :float-label="floatlabel"
      :error-label="errorlabel"
      :error="invalid"
      :clearable="true"
    >
      <q-autocomplete
        @search="search"
        :min-characters="0"
        @selected="selected"
      />
    </q-input>
  </div>
</template>

<script>
import globalStore from '../store/globalStore'
import restcallutils from '../restcallutils'

export default {
  props: [
    'model',
    'floatlabel',
    'errorlabel'
  ],
  data: function () {
    return {
      queriedValues: []
    }
  },
  watch: {
    model: function (newVal, oldVal) {
      if (typeof (newVal.guid) !== 'undefined') {
        if (newVal.guid !== '') {
          this.queriedValues[newVal.name] = newVal.guid
        }
      }
    }
  },
  methods: {
    search (terms, done) {
      // make an AJAX call
      // then call done(Array results)
      var TTT = this
      var callback = {
        ok: function (response) {
          // TTT.queriedValues = [] Not resetting. Will build up values in case user types previously searched for job name
          done(response.data.result.map(function (ite) {
            TTT.queriedValues[ite.name] = ite.guid
            return {
              value: ite.name,
              label: ite.name
            }
          }))
          // done([{value: 'a', label: 'b'}])
        },
        error: function (error) {
          console.log('JobAutoComplete Error')
          console.log(error)
          done([])
        }
      }
      var queryParams = []
      queryParams['query'] = terms
      var queryString = restcallutils.buildQueryString('jobs/', queryParams)
      // console.log(queryString)
      globalStore.getters.apiFN('GET', queryString, undefined, callback)
    },
    selected (item) {
      this.jobName = item.label
    },
    setValue (jobNAME) {
      if (typeof (this.queriedValues[jobNAME]) === 'undefined') {
        this.$emit('modelupdate', {guid: '', name: jobNAME})
      } else {
        this.$emit('modelupdate', {guid: this.queriedValues[jobNAME], name: jobNAME})
      }
    }
  },
  computed: {
    jobName: {
      get () {
        return this.model.name
      },
      set (val) {
        this.setValue(val)
      }
    },
    invalid () {
      // console.log('inv')
      // console.log(this.model.guid)
      if (typeof (this.model.name) !== 'undefined') {
        if (this.model.name !== '') {
          if (typeof (this.model.guid) === 'undefined') {
            return true
          }
          if (this.model.guid === '') {
            return true
          }
        }
      }
      return false
    }
  }
}

</script>
