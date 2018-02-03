
Feature('CanViewDashboard');

Scenario('test something', (I) => {
  I.amOnPage('/');
  I.seeCurrentUrlEquals('/#/dashboard');
  within('DIV.layout DIV.layout-page-container .layout-page', () => {
    I.see('Dashboard');
  });
});
