Feature: As a website user,
            I want to be able to add a portfolio

  Scenario: Successfully added portfolio
     Given The application is setup
     And   i login with "lucas2" and "test"
      When i add a portfolio called "portfolio1"
      Then i should see the alert "Added portfolio 'portfolio1'"

  Scenario: Existing portfolio with given name
     Given The application is setup
     And   i login with "lucas2" and "test"
      When i add a portfolio called "portfolio1"
      Then i should see the error "A portfolio with that name already exists"

  Scenario: Portfolio name contains invalid non-alphanumeric characters
     Given The application is setup
     And   i login with "lucas2" and "test"
      When i add a portfolio called "['portfolio1']"
      Then i should see the error "The portfolio name must contain only letters and numbers"

