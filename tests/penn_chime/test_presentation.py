import pytest

from src.penn_chime.presentation import display_header


def header_test_helper(expected_str, model, param, mock_st):
    display_header(mock_st, model, param)
    assert [
        s for s in mock_st.render_store if expected_str in s
    ], f"Expected the string '{expected_str}' in the display header"


def test_penn_logo_in_header(model, param, mock_st):
    penn_css = '<link rel="stylesheet" href="https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css">'
    header_test_helper(penn_css, model, param, mock_st)


def test_the_rest_of_header_shows_up(model, param, mock_st):
    random_part_of_header = "implying an effective $R_t$ of"
    header_test_helper(random_part_of_header, model, param, mock_st)


def test_mitigation_statement(model, param, mock_st):
    expected_doubling = "outbreak **reduces the doubling time to 7.8** days"
    header_test_helper(expected_doubling, model, param, mock_st)


def test_mitigation_statement_halving(halving_model, halving_param, mock_st):
    expected_halving = "outbreak **halves the infections every 51.9** days"
    header_test_helper(expected_halving, halving_model, halving_param, mock_st)


def test_growth_rate(model, param, mock_st):
    initial_growth = "and daily growth rate of **12.25%**."
    header_test_helper(initial_growth, model, param, mock_st)

    mitigated_growth = "and daily growth rate of **9.34%**."
    header_test_helper(mitigated_growth, model, param, mock_st)


def test_growth_rate_halving(halving_model, halving_param, mock_st):
    mitigated_halving = "and daily growth rate of **-1.33%**."
    header_test_helper(mitigated_halving, halving_model, halving_param, mock_st)


@pytest.mark.xfail()
def test_header_fail(mock_st, param):
    """
    Just proving to myself that these tests work
    """
    some_garbage = "ajskhlaeHFPIQONOI8QH34TRNAOP8ESYAW4"
    display_header(mock_st, param)
    assert len(
        list(filter(lambda s: some_garbage in s, mock_st.render_store))
    ), "This should fail"
