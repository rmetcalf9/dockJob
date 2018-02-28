
Feature('CanCreateOneJob');

Scenario('I can create a one job', (I) => {
  var jobName = 'testJob'

  I.amOnPage('/');
  I.waitForElement('DIV.layout DIV.layout-page-container .layout-page', 3000); // Wait for 3 seconds
  within('DIV.layout > HEADER', () => {
    I.click('menu');
  });
  within('DIV.layout > ASIDE.layout-aside', () => {
    I.click('Jobs');
  });
  I.waitForElement('Create Job', 3000); // Wait for 3 seconds
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
