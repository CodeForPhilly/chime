"""Streamlit display."""

import os
import json

from logging import INFO, basicConfig, getLogger
import pandas as pd
import i18n
from sys import stdout

from ..constants import (
    CHANGE_DATE,
    DOCS_URL,
    EPSILON,
    FLOAT_INPUT_MIN,
    FLOAT_INPUT_STEP,
    VERSION,
)
from ..model.parameters import Parameters, Disposition
from ..utils import (
    dataframe_to_base64,
    excel_to_base64,
)
from .spreadsheet import spreadsheet


basicConfig(
    level=INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=stdout,
)
logger = getLogger(__name__)


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
        i18n.t("presentation-infected-population-warning")
        if m.infected > p.population
        else ""
    )

    st.markdown(
        i18n.t("presentation-header"),
        unsafe_allow_html=True,
    )
    st.markdown(i18n.t("presentation-notice"))
    st.markdown(i18n.t("presentation-developed-by").format(
        docs_url=DOCS_URL))
    st.markdown(
        i18n.t("presentation-estimated-number-of-infection")
        .format(
            total_infections=m.infected,
            current_hosp=p.current_hospitalized,
            hosp_rate=p.hospitalized.rate,
            S=p.population,
            market_share=p.market_share,
            recovery_days=p.infectious_days,
            r_naught=m.r_naught,
            doubling_time=p.doubling_time,
            daily_growth=m.daily_growth_rate * 100.0,
            infected_population_warning_str=infected_population_warning_str,
            mitigation_str=(
                i18n.t("presentation-mitigation-rt-less-then-1")
                if m.r_t < 1
                else i18n.t("presentation-mitigation-rt-more-then-equal-1")
            ).format(
                relative_contact_rate=p.relative_contact_rate,
                doubling_time_t=abs(m.doubling_time_t),
                r_t=m.r_t,
                daily_growth_t=m.daily_growth_rate_t * 100.0,
            ),
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
    """
    Initializes the UI in the sidebar. These function calls create input elements, and bind the values they are set to
    to the appropriate variables. It's similar to Ember or Angular, if you are familiar with those frameworks.
    """

    st_obj = st.sidebar
    # used_widget_key = st.get_last_used_widget_key ( )

    current_hospitalized_input = NumberInput(
        st_obj,
        i18n.t("presentation-current-hospitalized"),
        min_value=0,
        value=d.current_hospitalized,
        step=1,
        format="%i",
    )
    n_days_input = NumberInput(
        st_obj,
        i18n.t("presentation-n-days"),
        min_value=1,
        max_value=30,
        value=d.n_days,
        step=1,
        format="%i",
    )
    doubling_time_input = NumberInput(
        st_obj,
        i18n.t("presentation-doubling-time"),
        min_value=0.5,
        value=d.doubling_time,
        step=0.25,
        format="%f",
    )
    current_date_input = DateInput(
        st_obj, i18n.t("presentation-current-date"), value=d.current_date,
    )
    date_first_hospitalized_input = DateInput(
        st_obj, i18n.t("presentation-date-first-hospitalized"),
        value=d.date_first_hospitalized,
    )
    mitigation_date_input = DateInput(
        st_obj, i18n.t("presentation-mitigation-date"),
        value=d.mitigation_date
    )
    relative_contact_pct_input = PercentInput(
        st_obj,
        i18n.t("presentation-relative-contact-rate"),
        min_value=0.0,
        max_value=100.0,
        value=d.relative_contact_rate,
        step=1.0,
    )
    hospitalized_pct_input = PercentInput(
        st_obj,
        i18n.t("presentation-hospitalized-rate"),
        value=d.hospitalized.rate,
        min_value=FLOAT_INPUT_MIN,
        max_value=100.0
    )
    icu_pct_input = PercentInput(
        st_obj,
        i18n.t("presentation-icu-rate"),
        min_value=0.0,
        value=d.icu.rate,
        step=0.05
    )
    ventilated_pct_input = PercentInput(
        st_obj, i18n.t("presentation-ventilated-rate"), value=d.ventilated.rate,
    )
    hospitalized_days_input = NumberInput(
        st_obj,
        i18n.t("presentation-hospitalized-days"),
        min_value=1,
        value=d.hospitalized.days,
        step=1,
        format="%i",
    )
    icu_days_input = NumberInput(
        st_obj,
        i18n.t("presentation-icu-days"),
        min_value=1,
        value=d.icu.days,
        step=1,
        format="%i",
    )
    ventilated_days_input = NumberInput(
        st_obj,
        i18n.t("presentation-ventilated-days"),
        min_value=1,
        value=d.ventilated.days,
        step=1,
        format="%i",
    )
    market_share_pct_input = PercentInput(
        st_obj,
        i18n.t("presentation-market-share"),
        min_value=0.5,
        value=d.market_share,
    )
    population_input = NumberInput(
        st_obj,
        i18n.t("presentation-population"),
        min_value=1,
        value=(d.population),
        step=1,
        format="%i",
    )
    infectious_days_input = NumberInput(
        st_obj,
        i18n.t("presentation-infectious-days"),
        min_value=1,
        value=d.infectious_days,
        step=1,
        format="%i",
    )
    max_y_axis_set_input = CheckboxInput(
        st_obj, i18n.t("presentation-max-y-axis-set")
    )
    max_y_axis_input = NumberInput(
        st_obj, i18n.t("presentation-max-y-axis"), value=500, format="%i", step=25
    )

    # Build in desired order
    st.sidebar.markdown(
        """**CHIME [{version}](https://github.com/CodeForPhilly/chime/releases/tag/{version}) ({change_date})**""".format(
            change_date=CHANGE_DATE,
            version=VERSION,
        )
    )

    st.sidebar.markdown(
        "### {hospital_parameters} [ℹ]({docs_url}/what-is-chime/parameters#hospital-parameters)".format(
            docs_url=DOCS_URL,
            hospital_parameters=i18n.t("presentation-hospital-parameters")
        )
    )
    population = population_input()
    market_share = market_share_pct_input()
    # known_infected = known_infected_input()
    current_hospitalized = current_hospitalized_input()

    st.sidebar.markdown(
        "### {spread_and_contact_parameters} [ℹ]({docs_url}/what-is-chime/parameters#spread-and-contact-parameters)".format(
            docs_url=DOCS_URL,
            spread_and_contact_parameters=i18n.t("presentation-spread-and-contact-parameters")
        )
    )

    if st.sidebar.checkbox(
        i18n.t("presentation-first-hospitalized-check")
    ):
        date_first_hospitalized = date_first_hospitalized_input()
        doubling_time = None
    else:
        doubling_time = doubling_time_input()
        date_first_hospitalized = None

    if st.sidebar.checkbox(
        i18n.t("presentation-social-distancing-implemented"),
        value=(d.relative_contact_rate > EPSILON)
    ):
        mitigation_date = mitigation_date_input()
        relative_contact_rate = relative_contact_pct_input()
    else:
        mitigation_date = None
        relative_contact_rate = EPSILON

    st.sidebar.markdown(
        "### {severity_parameters} [ℹ]({docs_url}/what-is-chime/parameters#severity-parameters)".format(
            docs_url=DOCS_URL,
            severity_parameters=i18n.t("presentation-severity-parameters")
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
        "### {display_parameters} [ℹ]({docs_url}/what-is-chime/parameters#display-parameters)".format(
            docs_url=DOCS_URL,
            display_parameters=i18n.t("presentation-display-parameters")
        )
    )
    n_days = n_days_input()
    max_y_axis_set = max_y_axis_set_input()

    max_y_axis = None
    if max_y_axis_set:
        max_y_axis = max_y_axis_input()

    current_date = current_date_input()
    use_log_scale = st.sidebar.checkbox(label=i18n.t("presentation-logarithmic-scale"), value=d.use_log_scale)

    # Subscribe implementation
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
        use_log_scale=use_log_scale
    )

# Read the environment variables and create json key object to use with ServiceAccountCredentials
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
    st_obj.subheader (i18n.t("presentation-subscribe"))
    email = st_obj.text_input (label=i18n.t("presentation-enter-email"), value="", key="na_lower_1")
    name = st_obj.text_input (label=i18n.t("presentation-enter-name"), value="", key="na_upper_1")
    affiliation = st_obj.text_input (label=i18n.t("presentation-enter-affiliation"), value="", key="na_upper_2")
    if st_obj.button (label=i18n.t("presentation-submit"), key="ta_submit_1"):
        row = [email, name, affiliation]
        send_subscription_to_google_sheet_secret_json(st_obj, row)

def send_subscription_to_google_sheet_secret_json(st_obj, row):
    json_secret = "/mnt/google-api-creds/client_secret.json"
    #print(json_secret)
    spr = spreadsheet (st_obj, json_secret)
    spr.writeToSheet("CHIME Form Submissions", row)

def send_subscription_to_google_sheet_secret_dict(st_obj, row):
    json_secret = readGoogleApiSecretsDict()
    #print(json_secret)
    spr = spreadsheet(st_obj, json_secret)
    spr.writeToSheet("CHIME Form Submissions", row)

def display_footer(st):
    st.subheader(i18n.t("presentation-references-acknowledgements"))
    st.markdown(
        i18n.t("presentation-references-acknowledgements-text")
    )
    st.markdown(i18n.t("presentation-copyright"))

def display_download_link(st, p, filename: str, df: pd.DataFrame):
    csv = dataframe_to_base64(df.rename(p.labels, axis=1))
    st.markdown(
        i18n.t("presentation-download").format(
            csv=csv, filename=filename
        ),
        unsafe_allow_html=True,
    )

def display_excel_download_link(st, filename: str, src: str):
    excel = excel_to_base64(src)
    st.markdown(
        i18n.t("presentation-excel-download").format(
            excel=excel, filename=filename
        ),
        unsafe_allow_html=True,
    )
