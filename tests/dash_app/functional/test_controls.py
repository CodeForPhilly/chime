def test_example(test_app):
    parameters = ['market_share', 'susceptible']

    elements = {k: test_app.driver.find_element_by_id(k) for k in parameters}

    elements['market_share'].clear()
    elements['market_share'].send_keys('100')

    new_admission_graph = test_app.driver.find_element_by_id('new-admissions-graph')
    admitted_patients_graph = test_app.driver.find_element_by_id('admitted-patients-graph')
