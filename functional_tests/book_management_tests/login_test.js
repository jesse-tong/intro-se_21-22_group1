import {By, Builder, Browser} from 'selenium-webdriver';
import assert from 'assert';

async function testInputLogin(driver, email, password){
    let sidebarToggler = await driver.findElement(By.className('navbar-toggler-icon'));
    await sidebarToggler.click();
    let loginLink = await driver.findElement(By.linkText('Log in'));
    await loginLink.click();
    //click on close button on sidebar
    let closeButton = await driver.findElement(By.className('btn-close'));
    await closeButton.click();
    
    //Enter email to login
    let emailInput = await driver.findElement(By.id('emailInput'));
    await emailInput.sendKeys(email);
    //enter password
    let passwordInput = await driver.findElement(By.id('passwordInput'));
    await passwordInput.sendKeys(password);
    
    let loginButton = await driver.findElement(By.id('loginSubmitButton'));
    await loginButton.click();
}

async function loginTestWithCorrectPassword(driver, email, password){
    await testInputLogin(driver, email, password)
    let notificationTitle = await driver.findElement(By.className('notification-title'));
    let notificationTitleText = await notificationTitle.getText();
    assert.equal("Login successfully!", notificationTitleText);

    let notificationContent = await driver.findElement(By.className('notification-content'));
    let notificationContentText = await notificationContent.getText();
    
    assert.equal("Login successfully!", notificationContentText);
}

async function loginTestWithIncorrectPassword(driver, email, password){
    await testInputLogin(driver, email, password);
    let notificationTitle = await driver.findElement(By.xpath("(//div[@class='notification-title'])[2]"));
    let notificationTitleText = await notificationTitle.getText();
    console.log(notificationTitleText);
    assert.equal("Login error", notificationTitleText);

    let notificationContent = await driver.findElement(By.xpath("(//div[@class='notification-content'])[2]"));
    let notificationContentText = await notificationContent.getText();
    assert.equal("Login with error: Invalid authentication", notificationContentText);
}

async function loginTestWithoutEmail(driver, password){
  await testInputLogin(driver, '', password);
  let notificationTitle = await driver.findElement(By.xpath("(//div[@class='notification-title'])[2]"));
  let notificationTitleText = await notificationTitle.getText();
  console.log(notificationTitleText);
  assert.equal("Login error", notificationTitleText);

  let notificationContent = await driver.findElement(By.xpath("(//div[@class='notification-content'])[2]"));
  let notificationContentText = await notificationContent.getText();
  assert.equal("Login with error: Invalid authentication", notificationContentText);
}

async function loginTestWithIncorrectEmail(driver, email, password){
  await testInputLogin(driver, email, password);
    let notificationTitle = await driver.findElement(By.xpath("(//div[@class='notification-title'])[2]"));
    let notificationTitleText = await notificationTitle.getText();
    console.log(notificationTitleText);
    assert.equal("Login error", notificationTitleText);

    let notificationContent = await driver.findElement(By.xpath("(//div[@class='notification-content'])[2]"));
    let notificationContentText = await notificationContent.getText();
    assert.equal("Login with error: Invalid authentication", notificationContentText);
}

(async function loginTests() {
    let driver;
    
    try {
      driver = await new Builder().forBrowser(Browser.FIREFOX).build();
      await driver.get('http://localhost:5173');
      let title = await driver.getTitle();
      assert.equal("EasyLib Library Management Software", title);
      await driver.manage().setTimeouts({implicit: 500});
      await loginTestWithCorrectPassword(driver, 'jesse-tong3@gmail.com', 'Password1');

      await driver.get('http://localhost:5173');
      let sidebarToggler = await driver.findElement(By.className('navbar-toggler-icon'));
      await sidebarToggler.click();
      let loginLink = await driver.findElement(By.linkText('Log out'));
      await loginLink.click();
      //click on close button on sidebar
      let closeButton = await driver.findElement(By.className('btn-close'));
      await closeButton.click();
      await loginTestWithIncorrectPassword(driver, 'jesse-tong3@gmail.com', 'Incorrectpassword');

      await driver.get('http://localhost:5173');
      sidebarToggler = await driver.findElement(By.className('navbar-toggler-icon'));
      await sidebarToggler.click();
      loginLink = await driver.findElement(By.linkText('Log in'));
      await loginLink.click();
      //click on close button on sidebar
      closeButton = await driver.findElement(By.className('btn-close'));
      await closeButton.click();
      await loginTestWithoutEmail(driver, 'Password1');

      await driver.get('http://localhost:5173');
      sidebarToggler = await driver.findElement(By.className('navbar-toggler-icon'));
      await sidebarToggler.click();
      loginLink = await driver.findElement(By.linkText('Log in'));
      await loginLink.click();
      //click on close button on sidebar
      closeButton = await driver.findElement(By.className('btn-close'));
      await closeButton.click();
      await loginTestWithIncorrectEmail(driver, 'falseemail@gmail.com', 'Password1');
      
    } catch (e) {
      console.log(e)
    } finally {
      await driver.quit();
    }
  }())

