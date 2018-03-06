vars = require('./vars')

Feature('CanCreateOneJob');

Scenario('I can create a one job', (I) => {
  var jobName = 'testJob'
  var t = ''

  I.amOnPage('/');
  I.waitForElement(vars().selectors.dashboard, 3); // Wait for 3 seconds

  //within('DIV.layout > HEADER', () => {
  //  I.click('menu');
  //});

  //Click Jobs
  I.executeScript("var elements = document.querySelector('" + vars().selectors.menu.jobs + "');elements.click();");

  I.click('Create Job');
  I.fillField(vars().selectors.createJobForm.jobName,jobName);
  I.fillField(vars().selectors.createJobForm.command,'ls -la');
  
  // This will already be checked I.checkOption(vars().selectors.createJobForm.enabled);
  
  // Don't change Repetition Interval - use defailt

  //var t = 'body > div.modal.fullscreen.row.flex-center > div > div > div.q-modal-layout-content.col.scroll > div > div.q-field.row.no-wrap.items-start.q-field-responsive.q-field-floating > div > div.q-field-content.col-xs-12.col-sm > div.q-if.row.no-wrap.items-end.relative-position.q-select.q-if-focusable.text-primary > div > div'

  //I.executeScript("var elements2 = document.querySelector('" + t + "');elements2.click();");

  t = 'body > div.q-popover.scroll.column.no-wrap.animate-popup-down > div > div.q-item.q-item-division.relative-position.q-item-link.cursor-pointer.q-select-highlight > div > div'
  I.executeScript("var elements3 = document.querySelector('" + t + "');elements3.click();");

  //I.uncheckOption('Daily');
  //I.uncheckOption('Monthly');
  //I.seeElement('Minute[disabled]');
  //I.seeElement('hour[disabled]');
  //I.seeElement('dayOfMonth[disabled]');
  //I.seeElement('timezone[disabled]');
  I.click('Ok');

  //Now query back job and make sure it is shown
  I.fillField('Filter',jobName);
  I.seeNumberOfElements('Search Results',1);

  //Not sure how to select correct job to delete yet
  I.click('Delete Job')
  I.click('Ok')

  //Now query back job and make sure it has gone
  I.fillField('Filter',jobName);
  I.seeNumberOfElements('Search Results',1);

});

