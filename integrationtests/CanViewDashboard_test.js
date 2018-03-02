vars = require('./vars')

Feature('CanViewDashboard');

Scenario('I can view the dashboard', (I) => {
  I.amOnPage('/');
  I.waitForElement(vars().selectors.dashboard, 3000); // Wait for 3 seconds
  I.seeCurrentUrlEquals('/#/dashboard');
  within(vars().selectors.toolbar, () => {
    I.see('Dashboard');
  });
  within(vars().selectors.dashboard, () => {
    I.see('Server Info');
  });
});

