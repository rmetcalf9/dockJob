
Feature('CanSee0Jobs');

Scenario('I can see 0 Jobs', (I) => {
  I.amOnPage('/');
  I.waitForElement('DIV.layout DIV.layout-page-container .layout-page', 3000); // Wait for 3 seconds
  within('DIV.layout DIV.layout-page-container .layout-page', () => {
    I.see('Total jobs setup: 0');
  });

});
