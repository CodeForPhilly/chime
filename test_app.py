import pytest

from penn_chime.models import sir
from penn_chime.presentation import display_header


# set up
class MockStreamlit:
    def __init__(self):
        self.render_store = []
        self.markdown = self.just_store_instead_of_rendering
        self.latex = self.just_store_instead_of_rendering
        self.subheader = self.just_store_instead_of_rendering

    def just_store_instead_of_rendering(self, inp, *args, **kwargs):
        self.render_store.append(inp)
        return None


st = MockStreamlit()


def test_header():
    penn_css = '<link rel="stylesheet" href="https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css">'
    display_header(st, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    assert len(
        list(filter(lambda s: penn_css in s, st.render_store))
    ), "The Penn Medicine header should be printed"


@pytest.mark.xfail()
def test_header_fail():
    some_garbage = 'ajskhlaeHFPIQONOI8QH34TRNAOP8ESYAW4'
    display_header(st, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    assert len(
        list(filter(lambda s: some_garbage in s, st.render_store))
    ), "This should fail"

# Test the math


def test_sir():
    """
    Someone who is good at testing, help
    """
    assert sir((100, 1, 0), 0.2, 0.5, 1) == (
        0.7920792079207921,
        0.20297029702970298,
        0.0049504950495049506,
    ), "This contrived example should work"

