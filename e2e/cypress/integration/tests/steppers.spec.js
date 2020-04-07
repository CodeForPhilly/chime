/// <reference types="cypress" />

context('Increment steppers', () => {
  beforeEach(() => {
    cy.visit('/')
  });

  it('Increment regional population', () => {
    cy.contains('Hospitalized Admissions peaks at 300');

    cy.get('input[type=number]').eq(0)
      .should('has.value', '3600000');

    cy.get('.step-up').eq(0).click();

    cy.get('input[type=number]').eq(0)
      .should('has.value', '3600001');

    cy.contains('Hospitalized Admissions peaks at 300');
  });

  it('Increment hospital market share', () => {
    cy.contains('Hospitalized Admissions peaks at 300');

    cy.get('input[type=number]').eq(1)
      .should('has.value', '15');

    cy.get('.step-up').eq(1).click();

    cy.get('input[type=number]').eq(1)
      .should('has.value', '15.1');

    cy.contains('Hospitalized Admissions peaks at 302');
  });

  it('Increment doubling time', () => {
    cy.contains('Hospitalized Admissions peaks at 300');

    cy.get('input[type=number]').eq(3)
      .should('has.value', '4');

    cy.get('.step-up').eq(3).click();

    cy.get('input[type=number]').eq(3)
      .should('has.value', '4.25');

    cy.contains('Hospitalized Admissions peaks at 272');
  });
});
