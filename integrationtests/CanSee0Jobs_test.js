
Feature('CanSee0Jobs');

Scenario('test something', (I) => {
  I.amOnPage('/');
  within('DIV.layout DIV.layout-page-container .layout-page', () => {
    I.see('Total jobs setup: 0');
  });

});
