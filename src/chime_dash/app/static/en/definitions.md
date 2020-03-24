## Guidance on Selecting Inputs
* **Hospitalized COVID-19 Patients:**
    The number of patients currently hospitalized with COVID-19 **at your hospital(s)**.
    This number is used in conjunction with Hospital Market Share and Hospitalization % to estimate the total number of infected individuals in your region.
* **Doubling Time (days):**
    This parameter drives the rate of new cases during the early phases of the outbreak.
    The American Hospital Association currently projects doubling rates between 7 and 10 days.
    This is the doubling time you expect under status quo conditions.
    To account for reduced contact and other public health interventions, modify the _Social distancing_ input.
* **Social distancing (% reduction in person-to-person physical contact):**
    This parameter allows users to explore how reduction in interpersonal contact & transmission (hand-washing) might slow the rate of new infections.
    It is your estimate of how much social contact reduction is being achieved in your region relative to the status quo.
    While it is unclear how much any given policy might affect social contact (eg. school closures or remote work), this parameter lets you see how projections change with percentage reductions in social contact.
* **Hospitalization %(total infections):
    ** Percentage of **all** infected cases which will need hospitalization.
* **ICU %(total infections):**
    Percentage of **all** infected cases which will need to be treated in an ICU.
* **Ventilated %(total infections):**
    Percentage of **all** infected cases which will need mechanical ventilation.
* **Hospital Length of Stay:**
    Average number of days of treatment needed for hospitalized COVID-19 patients.
* **ICU Length of Stay:**
    Average number of days of ICU treatment needed for ICU COVID-19 patients.
* **Vent Length of Stay:**
    Average number of days of ventilation needed for ventilated COVID-19 patients.
* **Hospital Market Share (%):**
    The proportion of patients in the region that are likely to come to your hospital (as opposed to other hospitals in the region) when they get sick.
    One way to estimate this is to look at all of the hospitals in your region and add up all of the beds.
    The number of beds at your hospital divided by the total number of beds in the region times 100 will give you a reasonable starting estimate.
* **Regional Population:**
    Total population size of the catchment region of your hospital(s).
* **Currently Known Regional Infections**:
    The number of infections reported in your hospital's catchment region.
    This is only used to compute detection rate - **it will not change projections**.
    This input is used to estimate the detection rate of infected individuals.
