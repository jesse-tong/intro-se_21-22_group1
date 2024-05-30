

describe('Manage borrow tests', () => {
    
    it('Add borrow test', () => {
        cy.visit('http://localhost:5000/admin/manage-borrow');
        cy.get('#searchTab').click();
        cy.get('#searchUserEmail').type('@gmail.com');
        cy.get('#searchUserButton').click();

        //Store the first user's first column value (User ID) and select the first user
        cy.get('[data-testid="searchUserResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const userId = $value.text();
            cy.wrap(userId).as('userId');
        });

        cy.get('[data-testid="searchUserResultRow"] td:nth-child(5)').contains('Select').click();

        cy.get('#searchBookTitle').type('Test book');
        cy.get('#searchBookButton').click();

        cy.get('[data-testid="searchBookResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const bookId = $value.text();
            cy.wrap(bookId).as('bookId');
        });
        cy.get('[data-testid="searchBookResultRow"] td:nth-child(6)').contains('Select').click();

        cy.get('#addBorrowTab').click();
        
        cy.get('@userId').then(userId => {
            cy.get('#selectedUserId').should('have.value', userId);
        });

        cy.get('@bookId').then(bookId => {
            cy.get('#selectedBookId').should('have.value', bookId);
        });

        cy.get('#startBorrow').clear().type('2024-05-15T10:00:00');
        cy.get('#endBorrow').clear().type('2024-06-15T23:59:59');
        cy.get('#isApproved').check();
        cy.get('#addBorrowButton').click();

        cy.get('.notification-title').should('contain', 'Add success');
    });

    it('Add borrow test with book stock equals 0', () => {
        cy.visit('http://localhost:5000/admin/manage-borrow');
        cy.get('#searchTab').click();
        cy.get('#searchUserEmail').type('@gmail.com');
        cy.get('#searchUserButton').click();

        //Store the first user's first column value (User ID) and select the first user
        cy.get('[data-testid="searchUserResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const userId = $value.text();
            cy.wrap(userId).as('userId');
        });

        cy.get('[data-testid="searchUserResultRow"] td:nth-child(5)').contains('Select').click();

        cy.get('#searchBookTitle').type('Test book 2');
        cy.get('#searchBookButton').click();

        cy.get('[data-testid="searchBookResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const bookId = $value.text();
            cy.wrap(bookId).as('bookId');
        });

        cy.get('[data-testid="searchBookResultRow"] td:nth-child(6)').contains('Select').click();

        cy.get('#addBorrowTab').click();
        
        cy.get('@userId').then(userId => {
            cy.get('#selectedUserId').should('have.value', userId);
        });

        cy.get('@bookId').then(bookId => {
            cy.get('#selectedBookId').should('have.value', bookId);
        });

        cy.get('#startBorrow').clear().type('2024-05-15T10:00:00');
        cy.get('#endBorrow').clear().type('2024-06-15T23:59:59');
        cy.get('#isApproved').check();
        cy.get('#addBorrowButton').click();

        cy.get('.notification-title').should('contain', 'Add failed');
    });

    it('Add borrow test with end date before start date', () => {
        cy.visit('http://localhost:5000/admin/manage-borrow');
        cy.get('#searchTab').click();
        cy.get('#searchUserEmail').type('@gmail.com');
        cy.get('#searchUserButton').click();

        //Store the first user's first column value (User ID) and select the first user
        cy.get('[data-testid="searchUserResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const userId = $value.text();
            cy.wrap(userId).as('userId');
        });

        cy.get('[data-testid="searchUserResultRow"] td:nth-child(5)').contains('Select').click();

        cy.get('#searchBookTitle').type('Test book');
        cy.get('#searchBookButton').click();

        cy.get('[data-testid="searchBookResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const bookId = $value.text();
            cy.wrap(bookId).as('bookId');
        });
        cy.get('[data-testid="searchBookResultRow"] td:nth-child(6)').contains('Select').click();

        cy.get('#addBorrowTab').click();
        
        cy.get('@userId').then(userId => {
            cy.get('#selectedUserId').should('have.value', userId);
        });

        cy.get('@bookId').then(bookId => {
            cy.get('#selectedBookId').should('have.value', bookId);
        });

        cy.get('#startBorrow').clear().type('2024-05-15T10:00:00');
        cy.get('#endBorrow').clear().type('2023-03-15T23:59:59');
        cy.get('#isApproved').check();
        cy.get('#addBorrowButton').click();

        cy.get('.notification-title').should('contain', 'Add failed');
        cy.get('.notification-content').should('contain', 'Invalid duration');
    });

    it('Add borrow test without start date', () => {
        cy.visit('http://localhost:5000/admin/manage-borrow');
        cy.get('#searchTab').click();
        cy.get('#searchUserEmail').type('@gmail.com');
        cy.get('#searchUserButton').click();

        //Store the first user's first column value (User ID) and select the first user
        cy.get('[data-testid="searchUserResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const userId = $value.text();
            cy.wrap(userId).as('userId');
        });

        cy.get('[data-testid="searchUserResultRow"] td:nth-child(5)').contains('Select').click();

        cy.get('#searchBookTitle').type('Test book 2');
        cy.get('#searchBookButton').click();

        cy.get('[data-testid="searchBookResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const bookId = $value.text();
            cy.wrap(bookId).as('bookId');
        });

        cy.get('[data-testid="searchBookResultRow"] td:nth-child(6)').contains('Select').click();

        cy.get('#addBorrowTab').click();
        
        cy.get('@userId').then(userId => {
            cy.get('#selectedUserId').should('have.value', userId);
        });

        cy.get('@bookId').then(bookId => {
            cy.get('#selectedBookId').should('have.value', bookId);
        });

        
        cy.get('#endBorrow').clear().type('2024-06-15T23:59:59');
        cy.get('#isApproved').check();
        cy.get('#addBorrowButton').click();

        cy.get('.notification-content').should('contain', 'No start date or end date selected');
    });

    it('Add borrow test without end date', () => {
        cy.visit('http://localhost:5000/admin/manage-borrow');
        cy.get('#searchTab').click();
        cy.get('#searchUserEmail').type('@gmail.com');
        cy.get('#searchUserButton').click();

        //Store the first user's first column value (User ID) and select the first user
        cy.get('[data-testid="searchUserResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const userId = $value.text();
            cy.wrap(userId).as('userId');
        });

        cy.get('[data-testid="searchUserResultRow"] td:nth-child(5)').contains('Select').click();

        cy.get('#searchBookTitle').type('Test book 2');
        cy.get('#searchBookButton').click();

        cy.get('[data-testid="searchBookResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const bookId = $value.text();
            cy.wrap(bookId).as('bookId');
        });

        cy.get('[data-testid="searchBookResultRow"] td:nth-child(6)').contains('Select').click();

        cy.get('#addBorrowTab').click();
        
        cy.get('@userId').then(userId => {
            cy.get('#selectedUserId').should('have.value', userId);
        });

        cy.get('@bookId').then(bookId => {
            cy.get('#selectedBookId').should('have.value', bookId);
        });

        
        cy.get('#startBorrow').clear().type('2024-06-15T23:59:59');
        cy.get('#isApproved').check();
        cy.get('#addBorrowButton').click();

        cy.get('.notification-content').should('contain', 'No start date or end date selected');
    });

    it('Add borrow test without user selected', () => {
        cy.visit('http://localhost:5000/admin/manage-borrow');
        cy.get('#searchTab').click();
        cy.get('#searchUserEmail').type('@gmail.com');
        cy.get('#searchUserButton').click();

        cy.get('#searchBookTitle').type('Test book 2');
        cy.get('#searchBookButton').click();

        cy.get('[data-testid="searchBookResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const bookId = $value.text();
            cy.wrap(bookId).as('bookId');
        });

        cy.get('[data-testid="searchBookResultRow"] td:nth-child(6)').contains('Select').click();

        cy.get('#addBorrowTab').click();

        cy.get('@bookId').then(bookId => {
            cy.get('#selectedBookId').should('have.value', bookId);
        });

        cy.get('#startBorrow').clear().type('2024-05-15T10:00:00');
        cy.get('#endBorrow').clear().type('2024-06-15T23:59:59');
        cy.get('#isApproved').check();
        cy.get('#addBorrowButton').click();

        cy.get('.notification-content').should('contain', 'No user ID selected or invalid user ID');
    });

    it('Add borrow test without book selected', () => {
        cy.visit('http://localhost:5000/admin/manage-borrow');
        cy.get('#searchTab').click();
        cy.get('#searchUserEmail').type('@gmail.com');
        cy.get('#searchUserButton').click();

        //Store the first user's first column value (User ID) and select the first user
        cy.get('[data-testid="searchUserResultRow"]:nth-child(1) td:nth-child(1)').then(($value)=> {
            const userId = $value.text();
            cy.wrap(userId).as('userId');
        });

        cy.get('[data-testid="searchUserResultRow"] td:nth-child(5)').contains('Select').click();     

        cy.get('#addBorrowTab').click();
        
        cy.get('@userId').then(userId => {
            cy.get('#selectedUserId').should('have.value', userId);
        });


        cy.get('#startBorrow').clear().type('2024-05-15T10:00:00');
        cy.get('#endBorrow').clear().type('2024-06-15T23:59:59');
        cy.get('#isApproved').check();
        cy.get('#addBorrowButton').click();

        cy.get('.notification-content').should('contain', 'No book ID selected or invalid book ID');
    });
});