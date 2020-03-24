/// <reference types="cypress" />

context('Actions', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000')
  })

  it('All + elements are clickable', () => {
    cy.get('.step-up').click( { multiple: true } )

    // This gets the "first" input from the sidebar. From clicking step up,
    // the number of days to project should increase from default 60 to 70.
    cy.get('input.st-al')
      .should('has.value', '70')
  })
})
