
Feature('CanCreateOneJob');

Scenario('I can create a one job', (I) => {
  var jobName = 'testJob'

  I.amOnPage('/');
  I.waitForElement('DIV.layout DIV.layout-page-container .layout-page', 3000); // Wait for 3 seconds

  //within('DIV.layout > HEADER', () => {
  //  I.click('menu');
  //});

  //Click Jobs
  I.executeScript("var elements = document.querySelector('#q-app > div > aside > div.q-scrollarea.relative-position > div.scroll.relative-position.overflow-hidden.full-height.full-width.q-touch.q-touch-x > div > div:nth-child(3) > div.q-item-main.q-item-section > div');elements.click();");

  I.click('Create Job');
  I.fillField('Job Name',jobName);
  I.fillField('Command','ls -la');
  I.checkOption('Enabled');
  I.uncheckOption('Hourly');
  I.uncheckOption('Daily');
  I.uncheckOption('Monthly');
  I.seeElement('Minute[disabled]');
  I.seeElement('hour[disabled]');
  I.seeElement('dayOfMonth[disabled]');
  I.seeElement('timezone[disabled]');
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
