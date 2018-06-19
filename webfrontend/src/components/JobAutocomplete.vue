<template>
  <div>
    <q-input
      v-model="jobName"
      type="text"
      :float-label="floatlabel"
      :error-label="errorlabel"
      :error="invalid"
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
    }
  },
  methods: {
    search (terms, done) {
      // make an AJAX call
      // then call done(Array results)
      var TTT = this
      var callback = {
        ok: function (response) {
          // done(response.data.result.map(function (ite) {
          //  return {
          //    value: ite.guid,
          //    label: ite.name
          //  }
          //}))
          done([{value: 'a', label: 'b'}])
        },
        error: function (error) {
          console.log('JobAutoComplete Error')
          console.log(error)
          done([])
        }
      }
      var queryString = restcallutils.buildQueryString('jobs/', [])
      // console.log(queryString)
      globalStore.getters.apiFN('GET', queryString, undefined, callback)
    },
    selected (item) {
      console.log('TODO Item selected ' + item)
    },
    setValue (jobNAME) {
      this.$emit('modelupdate', {guid: 'TODO work out guid for job ' + jobNAME, name: jobNAME})
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
      return false
    }
  }
}

</script>
