import { faker } from '@faker-js/faker';

describe('Login with correct login information', () => {
  it('Login with correct login information', () => {
    cy.visit('http://localhost:5000/login');
    cy.get('#emailInput').type('jesse-tong3@gmail.com');
    cy.get('#passwordInput').type('Password2');
    cy.get('#loginSubmitButton').click();
    cy.get('.notification-title').should('contain', 'Login successfully!')
    cy.get('.navbar-toggler-icon').click()
    cy.contains('Log out').click()
    cy.get('.notification-title').should('contain', 'Logout successfully!')
  })
})

describe('Login with incorrect login information', () => {
  it('Login with incorrect login information', () => {
    cy.visit('http://localhost:5000/login');
    cy.get('#emailInput').type('jesse-tong3@gmail.com');
    cy.get('#passwordInput').type('incorrectpassword');
    cy.get('#loginSubmitButton').click();
    cy.get('.notification-title').should('contain', 'Login error')
    cy.get('.notification-content').should('contain', 'Login with error: Invalid authentication')
    
  })
})

describe('Login with invalid email format', () => {
  it('Login with incorrect login information', () => {
    cy.visit('http://localhost:5000/login');
    cy.get('#emailInput').type(faker.internet.userName());
    cy.get('#passwordInput').type('incorrectpassword');
    cy.get('#loginSubmitButton').click();
    cy.get('.notification-title').should('contain', 'Login error')
    cy.get('.notification-content').should('contain', 'Login with error: Invalid authentication')
    
  })
})

describe('Register with invalid email format', () => {
  it('Login with incorrect login information', () => {
    cy.visit('http://localhost:5000/register');
    cy.get('#emailInput').type(faker.internet.userName());
    cy.get('#usernameInput').type(faker.internet.userName());
    cy.get('#passwordInput').type('SomeP@ssword1');
    cy.get('#passwordRepeatInput').type('SomeP@ssword1')
    cy.get('#registerButton').click();
    cy.get('.notification-title').should('contain', 'Register')
    cy.get('.notification-content').should('contain', 'Register with error: Invalid email')
    
  })
})

describe('Register with mismatch password repeat', () => {
  it('Login with incorrect login information', () => {
    cy.visit('http://localhost:5000/register');
    cy.get('#emailInput').type(faker.internet.email());
    cy.get('#usernameInput').type(faker.internet.userName());
    cy.get('#passwordInput').type('SomeP@ssword1');
    cy.get('#passwordRepeatInput').type(faker.internet.password())
    cy.get('#registerButton').click();
    cy.get('.notification-title').should('contain', 'Incorrect reentering password!')
    cy.get('.notification-content').should('contain', 'Register with error: Incorrect reentering password!')
    
  })
})