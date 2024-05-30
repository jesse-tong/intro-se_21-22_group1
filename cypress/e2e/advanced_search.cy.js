var title = 'Frankenstein';
var id = '1';
var isbn = '9788408061052';
var authors = ['Mary Shelley', 'Miguel de Cervantes'];
var genres = ['Horror', 'Epic', 'War & Millitary Fiction'];

describe('Advanced search tests', () => {
    
    it('Search results by title should contain search title', () => {
        cy.visit('http://localhost:5000/book/advanced-search');
        cy.get('#title').clear().type(title);
        cy.get('#searchButton').click();
        cy.get('[data-testid="searchResultRow"] td:nth-child(3)').each(($el, index, $list) => {
            cy.wrap($el.text()).should('contain', title);
        });
    });
    it('Search results by ID should contain ID', () => {
        cy.visit('http://localhost:5000/book/advanced-search');
        cy.get('#id').clear().type(id);
        cy.get('#searchButton').click();
        cy.get('[data-testid="searchResultRow"] td:nth-child(2)').each(($el, index, $list) => {
            cy.wrap($el.text()).should('contain', id);
        });
    });
    it('Search results by ISBN should contain ISBN', () => {
        cy.visit('http://localhost:5000/book/advanced-search');
        cy.get('#isbn').clear().type(isbn);
        cy.get('#searchButton').click();
        cy.get('[data-testid="searchResultRow"] td:nth-child(5)').each(($el, index, $list) => {
            cy.wrap($el.text()).should('contain', isbn);
        });
    });
    it('Search results by authors should contain at least one search author', () => {
        cy.visit('http://localhost:5000/book/advanced-search');
        cy.get('#authors').clear().type(authors.join(', '));
        cy.get('#searchButton').click();
        cy.get('[data-testid="searchResultRow"] td:nth-child(7)').contains('Details').click();
        
        cy.get('[data-testid="authorBadge"]').then(($els) => {
            var authorsOfBook = Cypress.$.makeArray($els);
            authorsOfBook = authorsOfBook.map((el) => { return el.innerText; })
            expect(authorsOfBook, 'to array').to.be.an('array');
            
            return authorsOfBook;
        }).then((authorsOfBook) => {
            var overlapAuthors = authorsOfBook.filter(author => authors.includes(author));
            expect(overlapAuthors).to.have.length.greaterThan(0);
        });
    });
    it('Search results by genres should contain at least one search genre', () => {
        cy.visit('http://localhost:5000/book/advanced-search');
        cy.get('#genres').clear().type(genres.join(', '));
        cy.get('#searchButton').click();
        cy.get('[data-testid="searchResultRow"] td:nth-child(7)').contains('Details').click();

        cy.get('[data-testid="genreBadge"]').then(($els) => {
            var genresOfBook = Cypress.$.makeArray($els);
            genresOfBook = genresOfBook.map((el) => { return el.innerText; })
            expect(genresOfBook, 'to array').to.be.an('array');
            
            return genresOfBook;
        }).then((genresOfBook) => {
            var overlapGenres = genresOfBook.filter(genre => genres.includes(genre));
            expect(overlapGenres).to.have.length.greaterThan(0);
        });
    });
});