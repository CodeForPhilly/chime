from time import sleep

import pytest

test_cases = [
    ('market_share', '100', 'Hospital market share (100%)'),
    ('population', '100', 'Region size (100)'),
    ('current_hospitalized', '100', 'Hospitalizations (100)'),

    ('doubling_time', '100', 'of 100 days'),
    ('relative_contact_rate', '100', 'A 100% reduction in social'),

    ('hospitalized_rate', '100', 'Hospitalization rate (100%)'),
]


@pytest.mark.parametrize('input_element, value, control', test_cases)
def test_controls(test_app, input_element, value, control):
    """
    Check if elements actually change data in intro (checking if controls are working)
    Intro text example:
    The estimated number of currently infected individuals is 560. The 510 confirmed cases in the region imply a 91% rate of detection. This is based on current inputs for Hospitalizations (14), Hospitalization rate (2%), Region size (4119405), and Hospital market share (100%).
An initial doubling time of 4 days and a recovery time of 14 days imply an $R_0$ of 3.65.
Mitigation: A 0% reduction in social contact after the onset of the outbreak reduces the doubling time to 4.0 days, implying an effective $R_t$ of $3.65$.
    """
    element = test_app.driver.find_element_by_id(input_element)

    element.clear()
    sleep(0.5)
    element.send_keys(value)
    sleep(0.5)

    intro = test_app.driver.find_element_by_id('intro').text

    assert control in intro
