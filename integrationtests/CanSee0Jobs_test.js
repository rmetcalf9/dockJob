Feature('CanSee0Jobs');

Scenario('I can see 0 Jobs', (I, dashboardPage) => {
  I.amOnPage('/');
  I.waitForElement(dashboardPage.dashboardWindow, 5); // Wait for 5 seconds
  within(dashboardPage.dashboardWindow, () => {
    I.see('Total jobs setup: 0');
  });

});
