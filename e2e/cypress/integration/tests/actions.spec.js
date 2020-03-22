/// <reference types="cypress" />

context('Actions', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000')
  })

  it('All + elements are clickable', () => {
    cy.get('.step-up').click( { multiple: true } )

    cy.get('input.st-al')
      .should('has.value', '7')
  })
})
