var bookId = 1;
var rating = 9;
var invalidRating = 'abc';
var invalidRating2 = '18'; //Since rating can only between 0 and 10
var invalidRatingFloat = '8.3';
var content = 'Test content';

describe('Add and edit comment tests', () => {
    
    it('Add comment with rating and content', () => {
        cy.visit('http://localhost:5000/book/' + bookId); //Go to a book detail page
        cy.get('#addCommentBookId').should('have.value', bookId);
        cy.get('#addCommentRating').clear().type(rating);
        cy.get('#addCommentContent').clear().type(content);
        cy.get('#addCommentButton').click();
        cy.get('.notification-title').should('contain', 'Add comment successfully');
        cy.get('.notification-content').should('contain', 'Add comment successfully');
        cy.wait(100);

    });

    it('Add comment without rating', () => {
        cy.visit('http://localhost:5000/book/' + bookId); //Go to a book detail page
        cy.get('#addCommentBookId').should('have.value', bookId);
        cy.get('#addCommentRating').clear();
        cy.get('#addCommentContent').clear().type(content);
        cy.get('#addCommentButton').click();
        cy.get('.notification-title').should('contain', 'No rating or invalid comment rating');
        cy.get('.notification-content').should('contain', 'No rating or invalid comment rating');
        cy.wait(100);
    });

    it('Add comment without invalid rating out of range', () => {
        cy.visit('http://localhost:5000/book/' + bookId); //Go to a book detail page
        cy.get('#addCommentBookId').should('have.value', bookId);
        cy.get('#addCommentRating').clear().type(invalidRating2);
        cy.get('#addCommentContent').clear().type(content);
        cy.get('#addCommentButton').click();
        cy.get('.notification-title').should('contain', 'No rating or invalid comment rating');
        cy.get('.notification-content').should('contain', 'No rating or invalid comment rating');
        cy.wait(100);
    });

    it('Add comment with a rating that\'s not a integer', () => {
        cy.visit('http://localhost:5000/book/' + bookId); //Go to a book detail page
        cy.get('#addCommentBookId').should('have.value', bookId);
        cy.get('#addCommentRating').clear().type(invalidRatingFloat);
        cy.get('#addCommentContent').clear().type(content);
        cy.get('#addCommentButton').click();
        cy.get('.notification-title').should('contain', 'No rating or invalid comment rating');
        cy.get('.notification-content').should('contain', 'No rating or invalid comment rating');
        cy.wait(100);
    });

    it('Add comment with a non-number integer', () => {
        cy.visit('http://localhost:5000/book/' + bookId); //Go to a book detail page
        cy.get('#addCommentBookId').should('have.value', bookId);
        cy.get('#addCommentRating').clear().type(invalidRating);
        cy.get('#addCommentContent').clear().type(content);
        cy.get('#addCommentButton').click();
        cy.get('.notification-title').should('contain', 'No rating or invalid comment rating');
        cy.get('.notification-content').should('contain', 'No rating or invalid comment rating');
        cy.wait(100);
    });
});