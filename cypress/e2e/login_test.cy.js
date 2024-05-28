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