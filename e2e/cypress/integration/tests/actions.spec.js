/// <reference types="cypress" />

context('Actions', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000')
  });

  it('All + elements are clickable', () => {
    cy.get('.step-up').click( { multiple: true } );

    // This gets the "first" input from the sidebar. From clicking step up,
    // the Regional Population should increase from default 4119405 to 4219405.
    cy.get('input.st-al')
      .should('has.value', '4119406')
  })
});
