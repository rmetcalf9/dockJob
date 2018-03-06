
module.exports = function() {
  return {
    selectors: {
      toolbar: '#q-app > div > header > div',
      menu: {
        jobs: '#q-app > div > div.q-drawer-container > aside > div > div:nth-child(3)',
      },
      dashboard: '#q-app > div > div.q-layout-page-container.q-layout-transition > div',
      createJobForm: {
        jobName: 'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > div:nth-child(1) > div > div.q-field-content.col-xs-12.col-sm > div.q-if.row.no-wrap.items-end.relative-position.q-input.q-if-error.text-negative > div > input',
        command: 'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > div:nth-child(2) > div > div.q-field-content.col-xs-12.col-sm > div.q-if.row.no-wrap.items-end.relative-position.q-input.q-if-error.text-negative > div > div > textarea.col.q-input-target.q-input-area',
        enabled: 'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > div:nth-child(3) > div > div.q-field-content.col-xs-12.col-sm > div.q-option.cursor-pointer.no-outline.row.inline.no-wrap.items-center.q-toggle.q-focusable.q-touch > div > div.q-toggle-base'
      }
    }
  }
}
