"""effectful functions for streamlit io"""

from typing import Optional

import altair as alt  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from .defaults import Constants, RateLos
from .utils import add_date_column, dataframe_to_base64
from .parameters import Parameters

DATE_FORMAT = "%b, %d"  # see https://strftime.org
DOCS_URL = "https://code-for-philly.gitbook.io/chime"

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """


########
# Text #
########


def display_header(st, m, p):

    detection_prob_str = (
        "{detection_prob:.0%}".format(detection_prob=m.detection_probability)
        if m.detection_probability
        else "unknown"
    )

    infection_warning_str = (
        """(Warning: The number of known infections is greater than the estimate of infected patients based on inputs for current hospitalization, market share, and hospitalization rate. Please verify the market share value in the sidebar, and see if the hospitalization rate needs to be lowered.)"""
        if p.known_infected > m.infected
        else ""
    )

    infected_population_warning_str = (
        """(Warning: The number of estimated infections is greater than the total regional population. Please verify the values entered in the sidebar.)"""
        if m.infected > p.susceptible
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
        """[Documentation](https://code-for-philly.gitbook.io/chime/) | [Github](https://github.com/CodeForPhilly/chime/) | [Slack](https://codeforphilly.org/chat?channel=covid19-chime-penn)"""
    )
    st.markdown(
        """**IMPORTANT NOTICE**: Admissions and Census calculations were previously **undercounting**. Please update your reports generated before """ + p.change_date() + """. See more about changes [here](https://github.com/CodeForPhilly/chime/labels/models)."""
    )
    st.markdown(
        """*This tool was developed by the [Predictive Healthcare team](http://predictivehealthcare.pennmedicine.org/) at
    Penn Medicine to assist hospitals and public health officials with hospital capacity planning, 
    but can be used anywhere in the world. 
    Customize it for your region by modifying data inputs in the left panel.
    For questions on how to use this tool see the [User docs]({docs_url}). Code can be found on [Github](https://github.com/CodeForPhilly/chime)*.
    """.format(docs_url=DOCS_URL)
    )

    st.markdown(
        """The estimated number of currently infected individuals is **{total_infections:.0f}**. The **{initial_infections}**
    confirmed cases in the region imply a **{detection_prob_str}** rate of detection. This is based on current inputs for
    Hospitalizations (**{current_hosp}**), Hospitalization rate (**{hosp_rate:.0%}**), Region size (**{S}**),
    and Hospital market share (**{market_share:.0%}**).
    
{infection_warning_str} 
{infected_population_warning_str}

An initial doubling time of **{doubling_time}** days and a recovery time of **{recovery_days}** days imply an $R_0$ of
 **{r_naught:.2f}** and daily growth rate of **{daily_growth:.2f}%**. 
 
**Mitigation**: A **{relative_contact_rate:.0%}** reduction in social contact after the onset of the
outbreak **{impact_statement:s} {doubling_time_t:.1f}** days, implying an effective $R_t$ of **${r_t:.2f}$** 
and daily growth rate of **{daily_growth_t:.2f}%**.
""".format(
            total_infections=m.infected,
            initial_infections=p.known_infected,
            detection_prob_str=detection_prob_str,
            current_hosp=p.current_hospitalized,
            hosp_rate=p.hospitalized.rate,
            S=p.susceptible,
            market_share=p.market_share,
            recovery_days=p.recovery_days,
            r_naught=m.r_naught,
            doubling_time=p.doubling_time,
            relative_contact_rate=p.relative_contact_rate,
            r_t=m.r_t,
            doubling_time_t=abs(m.doubling_time_t),
            impact_statement=("halves the infections every" if m.r_t < 1 else "reduces the doubling time to"),
            daily_growth=m.daily_growth,
            daily_growth_t=m.daily_growth_t,
            docs_url=DOCS_URL,
            infection_warning_str=infection_warning_str,
            infected_population_warning_str=infected_population_warning_str
        )
    )

    return None


class InputWrapper:
    """Helper to separate Streamlit input definition from creation/rendering"""
    def __init__(self, st_obj, label, value, kwargs):
        self.st_obj = st_obj
        self.label = label
        self.value = value
        self.kwargs = kwargs

    def build(self):
        return self.st_obj(self.label, value=self.value, **self.kwargs)


class NumberInputWrapper(InputWrapper):
    def __init__(self, st_obj, label, min_value=None, max_value=None, value=None, step=None, format=None, key=None):
        kwargs = dict(min_value=min_value, max_value=max_value, step=step, format=format, key=key)
        super().__init__(st_obj.number_input, label, value, kwargs)


class CheckboxWrapper(InputWrapper):
    def __init__(self, st_obj, label, value=None, key=None):
        kwargs = dict(key=key)
        super().__init__(st_obj.checkbox, label, value, kwargs)


def display_sidebar(st, d: Constants) -> Parameters:
    # Initialize variables
    # these functions create input elements and bind the values they are set to
    # to the variables they are set equal to
    # it's kindof like ember or angular if you are familiar with those

    if d.known_infected < 1:
        raise ValueError("Known cases must be larger than one to enable predictions.")
    st_obj = st.sidebar
    current_hospitalized = NumberInputWrapper(
        st_obj,
        "Currently Hospitalized COVID-19 Patients",
        min_value=0,
        value=d.current_hospitalized,
        step=1,
        format="%i",
    )
    n_days = NumberInputWrapper(
        st_obj,
        "Number of days to project",
        min_value=30,
        value=d.n_days,
        step=10,
        format="%i",
    )
    doubling_time = NumberInputWrapper(
        st_obj,
        "Doubling time before social distancing (days)",
        min_value=0,
        value=d.doubling_time,
        step=1,
        format="%i",
    )
    relative_contact_rate = NumberInputWrapper(
        st_obj,
        "Social distancing (% reduction in social contact)",
        min_value=0,
        max_value=100,
        value=int(d.relative_contact_rate * 100),
        step=5,
        format="%i",
    )
    hospitalized_rate = NumberInputWrapper(
        st_obj,
        "Hospitalization %(total infections)",
        min_value=0.001,
        max_value=100.0,
        value=d.hospitalized.rate * 100,
        step=1.0,
        format="%f",
    )
    icu_rate = NumberInputWrapper(
        st_obj,
        "ICU %(total infections)",
        min_value=0.0,
        max_value=100.0,
        value=d.icu.rate * 100,
        step=1.0,
        format="%f",
    )
    ventilated_rate = NumberInputWrapper(
        st_obj,
        "Ventilated %(total infections)",
        min_value=0.0,
        max_value=100.0,
        value=d.ventilated.rate * 100,
        step=1.0,
        format="%f",
    )
    hospitalized_los = NumberInputWrapper(
        st_obj,
        "Hospital Length of Stay",
        min_value=0,
        value=d.hospitalized.length_of_stay,
        step=1,
        format="%i",
    )
    icu_los = NumberInputWrapper(
        st_obj,
        "ICU Length of Stay",
        min_value=0,
        value=d.icu.length_of_stay,
        step=1,
        format="%i",
    )
    ventilated_los = NumberInputWrapper(
        st_obj,
        "Vent Length of Stay",
        min_value=0,
        value=d.ventilated.length_of_stay,
        step=1,
        format="%i",
    )
    market_share = NumberInputWrapper(
        st_obj,
        "Hospital Market Share (%)",
        min_value=0.001,
        max_value=100.0,
        value=d.market_share * 100,
        step=1.0,
        format="%f",
    )
    susceptible = NumberInputWrapper(
        st_obj,
        "Regional Population",
        min_value=1,
        value=d.region.susceptible,
        step=100000,
        format="%i",
    )
    known_infected = NumberInputWrapper(
        st_obj,
        "Currently Known Regional Infections (only used to compute detection rate - does not change projections)",
        min_value=0,
        value=d.known_infected,
        step=10,
        format="%i",
    )
    as_date = CheckboxWrapper(st_obj, "Present result as dates instead of days", value=False)
    max_y_axis_set = CheckboxWrapper(st_obj, "Set the Y-axis on graphs to a static value")

    max_y_axis = None
    if max_y_axis_set:
        max_y_axis = NumberInputWrapper(st_obj, "Y-axis static value", value=500, format="%i", step=25)

    # Build in desired order
    st.sidebar.markdown("### Regional Parameters [ℹ]({docs_url}/what-is-chime/parameters)".format(docs_url=DOCS_URL))
    susceptible.build()
    market_share.build()
    known_infected.build()
    current_hospitalized.build()

    st.sidebar.markdown("### Spread and Contact Parameters [ℹ]({docs_url}/what-is-chime/parameters)"
                        .format(docs_url=DOCS_URL))
    doubling_time.build()
    relative_contact_rate.build()

    st.sidebar.markdown("### Severity Parameters [ℹ]({docs_url}/what-is-chime/parameters)".format(docs_url=DOCS_URL))
    hospitalized_rate.build()
    icu_rate.build()
    ventilated_rate.build()
    hospitalized_los.build()
    icu_los.build()
    ventilated_los.build()

    st.sidebar.markdown("### Display Parameters [ℹ]({docs_url}/what-is-chime/parameters)".format(docs_url=DOCS_URL))
    n_days.build()
    max_y_axis.build()
    as_date.build()

    return Parameters(
        as_date=as_date.value,
        current_hospitalized=current_hospitalized.value,
        market_share=market_share.value,
        known_infected=known_infected.value,
        doubling_time=doubling_time.value,

        max_y_axis=max_y_axis.value,
        n_days=n_days.value,
        relative_contact_rate=relative_contact_rate.value / 100.0,
        susceptible=susceptible.value,

        hospitalized=RateLos(hospitalized_rate.value / 100.0, hospitalized_los.value),
        icu=RateLos(icu_rate.value / 100.0, icu_los.value),
        ventilated=RateLos(ventilated_rate.value / 100.0, ventilated_los.value),
    )


def show_more_info_about_this_tool(st, model, parameters, defaults, notes: str = ""):
    """a lot of streamlit writing to screen."""
    st.subheader(
        "[Discrete-time SIR modeling](https://mathworld.wolfram.com/SIRModel.html) of infections/recovery"
    )
    st.markdown(
        """The model consists of individuals who are either _Susceptible_ ($S$), _Infected_ ($I$), or _Recovered_ ($R$).

The epidemic proceeds via a growth and decline process. This is the core model of infectious disease spread and has been in use in epidemiology for many years."""
    )
    st.markdown("""The dynamics are given by the following 3 equations.""")

    st.latex("S_{t+1} = (-\\beta S_t I_t) + S_t")
    st.latex("I_{t+1} = (\\beta S_t I_t - \\gamma I_t) + I_t")
    st.latex("R_{t+1} = (\\gamma I_t) + R_t")

    st.markdown(
        """To project the expected impact to Penn Medicine, we estimate the terms of the model.

To do this, we use a combination of estimates from other locations, informed estimates based on logical reasoning, and best guesses from the American Hospital Association.


### Parameters

The model's parameters, $\\beta$ and $\\gamma$, determine the virulence of the epidemic.

$$\\beta$$ can be interpreted as the _effective contact rate_:
"""
    )
    st.latex("\\beta = \\tau \\times c")

    st.markdown(
        """which is the transmissibility ($\\tau$) multiplied by the average number of people exposed ($$c$$).  The transmissibility is the basic virulence of the pathogen.  The number of people exposed $c$ is the parameter that can be changed through social distancing.


$\\gamma$ is the inverse of the mean recovery time, in days.  I.e.: if $\\gamma = 1/{recovery_days}$, then the average infection will clear in {recovery_days} days.

An important descriptive parameter is the _basic reproduction number_, or $R_0$.  This represents the average number of people who will be infected by any given infected person.  When $R_0$ is greater than 1, it means that a disease will grow.  Higher $R_0$'s imply more rapid growth.  It is defined as """.format(
            recovery_days=int(parameters.recovery_days)
        )
    )
    st.latex("R_0 = \\beta /\\gamma")

    st.markdown(
        """

$R_0$ gets bigger when

- there are more contacts between people
- when the pathogen is more virulent
- when people have the pathogen for longer periods of time

A doubling time of {doubling_time} days and a recovery time of {recovery_days} days imply an $R_0$ of {r_naught:.2f}.

#### Effect of social distancing

After the beginning of the outbreak, actions to reduce social contact will lower the parameter $c$.  If this happens at
time $t$, then the number of people infected by any given infected person is $R_t$, which will be lower than $R_0$.

A {relative_contact_rate:.0%} reduction in social contact would increase the time it takes for the outbreak to double,
to {doubling_time_t:.2f} days from {doubling_time:.2f} days, with a $R_t$ of {r_t:.2f}.

#### Using the model

We need to express the two parameters $\\beta$ and $\\gamma$ in terms of quantities we can estimate.

- $\\gamma$:  the CDC is recommending 14 days of self-quarantine, we'll use $\\gamma = 1/{recovery_days}$.
- To estimate $$\\beta$$ directly, we'd need to know transmissibility and social contact rates.  since we don't know these things, we can extract it from known _doubling times_.  The AHA says to expect a doubling time $T_d$ of 7-10 days. That means an early-phase rate of growth can be computed by using the doubling time formula:
""".format(
            doubling_time=parameters.doubling_time,
            recovery_days=parameters.recovery_days,
            r_naught=model.r_naught,
            relative_contact_rate=parameters.relative_contact_rate,
            doubling_time_t=model.doubling_time_t,
            r_t=model.r_t,
        )
    )
    st.latex("g = 2^{1/T_d} - 1")

    st.markdown(
        """
- Since the rate of new infections in the SIR model is $g = \\beta S - \\gamma$, and we've already computed $\\gamma$, $\\beta$ becomes a function of the initial population size of susceptible individuals.
$$\\beta = (g + \\gamma)$$.


### Initial Conditions

- {notes} \n
""".format(
            notes=notes
        )
        + "- "
        + "| \n".join(
            f"{key} = {value} "
            for key, value in defaults.region.__dict__.items()
            if key != "_s"
        )
    )
    return None


def write_definitions(st):
    st.subheader("Guidance on Selecting Inputs")
    st.markdown(
        """**This information has been moved to the 
[User Documentation]({docs_url}/what-is-chime/parameters#guidance-on-selecting-inputs)**""".format(docs_url=DOCS_URL)
    )


def write_footer(st):
    st.subheader("References & Acknowledgements")
    st.markdown(
        """* AHA Webinar, Feb 26, James Lawler, MD, an associate professor University of Nebraska Medical Center, What Healthcare Leaders Need To Know: Preparing for the COVID-19
* We would like to recognize the valuable assistance in consultation and review of model assumptions by Michael Z. Levy, PhD, Associate Professor of Epidemiology, Department of Biostatistics, Epidemiology and Informatics at the Perelman School of Medicine
    """
    )
    st.markdown("© 2020, The Trustees of the University of Pennsylvania")


def show_additional_projections(
    st, alt, charting_func, model, parameters
):
    st.subheader(
        "The number of infected and recovered individuals in the hospital catchment region at any given moment"
    )

    st.altair_chart(
        charting_func(
            alt,
            model=model,
            parameters=parameters
        ),
        use_container_width=True,
    )


##########
# Tables #
##########


def draw_projected_admissions_table(
    st, projection_admits: pd.DataFrame, labels, day_range, as_date: bool = False
):
    admits_table = projection_admits[np.mod(projection_admits.index, day_range) == 0].copy()
    admits_table["day"] = admits_table.index
    admits_table.index = range(admits_table.shape[0])
    admits_table = admits_table.fillna(0).astype(int)

    if as_date:
        admits_table = add_date_column(
            admits_table, drop_day_column=True, date_format=DATE_FORMAT
        )
    admits_table.rename(labels)
    st.table(admits_table)
    return None


def draw_census_table(st, census_df: pd.DataFrame, labels, day_range, as_date: bool = False):
    census_table = census_df[np.mod(census_df.index, day_range) == 0].copy()
    census_table.index = range(census_table.shape[0])
    census_table.loc[0, :] = 0
    census_table = census_table.dropna().astype(int)

    if as_date:
        census_table = add_date_column(
            census_table, drop_day_column=True, date_format=DATE_FORMAT
        )

    census_table.rename(labels)
    st.table(census_table)
    return None


def draw_raw_sir_simulation_table(st, model, parameters):
    as_date = parameters.as_date
    projection_area = model.raw_df
    infect_table = (projection_area.iloc[::7, :]).apply(np.floor)
    infect_table.index = range(infect_table.shape[0])
    infect_table["day"] = infect_table.day.astype(int)

    if as_date:
        infect_table = add_date_column(
            infect_table, drop_day_column=True, date_format=DATE_FORMAT
        )

    st.table(infect_table)
    build_download_link(st,
        filename="raw_sir_simulation_data.csv",
        df=projection_area,
        parameters=parameters
    )

def build_download_link(st, filename: str, df: pd.DataFrame, parameters: Parameters):
    if parameters.as_date:
        df = add_date_column(df, drop_day_column=True, date_format="%Y-%m-%d")

    csv = dataframe_to_base64(df)
    st.markdown("""
        <a download="{filename}" href="data:file/csv;base64,{csv}">Download full table as CSV</a>
""".format(csv=csv,filename=filename), unsafe_allow_html=True)
