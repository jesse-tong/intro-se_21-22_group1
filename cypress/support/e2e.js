// ***********************************************************
// This example support/e2e.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

// Import commands.js using ES2015 syntax:
import './commands'

// Alternatively you can use CommonJS syntax:
// require('./commands')

beforeEach(()=> {
    Cypress.session.clearAllSavedSessions();
    cy.session('login', ()=>{
        cy.once('uncaught:exception', () => false);
        cy.visit('http://localhost:5000/login');
        cy.get('#emailInput').type('jesse-tong3@gmail.com');
        cy.get('#passwordInput').type('Password2');
        cy.get('#rememberMe').check();
        cy.get('#loginSubmitButton').click();
        cy.wait(200);
    }, { cacheAcrossSpecs: true })
});

