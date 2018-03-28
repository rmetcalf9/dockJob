
Feature('InvalidJobShowsError');

Scenario('test something', (I, dashboardPage) => {
  I.amOnPage('/#/jobs/abc');
  I.waitForElement(dashboardPage.dashboardWindow, 5); // Wait for 5 seconds
  I.see('Job query failed - Invalid Job Identifier')

});
