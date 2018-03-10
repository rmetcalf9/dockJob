Feature('CanViewDashboard');

Scenario('I can view the dashboard', (I, dashboardPage, indexPage) => {
  I.amOnPage('/');
  I.waitForElement(dashboardPage.dashboardWindow, 5); // Wait for 5 seconds
  I.seeCurrentUrlEquals('/#/dashboard');
  within(indexPage.Toolbar, () => {
    I.see('Dashboard');
  });
  within(dashboardPage.dashboardWindow, () => {
    I.see('Server Info');
  });
});

