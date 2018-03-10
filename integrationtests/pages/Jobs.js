
'use strict';

let I;

module.exports = {

  _init() {
    I = require('../steps_file.js')();
  },

  // insert your locators and methods here
  CreateJobButton: {css: '#q-app > div > div.q-layout-page-container.q-layout-transition > div > div.q-table-container > div.q-table-top.relative-position.row.items-center > div:nth-child(1) > button'},
  CreateJobForm: {
    jobName: {css: 'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > div:nth-child(1) > div > div.q-field-content.col-xs-12.col-sm > div.q-if.row.no-wrap.items-end.relative-position.q-input.q-if-error.text-negative > div > input'},
    command: {css: 'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > div:nth-child(2) > div > div.q-field-content.col-xs-12.col-sm > div.q-if.row.no-wrap.items-end.relative-position.q-input.q-if-error.text-negative > div > div > textarea.col.q-input-target.q-input-area'},
    createButton: {css: 'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > button.q-btn.inline.relative-position.q-btn-item.non-selectable.q-btn-rectangle.q-focusable.q-hoverable.bg-primary.text-white > div.q-focus-helper'},
    selectDailyMode() {
      I.click({css:'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > div.q-field.row.no-wrap.items-start.q-field-responsive.q-field-floating > div > div.q-field-content.col-xs-12.col-sm > div.q-if.row.no-wrap.items-end.relative-position.q-select.q-if-focusable.text-primary > div'})
      I.wait(1)
      I.click({css:'body > div.q-popover.scroll.column.no-wrap.animate-popup-down > div > div.active.q-item.q-item-division.relative-position.q-item-link.cursor-pointer.q-select-highlight > div > div'})
    },
    selectMonday() {
      I.click({css:'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > div.q-field.row.no-wrap.items-start.q-field-responsive.q-field-floating > div > div.q-field-content.col-xs-12.col-sm > div.q-if.row.no-wrap.items-end.relative-position.q-select.q-if-has-label.q-if-error.q-if-focusable.text-negative > div'})
      I.wait(1)
      I.click({css:'body > div.q-popover.scroll.column.no-wrap.animate-popup-up > div > div.q-item.q-item-division.relative-position.q-item-link.cursor-pointer.q-select-highlight > div.q-item-side.q-item-section.q-item-side-right > div > div'})
      I.wait(1)
      I.click({css:'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > div.q-field.row.no-wrap.items-start.q-field-responsive.q-field-floating > div > div.q-field-label.q-field-margin.col-xs-12.col-sm-3'})
      I.wait(1)
    }
  }
}
