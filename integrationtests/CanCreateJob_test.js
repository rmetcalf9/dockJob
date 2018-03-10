Feature('CanCreateOneJob');

Scenario('I can create one job', (I, dashboardPage, indexPage, jobsPage) => {
  var jobName = 'testJob'


  I.amOnPage('/');
  I.waitForElement(dashboardPage.dashboardWindow, 5); // Wait for 5 seconds
  I.click(indexPage.JobLink)
  I.click(jobsPage.CreateJobButton)

  I.fillField(jobsPage.CreateJobForm.jobName,jobName);
  I.fillField(jobsPage.CreateJobForm.command,'ls -la');

  jobsPage.CreateJobForm.selectDailyMode()
  //jobsPage.CreateJobForm.selectMonday()

  //I.click(jobsPage.CreateJobForm.createButton);
  //Not working


  //I.uncheckOption('Daily');
  //I.uncheckOption('Monthly');
  //I.seeElement('Minute[disabled]');
  //I.seeElement('hour[disabled]');
  //I.seeElement('dayOfMonth[disabled]');
  //I.seeElement('timezone[disabled]');
  //I.click('Ok');

  //Now query back job and make sure it is shown
  //I.fillField('Filter',jobName);
  //I.seeNumberOfElements('Search Results',1);

  //Not sure how to select correct job to delete yet
  //I.click('Delete Job')
  //I.click('Ok')

  //Now query back job and make sure it has gone
  //I.fillField('Filter',jobName);
  //I.seeNumberOfElements('Search Results',1);

});

