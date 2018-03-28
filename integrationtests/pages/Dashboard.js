
'use strict';

let I;

module.exports = {

  _init() {
    I = require('../steps_file.js')();
  },

  // insert your locators and methods here
  dashboardWindow: {css: '#q-app > div > div.q-layout-page-container.q-layout-transition > main'}

}
