vars = require('./vars')

Feature('CanSee0Jobs');

Scenario('I can see 0 Jobs', (I) => {
  I.amOnPage('/');
  I.waitForElement(vars().selectors.dashboard, 3000); // Wait for 3 seconds
  within('#q-app > div > div.q-layout-page-container.q-layout-transition > div', () => {
    I.see('Total jobs setup: 0');
  });

});
