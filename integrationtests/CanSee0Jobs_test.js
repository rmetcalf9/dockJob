
Feature('CanSee0Jobs');

Scenario('I can see 0 Jobs', (I) => {
  I.amOnPage('/');
  within('DIV.layout DIV.layout-page-container .layout-page', () => {
    I.see('Total jobs setup: 0');
  });

});
