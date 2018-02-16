
Feature('CanViewDashboard');

Scenario('I can view the dashboard', (I) => {
  I.amOnPage('/');
  I.waitForElement('DIV.layout DIV.layout-page-container .layout-page', 3000); // Wait for 3 seconds
  I.seeCurrentUrlEquals('/#/dashboard');
  within('DIV.layout > header > div.q-toolbar', () => {
    I.see('Dashboard');
  });
  within('DIV.layout > DIV.layout-page-container > .layout-page', () => {
    I.see('Server Info');
  });
});

//
