/// <reference types="cypress" />

context('Increment steppers', () => {
  beforeEach(() => {
    cy.visit('/')
  });

  it('Increment regional population', () => {
    cy.contains('Regional population (3600000)');

    cy.get('input[type=number]').eq(0)
      .should('has.value', '3600000');

    cy.get('.step-up').eq(0).click();

    cy.get('input[type=number]').eq(0)
      .should('has.value', '3600001');

    cy.contains('Regional population (3600001)');
  });

  it('Increment hospital market share', () => {
    cy.contains('The estimated number of currently infected individuals is 20128.');

    cy.get('input[type=number]').eq(1)
      .should('has.value', '15');

    cy.get('.step-up').eq(1).click();

    cy.get('input[type=number]').eq(1)
      .should('has.value', '15.1');

    cy.contains('The estimated number of currently infected individuals is 19996.');
  });

  it('Increment doubling time', () => {
    cy.contains('An initial doubling time of 4.0 days');

    cy.get('input[type=number]').eq(3)
      .should('has.value', '4');

    cy.get('.step-up').eq(3).click();

    cy.get('input[type=number]').eq(3)
      .should('has.value', '4.25');

    cy.contains('An initial doubling time of 4.25 days');
  });
});
