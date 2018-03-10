
'use strict';

let I;

module.exports = {

  _init() {
    I = require('../steps_file.js')();
  },

  // insert your locators and methods here
  JobLink: {css: '#q-app > div > div.q-drawer-container > aside > div > div:nth-child(3) > div.q-item-main.q-item-section > div'},
  Toolbar: {css: '#q-app > div > header > div'},

}
