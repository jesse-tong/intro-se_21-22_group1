import {By, Builder, Browser} from 'selenium-webdriver';
import assert from 'assert';
import { loginTestWithCorrectPassword } from './login_test.js';

(async function loginTests() {
    let driver;
    
    try {
      driver = await new Builder().forBrowser(Browser.FIREFOX).build();
      await driver.get('http://localhost:5173');
      let title = await driver.getTitle();
      assert.equal("EasyLib Library Management Software", title);
      await driver.manage().setTimeouts({implicit: 500});
      await loginTestWithCorrectPassword(driver, 'jesse-tong3@gmail.com', 'Password1');

      
      closeButton = await driver.findElement(By.className('btn-close'));
      await closeButton.click();
      
      
    } catch (e) {
      console.log(e)
    } finally {
      await driver.quit();
    }
  }())

