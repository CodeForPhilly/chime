"""Streamlit display."""

import os
import json

import pandas as pd

from ..constants import (
    CHANGE_DATE,
    DOCS_URL,
    EPSILON,
    FLOAT_INPUT_MIN,
    FLOAT_INPUT_STEP,
    VERSION,
)
from ..model.parameters import Parameters, Disposition
from ..utils import dataframe_to_base64
from .spreadsheet import spreadsheet

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """


########
# Text #
########


def display_header(st, m, p):

    infected_population_warning_str = (
        """(Warning: The number of estimated infections is greater than the total regional population. Please verify the values entered in the sidebar.)"""
        if m.infected > p.population
        else ""
    )

    st.markdown(
        """
<link rel="stylesheet" href="https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css">
<div class="penn-medicine-header__content">
    <a href="https://www.pennmedicine.org" class="penn-medicine-header__logo"
        title="Go to the Penn Medicine home page">Penn Medicine</a>
    <a id="title" class="penn-medicine-header__title">COVID-19 Hospital Impact Model for Epidemics (CHIME)</a>
</div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """**Notice**: *There is a high
degree of uncertainty about the details of COVID-19 infection, transmission, and the effectiveness of social distancing
measures. Long-term projections made using this simplified model of outbreak progression should be treated with extreme caution.*
    """
    )
    st.markdown(
        """
This tool was developed by [Predictive Healthcare](http://predictivehealthcare.pennmedicine.org/) at
Penn Medicine to assist hospitals and public health officials with hospital capacity planning.
Please read [How to Use CHIME]({docs_url}) to customize inputs for your region.""".format(docs_url=DOCS_URL))

    st.markdown(
        """The estimated number of currently infected individuals is **{total_infections:.0f}**. This is based on current inputs for
    Hospitalizations (**{current_hosp}**), Hospitalization rate (**{hosp_rate:.0%}**), Regional population (**{S}**),
    and Hospital market share (**{market_share:.0%}**).

{infected_population_warning_str}

An initial doubling time of **{doubling_time}** days and a recovery time of **{recovery_days}** days imply an $R_0$ of
 **{r_naught:.2f}** and daily growth rate of **{daily_growth:.2f}%**.

**Mitigation**: A **{relative_contact_rate:.0%}** reduction in social contact after the onset of the
outbreak **{impact_statement:s} {doubling_time_t:.1f}** days, implying an effective $R_t$ of **${r_t:.2f}$**
and daily growth rate of **{daily_growth_t:.2f}%**.
""".format(
            total_infections=m.infected,
            current_hosp=p.current_hospitalized,
            hosp_rate=p.hospitalized.rate,
            S=p.population,
            market_share=p.market_share,
            recovery_days=p.infectious_days,
            r_naught=m.r_naught,
            doubling_time=p.doubling_time,
            relative_contact_rate=p.relative_contact_rate,
            r_t=m.r_t,
            doubling_time_t=abs(m.doubling_time_t),
            impact_statement=(
                "halves the infections every"
                if m.r_t < 1
                else "reduces the doubling time to"
            ),
            daily_growth=m.daily_growth_rate * 100.0,
            daily_growth_t=m.daily_growth_rate_t * 100.0,
            infected_population_warning_str=infected_population_warning_str,
        )
    )

    return None


class Input:
    """Helper to separate Streamlit input definition from creation/rendering"""

    def __init__(self, st_obj, label, value, kwargs):
        self.st_obj = st_obj
        self.label = label
        self.value = value
        self.kwargs = kwargs

    def __call__(self):
        return self.st_obj(self.label, value=self.value, **self.kwargs)


class NumberInput(Input):
    def __init__(
        self,
        st_obj,
        label,
        min_value=None,
        max_value=None,
        value=None,
        step=None,
        format=None,
        key=None,
    ):
        kwargs = dict(
            min_value=min_value,
            max_value=max_value,
            step=step,
            format=format,
            key=key,
        )
        super().__init__(st_obj.number_input, label, value, kwargs)


class DateInput(Input):
    def __init__(self, st_obj, label, value=None, key=None):
        kwargs = dict(key=key)
        super().__init__(st_obj.date_input, label, value, kwargs)


class PercentInput(NumberInput):
    def __init__(
        self,
        st_obj,
        label,
        min_value=0.0,
        max_value=100.0,
        value=None,
        step=FLOAT_INPUT_STEP,
        format="%f",
        key=None,
    ):
        super().__init__(
            st_obj,
            label,
            min_value,
            max_value,
            value * 100.0,
            step,
            format,
            key,
        )

    def __call__(self):
        return super().__call__() / 100.0


class CheckboxInput(Input):
    def __init__(self, st_obj, label, value=None, key=None):
        kwargs = dict(key=key)
        super().__init__(st_obj.checkbox, label, value, kwargs)


def display_sidebar(st, d: Parameters) -> Parameters:
    # Initialize variables
    # these functions create input elements and bind the values they are set to
    # to the variables they are set equal to
    # it's kindof like ember or angular if you are familiar with those

    st_obj = st.sidebar
    # used_widget_key = st.get_last_used_widget_key ( )

    current_hospitalized_input = NumberInput(
        st_obj,
        "Currently hospitalized COVID-19 patients",
        min_value=0,
        value=d.current_hospitalized,
        step=1,
        format="%i",
    )
    n_days_input = NumberInput(
        st_obj,
        "Number of days to project",
        min_value=30,
        value=d.n_days,
        step=1,
        format="%i",
    )
    doubling_time_input = NumberInput(
        st_obj,
        "Doubling time in days (up to today)",
        min_value=0.5,
        value=d.doubling_time,
        step=0.25,
        format="%f",
    )
    current_date_input = DateInput(
        st_obj, "Current date (default is today)", value=d.current_date,
    )
    date_first_hospitalized_input = DateInput(
        st_obj, "Date of first hospitalized case (enter this date to have CHIME estimate the initial doubling time)",
        value=d.date_first_hospitalized,
    )
    mitigation_date_input = DateInput(
        st_obj, "Date of social distancing measures effect (may be delayed from implementation)",
        value=d.mitigation_date
    )
    relative_contact_pct_input = PercentInput(
        st_obj,
        "Social distancing (% reduction in social contact going forward)",
        min_value=0.0,
        max_value=100.0,
        value=d.relative_contact_rate,
        step=1.0,
    )
    hospitalized_pct_input = PercentInput(
        st_obj,
        "Hospitalization %(total infections)",
        value=d.hospitalized.rate,
        min_value=FLOAT_INPUT_MIN,
        max_value=100.0
    )
    icu_pct_input = PercentInput(
        st_obj,
        "ICU %(total infections)",
        min_value=0.0,
        value=d.icu.rate,
        step=0.05
    )
    ventilated_pct_input = PercentInput(
        st_obj, "Ventilated %(total infections)", value=d.ventilated.rate,
    )
    hospitalized_days_input = NumberInput(
        st_obj,
        "Average hospital length of stay (in days)",
        min_value=1,
        value=d.hospitalized.days,
        step=1,
        format="%i",
    )
    icu_days_input = NumberInput(
        st_obj,
        "Average days in ICU",
        min_value=1,
        value=d.icu.days,
        step=1,
        format="%i",
    )
    ventilated_days_input = NumberInput(
        st_obj,
        "Average days on ventilator",
        min_value=1,
        value=d.ventilated.days,
        step=1,
        format="%i",
    )
    market_share_pct_input = PercentInput(
        st_obj,
        "Hospital market share (%)",
        min_value=0.5,
        value=d.market_share,
    )
    population_input = NumberInput(
        st_obj,
        "Regional population",
        min_value=1,
        value=(d.population),
        step=1,
        format="%i",
    )
    infectious_days_input = NumberInput(
        st_obj,
        "Infectious days",
        min_value=1,
        value=d.infectious_days,
        step=1,
        format="%i",
    )
    max_y_axis_set_input = CheckboxInput(
        st_obj, "Set the Y-axis on graphs to a static value"
    )
    max_y_axis_input = NumberInput(
        st_obj, "Y-axis static value", value=500, format="%i", step=25
    )

    # Build in desired order
    st.sidebar.markdown(
        """**CHIME [{version}](https://github.com/CodeForPhilly/chime/releases/tag/{version}) ({change_date})**""".format(
            change_date=CHANGE_DATE,
            version=VERSION,
        )
    )

    st.sidebar.markdown(
        "### Hospital Parameters [ℹ]({docs_url}/what-is-chime/parameters#hospital-parameters)".format(
            docs_url=DOCS_URL
        )
    )
    population = population_input()
    market_share = market_share_pct_input()
    # known_infected = known_infected_input()
    current_hospitalized = current_hospitalized_input()

    st.sidebar.markdown(
        "### Spread and Contact Parameters [ℹ]({docs_url}/what-is-chime/parameters#spread-and-contact-parameters)".format(
            docs_url=DOCS_URL
        )
    )

    if st.sidebar.checkbox(
        "I know the date of the first hospitalized case."
    ):
        date_first_hospitalized = date_first_hospitalized_input()
        doubling_time = None
    else:
        doubling_time = doubling_time_input()
        date_first_hospitalized = None

    if st.sidebar.checkbox(
        "Social distancing measures have been implemented",
        value=(d.relative_contact_rate > EPSILON)
    ):
        mitigation_date = mitigation_date_input()
        relative_contact_rate = relative_contact_pct_input()
    else:
        mitigation_date = None
        relative_contact_rate = EPSILON

    st.sidebar.markdown(
        "### Severity Parameters [ℹ]({docs_url}/what-is-chime/parameters#severity-parameters)".format(
            docs_url=DOCS_URL
        )
    )
    hospitalized_rate = hospitalized_pct_input()
    icu_rate = icu_pct_input()
    ventilated_rate = ventilated_pct_input()
    infectious_days = infectious_days_input()
    hospitalized_days = hospitalized_days_input()
    icu_days = icu_days_input()
    ventilated_days = ventilated_days_input()

    st.sidebar.markdown(
        "### Display Parameters [ℹ]({docs_url}/what-is-chime/parameters#display-parameters)".format(
            docs_url=DOCS_URL
        )
    )
    n_days = n_days_input()
    max_y_axis_set = max_y_axis_set_input()

    max_y_axis = None
    if max_y_axis_set:
        max_y_axis = max_y_axis_input()

    current_date = current_date_input()
    #Subscribe implementation
    subscribe(st_obj)

    return Parameters(
        current_hospitalized=current_hospitalized,
        current_date=current_date,
        date_first_hospitalized=date_first_hospitalized,
        doubling_time=doubling_time,
        hospitalized=Disposition.create(
            rate=hospitalized_rate,
            days=hospitalized_days),
        icu=Disposition.create(
            rate=icu_rate,
            days=icu_days),
        infectious_days=infectious_days,
        market_share=market_share,
        max_y_axis=max_y_axis,
        mitigation_date=mitigation_date,
        n_days=n_days,
        population=population,
        recovered=d.recovered,
        relative_contact_rate=relative_contact_rate,
        ventilated=Disposition.create(
            rate=ventilated_rate,
            days=ventilated_days),
    )

#Read the environment variables and cteate json key object to use with ServiceAccountCredentials
def readGoogleApiSecrets():
    client_secret = {}
    os.getenv
    type = os.getenv ('GAPI_CRED_TYPE').strip()
    print (type)
    client_secret['type'] = type,
    client_secret['project_id'] = os.getenv ('GAPI_CRED_PROJECT_ID'),
    client_secret['private_key_id'] = os.getenv ('GAPI_CRED_PRIVATE_KEY_ID'),
    client_secret['private_key'] = os.getenv ('GAPI_CRED_PRIVATE_KEY'),
    client_secret['client_email'] = os.getenv ('GAPI_CRED_CLIENT_EMAIL'),
    client_secret['client_id'] = os.getenv ('GAPI_CRED_CLIENT_ID'),
    client_secret['auth_uri'] = os.getenv ('GAPI_CRED_AUTH_URI'),
    client_secret['token_uri'] = os.getenv ('GAPI_CRED_TOKEN_URI'),
    client_secret['auth_provider_x509_cert_url'] =  os.getenv ('GAPI_CRED_AUTH_PROVIDER_X509_CERT_URL'),
    client_secret['client_x509_cert_url'] = os.getenv ('GAPI_CRED_CLIENT_X509_CERT_URI'),
    json_data = json.dumps (client_secret)
    print(json_data)
    return json_data

def readGoogleApiSecretsDict():
    type = os.getenv ('GAPI_CRED_TYPE')
    project_id = os.getenv ('GAPI_CRED_PROJECT_ID')
    private_key_id =  os.getenv ('GAPI_CRED_PRIVATE_KEY_ID')
    private_key = os.getenv ('GAPI_CRED_PRIVATE_KEY')
    client_email = os.getenv ('GAPI_CRED_CLIENT_EMAIL')
    client_id = os.getenv ('GAPI_CRED_CLIENT_ID')
    auth_uri = os.getenv ('GAPI_CRED_AUTH_URI')
    token_uri = os.getenv ('GAPI_CRED_TOKEN_URI')
    auth_provider_x509_cert_url = os.getenv ('GAPI_CRED_AUTH_PROVIDER_X509_CERT_URL')
    client_x509_cert_url = os.getenv ('GAPI_CRED_CLIENT_X509_CERT_URI')

    secret = {
        'type' : type,
        'project_id' : project_id,
        'private_key_id' : private_key_id,
        'private_key':private_key,
        'client_email': client_email,
        'client_id': client_id,
        'auth_uri': auth_uri,
        'token_uri': token_uri,
        'auth_provider_x509_cert_url':auth_provider_x509_cert_url,
        'client_x509_cert_url':client_x509_cert_url
    }
    return secret

def subscribe(st_obj):
    st_obj.subheader ("Subscribe")
    email = st_obj.text_input (label="Enter Email", value="", key="na_lower_1")
    name = st_obj.text_input (label="Enter Name", value="", key="na_upper_1")
    affiliation = st_obj.text_input (label="Enter Affiliation", value="", key="na_upper_2")
    if st_obj.button (label="Submit", key="ta_submit_1"):
        row = [email, name, affiliation]
        send_subscription_to_google_sheet(st_obj, row)

def send_subscription_to_google_sheet(st_obj, row):
    json_secret = readGoogleApiSecretsDict()
    #print(json_secret)
    spr = spreadsheet(st_obj, json_secret)
    spr.writeToSheet("CHIME Form Submissions", row)

def display_footer(st):
    st.subheader("References & Acknowledgements")
    st.markdown(
        """* AHA Webinar, Feb 26, James Lawler, MD, an associate professor University of Nebraska Medical Center, What Healthcare Leaders Need To Know: Preparing for the COVID-19
* We would like to recognize the valuable assistance in consultation and review of model assumptions by Michael Z. Levy, PhD, Associate Professor of Epidemiology, Department of Biostatistics, Epidemiology and Informatics at the Perelman School of Medicine
* Finally we'd like to thank [Code for Philly](https://codeforphilly.org/) and the many members of the open-source community that [contributed](https://github.com/CodeForPhilly/chime/graphs/contributors) to this project.
    """
    )
    st.markdown("© 2020, The Trustees of the University of Pennsylvania")


def display_download_link(st, filename: str, df: pd.DataFrame):
    csv = dataframe_to_base64(df)
    st.markdown(
        """
        <a download="{filename}" href="data:file/csv;base64,{csv}">Download {filename}</a>
""".format(
            csv=csv, filename=filename
        ),
        unsafe_allow_html=True,
    )
