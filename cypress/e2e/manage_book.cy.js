import { faker } from '@faker-js/faker';

const isbn = faker.commerce.isbn();
const bookStock = faker.number.int({ min: 1, max: 10});
const publishYear = faker.number.int({min: 1800, max: 2025});
const bookTitle = faker.commerce.productName();
var author = faker.person.fullName();
var genre = faker.music.genre();
var language = 'English';
var description = faker.commerce.productDescription();
var FrankensteinTitle = "Frankenstein";
var FrankensteinISBN = ""

const login = () => {
    
}

describe('Manage book tests', () => {
    
    it('Add book test', () => {
        cy.visit('http://localhost:5000/admin/manage-books');
        cy.get('#editBookISBN').type(isbn)
        cy.get('#editBookStock').clear();
        cy.get('#editBookStock').type(bookStock);
        cy.get('#editPublishYear').clear();
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
        cy.get('#editLanguage').type(language);
        cy.get('#addLanguageButton').click();
        cy.get('[data-testid="languageBadge"]').should('have.length', 1);
        cy.get('[data-testid="languageBadge"]').contains(language);

        //Test clear all authors button
        cy.get('#clearAllLanguagesButton').click();
        cy.get('[data-testid="languageBadge"]').should('have.length', 0);

        cy.get('#addLanguageButton').click();

        //Add description
        cy.get('#editDescription').type(description);
        cy.get('#addBookButton').click()

        cy.get('.notification-title').should('contain', 'Add book successfully')
        cy.get('.notification-content').should('contain', 'Add book successfully')
  });

  it('Search and edit book test with "not updating language" checkbox checked', () => {

    cy.once('uncaught:exception', () => false);
    cy.visit('http://localhost:5000/admin/manage-books');
    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();

    //Check if the input information are correctly input
    cy.get('[data-testid="bookTableRow"]').should('have.length', 1);
    cy.get('[data-testid="bookTableRow"] td:nth-child(2)').contains(bookTitle);
    cy.get('[data-testid="bookTableRow"] td:nth-child(3)').contains(publishYear);
    cy.get('[data-testid="bookTableRow"] td:nth-child(4)').contains(isbn);
    cy.get('[data-testid="bookTableRow"] td:nth-child(5)').contains(bookStock);
    cy.get('[data-testid="bookTableRow"] td:nth-child(6) button').contains('Edit').click();
    
    //Check if the author, genre and language are correct
    cy.get('[data-testid="authorBadge"]').should('have.length', 1);
    cy.get('[data-testid="authorBadge"]').contains(author);
    cy.get('[data-testid="genreBadge"]').should('have.length', 1);
    cy.get('[data-testid="genreBadge"]').contains(genre);
    cy.get('[data-testid="languageBadge"]').should('have.length', 1);
    cy.get('[data-testid="languageBadge"]').contains(language);

    //Edit to the new author
    cy.get('#clearAllAuthorButton').click();
    author = faker.person.fullName();
    cy.get('#editAuthor').type(author);
    cy.get('#addAuthorButton').click();

    //Edit to the new genre
    cy.get('#clearAllGenresButton').click();
    genre = faker.music.genre()
    cy.get('#editGenre').type(genre);
    cy.get('#addGenreButton').click();
    
    //Testing 'not updating language' checkbox
    cy.get('#editLanguage').type('Test Language');
    cy.get('#addLanguageButton').click();
    cy.get('#notUpdatingLanguages').check();

    description = faker.commerce.productDescription();
    cy.get('#editDescription').clear();
    cy.get('#editDescription').type(description);
    cy.get('#editBookButton').click();

    cy.get('.notification-title').should('contain', 'Edit book details successfully')
    cy.get('.notification-content').should('contain', 'Edit book successfully');

    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();

    cy.get('[data-testid="bookTableRow"] td:nth-child(6) button').contains('Edit').click();
    
    //Check if the author, genre and language are correct
    cy.get('[data-testid="authorBadge"]').should('have.length', 1);
    cy.get('[data-testid="authorBadge"]').contains(author);
    cy.get('[data-testid="genreBadge"]').should('have.length', 1);
    cy.get('[data-testid="genreBadge"]').contains(genre);
    cy.get('[data-testid="languageBadge"]').should('have.length', 1);
    cy.get('[data-testid="languageBadge"]').contains(language);
  });

  it('Search and edit book test with "not updating genres" checkbox checked', () => {

    cy.once('uncaught:exception', () => false);
    cy.visit('http://localhost:5000/admin/manage-books');
    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();

    //Check if the input information are correctly input
    cy.get('[data-testid="bookTableRow"]').should('have.length', 1);
    cy.get('[data-testid="bookTableRow"] td:nth-child(2)').contains(bookTitle);
    cy.get('[data-testid="bookTableRow"] td:nth-child(4)').contains(isbn);
    cy.get('[data-testid="bookTableRow"] td:nth-child(5)').contains(bookStock);
    cy.get('[data-testid="bookTableRow"] td:nth-child(6) button').contains('Edit').click();
    
    //Check if the author, genre and language are correct
    cy.get('[data-testid="authorBadge"]').should('have.length', 1);
    cy.get('[data-testid="authorBadge"]').contains(author);
    cy.get('[data-testid="genreBadge"]').should('have.length', 1);
    cy.get('[data-testid="genreBadge"]').contains(genre);
    cy.get('[data-testid="languageBadge"]').should('have.length', 1);
    cy.get('[data-testid="languageBadge"]').contains(language);

    //Edit to the new author
    cy.get('#clearAllAuthorButton').click();
    author = faker.person.fullName();
    cy.get('#editAuthor').type(author);
    cy.get('#addAuthorButton').click();

    //Test 'Not updating genres' button
    cy.get('#clearAllGenresButton').click();
    cy.get('#editGenre').type('Test genre');
    cy.get('#addGenreButton').click();
    cy.get('#notUpdatingGenres').check();
    
    //Edit to a new language
    language = 'French';
    cy.get('#clearAllLanguagesButton').click();
    cy.get('#editLanguage').clear;
    cy.get('#editLanguage').type(language);
    cy.get('#addLanguageButton').click();

    description = faker.commerce.productDescription();
    cy.get('#editDescription').clear();
    cy.get('#editDescription').type(description);
    cy.get('#editBookButton').click();

    cy.get('.notification-title').should('contain', 'Edit book details successfully')
    cy.get('.notification-content').should('contain', 'Edit book successfully');

    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();

    cy.get('[data-testid="bookTableRow"] td:nth-child(6) button').contains('Edit').click();
    
    //Check if the author, genre and language are correct
    cy.get('[data-testid="authorBadge"]').should('have.length', 1);
    cy.get('[data-testid="authorBadge"]').contains(author);
    cy.get('[data-testid="genreBadge"]').should('have.length', 1);
    cy.get('[data-testid="genreBadge"]').contains(genre);
    cy.get('[data-testid="languageBadge"]').should('have.length', 1);
    cy.get('[data-testid="languageBadge"]').contains(language);
  });

  it('Search and edit book test with "not updating authors" checkbox checked', () => {

    cy.once('uncaught:exception', () => false);
    cy.visit('http://localhost:5000/admin/manage-books');
    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();

    //Check if the input information are correctly input
    cy.get('[data-testid="bookTableRow"]').should('have.length', 1);
    cy.get('[data-testid="bookTableRow"] td:nth-child(2)').contains(bookTitle);
    cy.get('[data-testid="bookTableRow"] td:nth-child(4)').contains(isbn);
    cy.get('[data-testid="bookTableRow"] td:nth-child(5)').contains(bookStock);
    cy.get('[data-testid="bookTableRow"] td:nth-child(6) button').contains('Edit').click();
    
    //Check if the author, genre and language are correct
    cy.get('[data-testid="authorBadge"]').should('have.length', 1);
    cy.get('[data-testid="authorBadge"]').contains(author);
    cy.get('[data-testid="genreBadge"]').should('have.length', 1);
    cy.get('[data-testid="genreBadge"]').contains(genre);
    cy.get('[data-testid="languageBadge"]').should('have.length', 1);
    cy.get('[data-testid="languageBadge"]').contains(language);

    //Edit to the new author
    cy.get('#clearAllAuthorButton').click();
    cy.get('#editAuthor').type('Test author');
    cy.get('#addAuthorButton').click();
    cy.get('#notUpdatingAuthors').click()

    //Test 'Not updating genres' button
    cy.get('#clearAllGenresButton').click();
    genre = faker.music.genre()
    cy.get('#editGenre').clear();
    cy.get('#editGenre').type(genre);
    cy.get('#addGenreButton').click();
    
    
    //Edit to a new language
    language = 'German';
    cy.get('#clearAllLanguagesButton').click();
    cy.get('#editLanguage').clear;
    cy.get('#editLanguage').type(language);
    cy.get('#addLanguageButton').click();

    description = faker.commerce.productDescription();
    cy.get('#editDescription').clear();
    cy.get('#editDescription').type(description);
    cy.get('#editBookButton').click();

    cy.get('.notification-title').should('contain', 'Edit book details successfully')
    cy.get('.notification-content').should('contain', 'Edit book successfully');

    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();

    cy.get('[data-testid="bookTableRow"] td:nth-child(6) button').contains('Edit').click();
    
    //Check if the author, genre and language are correct
    cy.get('[data-testid="authorBadge"]').should('have.length', 1);
    cy.get('[data-testid="authorBadge"]').contains(author);
    cy.get('[data-testid="genreBadge"]').should('have.length', 1);
    cy.get('[data-testid="genreBadge"]').contains(genre);
    cy.get('[data-testid="languageBadge"]').should('have.length', 1);
    cy.get('[data-testid="languageBadge"]').contains(language);
  });

  it('Search and edit book without ISBN', () => {

    cy.once('uncaught:exception', () => false);
    cy.visit('http://localhost:5000/admin/manage-books');
    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();

    //Check if the input information are correctly input
    cy.get('[data-testid="bookTableRow"]').should('have.length', 1);
    cy.get('[data-testid="bookTableRow"] td:nth-child(2)').contains(bookTitle);
    cy.get('[data-testid="bookTableRow"] td:nth-child(4)').contains(isbn);
    cy.get('[data-testid="bookTableRow"] td:nth-child(5)').contains(bookStock);
    cy.get('[data-testid="bookTableRow"] td:nth-child(6) button').contains('Edit').click();
    

    //Clear ISBN and leave it blank
    cy.get('#editBookISBN').clear();
    cy.get('#editBookButton').click();

    cy.get('.notification-title').should('contain', 'Edit book details successfully')
    cy.get('.notification-content').should('contain', 'Edit book successfully');

    
  });

  it('Search and edit book with title and ISBN the same of another book', () => {

    cy.once('uncaught:exception', () => false);
    cy.visit('http://localhost:5000/admin/manage-books');
    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();

    //Check if the input information are correctly input
    cy.get('[data-testid="bookTableRow"]').should('have.length', 1);
    cy.get('[data-testid="bookTableRow"] td:nth-child(2)').contains(bookTitle);
    cy.get('[data-testid="bookTableRow"] td:nth-child(5)').contains(bookStock);
    cy.get('[data-testid="bookTableRow"] td:nth-child(6) button').contains('Edit').click();
    

    //Enter title and ISBN of another book
    cy.get('#editBookTitle').clear().type('Frankenstein');
    cy.get('#editBookISBN').clear().type('13, 978-0486282114');
    cy.get('#editBookButton').click();

    cy.get('.notification-title').should('contain', 'Edit book details failed')
    cy.get('.notification-content').should('contain', 'Edit book failed');

    
  });

  it('Delete book', ()=> {
    cy.visit('http://localhost:5000/admin/manage-books');
    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();
    cy.get('[data-testid="bookTableRow"]').should('have.length', 1);
    cy.get('[data-testid="bookTableRow"] td:nth-child(6) button').contains('Delete').click();

    //The notification should show that the book has been deleted successfully
    cy.get('.notification-title').should('contain', 'Delete book successfully')
    cy.get('.notification-content').should('contain', 'Delete book successfully')

    //Search the book again and it should show no result
    cy.get('#editBookTab').click();
    cy.get('#searchBookTitle').clear();
    cy.get('#searchBookTitle').type(bookTitle);
    cy.get('#searchBookButton').click();
    cy.get('[data-testid="bookTableRow"]').should('have.length', 0);
  });
})

