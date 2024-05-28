import { faker } from '@faker-js/faker';

const isbn = faker.commerce.isbn();
const bookStock = faker.number.int({ min: 1, max: 10});
const publishYear = faker.number.int({min: 1, max: 2025});
const bookTitle = faker.commerce.productName();
const author = faker.person.fullName();
const genre = faker.music.genre();
const language = 'English';
const description = faker.commerce.productDescription();


const login = () => {
    
}

describe('Add book test in general', () => {
    
    it('Add book test', () => {
        cy.visit('http://localhost:5000/admin/manage-books');
        cy.get('#editBookISBN').type(isbn)
        cy.get('#editBookStock').type(bookStock);
        cy.get('#editPublishYear').type(publishYear);
        cy.get('#editBookTitle').type(bookTitle);

        //Test add author button
        cy.get('#editAuthor').type(author);
        cy.get('#addAuthorButton').click(); 
        cy.get('[data-testid="authorBadge"]').should('have.length', 1);
        cy.get('[data-testid="authorBadge"]').contains(author);
        
        //Test clear all authors button
        cy.get('#clearAllAuthorButton').click();
        cy.get('[data-testid="authorBadge"]').should('have.length', 0);

        cy.get('#addAuthorButton').click(); 

        //Test Add genre button
        cy.get('#editGenre').type(genre);
        cy.get('#addGenreButton').click();
        cy.get('[data-testid="genreBadge"]').should('have.length', 1);
        cy.get('[data-testid="genreBadge"]').contains(genre);

        //Test clear all authors button
        cy.get('#clearAllGenresButton').click();
        cy.get('[data-testid="genreBadge"]').should('have.length', 0);


        cy.get('#addGenreButton').click();

        //Test Add language button
        cy.get('#editLanguage').type(genre);
        cy.get('#addLanguageButton').click();
        cy.get('[data-testid="languageBadge"]').should('have.length', 1);
        cy.get('[data-testid="languageBadge"]').contains(genre);

        //Test clear all authors button
        cy.get('#clearAllLanguagesButton').click();
        cy.get('[data-testid="languageBadge"]').should('have.length', 0);

        cy.get('#addLanguageButton').click();

        //Add description
        cy.get('#editDescription').type(description);
        cy.get('#addBookButton').click()

        cy.get('.notification-title').should('contain', 'Add book successfully')
        cy.get('.notification-content').should('contain', 'Add book successfully')
  })
})