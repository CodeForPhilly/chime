import altair as alt
import numpy as np
import pandas as pd


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """


########
# Text #
########


def display_header(
    st,
    total_infections,
    initial_infections,
    detection_prob,
    current_hosp,
    hosp_rate,
    S,
    market_share,
    recovery_days,
    r_naught,
    doubling_time,
    relative_contact_rate,
    r_t,
    doubling_time_t,
):
    st.markdown(
        """
<link rel="stylesheet" href="https://www1.pennmedicine.org/styles/shared/penn-medicine-header.css">

<div class="penn-medicine-header__content">
    <a href="https://www.pennmedicine.org" class="penn-medicine-header__logo"
        title="Go to the Penn Medicine home page">Penn Medicine</a>
    <a id="title" class="penn-medicine-header__title">Penn Medicine - COVID-19 Hospital Impact Model for Epidemics</a>
</div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """*This tool was developed by the [Predictive Healthcare team](http://predictivehealthcare.pennmedicine.org/) at
    Penn Medicine. For questions and comments please see our
    [contact page](http://predictivehealthcare.pennmedicine.org/contact/). Code can be found on [Github](https://github.com/pennsignals/chime).
    Join our [Slack channel](https://codeforphilly.org/chat?channel=covid19-chime-penn) if you would like to get involved!*"""
    )

    st.markdown(
        """The estimated number of currently infected individuals is **{total_infections:.0f}**. The **{initial_infections}**
    confirmed cases in the region imply a **{detection_prob:.0%}** rate of detection. This is based on current inputs for
    Hospitalizations (**{current_hosp}**), Hospitalization rate (**{hosp_rate:.0%}**), Region size (**{S}**),
    and Hospital market share (**{market_share:.0%}**).

An initial doubling time of **{doubling_time}** days and a recovery time of **{recovery_days}** days imply an $R_0$ of
**{r_naught:.2f}**.

**Mitigation**: A **{relative_contact_rate:.0%}** reduction in social contact after the onset of the
outbreak reduces the doubling time to **{doubling_time_t:.1f}** days, implying an effective $R_t$ of **${r_t:.2f}$**.
""".format(
            total_infections=total_infections,
            initial_infections=initial_infections,
            detection_prob=detection_prob,
            current_hosp=current_hosp,
            hosp_rate=hosp_rate,
            S=S,
            market_share=market_share,
            recovery_days=recovery_days,
            r_naught=r_naught,
            doubling_time=doubling_time,
            relative_contact_rate=relative_contact_rate,
            r_t=r_t,
            doubling_time_t=doubling_time_t,
        )
    )

    return None


def show_more_info_about_this_tool(
    st,
    recovery_days,
    doubling_time,
    r_naught,
    relative_contact_rate,
    doubling_time_t,
    r_t,
    delaware,
    chester,
    montgomery,
    bucks,
    philly,
):
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
            recovery_days=int(recovery_days)
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
            doubling_time=doubling_time,
            recovery_days=recovery_days,
            r_naught=r_naught,
            relative_contact_rate=relative_contact_rate,
            doubling_time_t=doubling_time_t,
            r_t=r_t,
        )
    )
    st.latex("g = 2^{1/T_d} - 1")

    st.markdown(
        """
- Since the rate of new infections in the SIR model is $g = \\beta S - \\gamma$, and we've already computed $\\gamma$, $\\beta$ becomes a function of the initial population size of susceptible individuals.
$$\\beta = (g + \\gamma)$$.


### Initial Conditions

- The total size of the susceptible population will be the entire catchment area for Penn Medicine entities (HUP, PAH, PMC, CCH)
  - Delaware = {delaware}
  - Chester = {chester}
  - Montgomery = {montgomery}
  - Bucks = {bucks}
  - Philly = {philly}""".format(
            delaware=delaware,
            chester=chester,
            montgomery=montgomery,
            bucks=bucks,
            philly=philly,
        )
    )
    return None


def write_definitions(st):
    st.subheader("Guidance on Selecting Inputs")
    st.markdown(
        """* **Hospitalized COVID-19 Patients:** The number of patients currently hospitalized with COVID-19 **at your hospital(s)**. This number is used in conjunction with Hospital Market Share and Hospitalization % to estimate the total number of infected individuals in your region.
* **Doubling Time (days):** This parameter drives the rate of new cases during the early phases of the outbreak. The American Hospital Association currently projects doubling rates between 7 and 10 days. This is the doubling time you expect under status quo conditions. To account for reduced contact and other public health interventions, modify the _Social distancing_ input.
* **Social distancing (% reduction in person-to-person physical contact):** This parameter allows users to explore how reduction in interpersonal contact & transmission (hand-washing) might slow the rate of new infections. It is your estimate of how much social contact reduction is being achieved in your region relative to the status quo. While it is unclear how much any given policy might affect social contact (eg. school closures or remote work), this parameter lets you see how projections change with percentage reductions in social contact.
* **Hospitalization %(total infections):** Percentage of **all** infected cases which will need hospitalization.
* **ICU %(total infections):** Percentage of **all** infected cases which will need to be treated in an ICU.
* **Ventilated %(total infections):** Percentage of **all** infected cases which will need mechanical ventilation.
* **Hospital Length of Stay:** Average number of days of treatment needed for hospitalized COVID-19 patients.
* **ICU Length of Stay:** Average number of days of ICU treatment needed for ICU COVID-19 patients.
* **Vent Length of Stay:**  Average number of days of ventilation needed for ventilated COVID-19 patients.
* **Hospital Market Share (%):** The proportion of patients in the region that are likely to come to your hospital (as opposed to other hospitals in the region) when they get sick. One way to estimate this is to look at all of the hospitals in your region and add up all of the beds. The number of beds at your hospital divided by the total number of beds in the region times 100 will give you a reasonable starting estimate.
* **Regional Population:** Total population size of the catchment region of your hospital(s).
* **Currently Known Regional Infections**: The number of infections reported in your hospital's catchment region. This is only used to compute detection rate - **it will not change projections**. This input is used to estimate the detection rate of infected individuals.
    """
    )


def write_footer(st):
    st.subheader("References & Acknowledgements")
    st.markdown(
        """* AHA Webinar, Feb 26, James Lawler, MD, an associate professor University of Nebraska Medical Center, What Healthcare Leaders Need To Know: Preparing for the COVID-19
* We would like to recognize the valuable assistance in consultation and review of model assumptions by Michael Z. Levy, PhD, Associate Professor of Epidemiology, Department of Biostatistics, Epidemiology and Informatics at the Perelman School of Medicine
    """
    )
    st.markdown("© 2020, The Trustees of the University of Pennsylvania")


##########
# Charts #
##########


def new_admissions_chart(
    alt, projection_admits: pd.DataFrame, plot_projection_days: int
) -> alt.Chart:
    """docstring"""
    projection_admits = projection_admits.rename(
        columns={"hosp": "Hospitalized", "icu": "ICU", "vent": "Ventilated"}
    )
    return (
        alt.Chart(projection_admits.head(plot_projection_days))
        .transform_fold(fold=["Hospitalized", "ICU", "Ventilated"])
        .mark_line(point=True)
        .encode(
            x=alt.X("day", title="Days from today"),
            y=alt.Y("value:Q", title="Daily admissions"),
            color="key:N",
            tooltip=[
                "day",
                alt.Tooltip("value:Q", format=".0f", title="Admissions"),
                "key:N",
            ],
        )
        .interactive()
    )


def admitted_patients_chart(alt, census: pd.DataFrame) -> alt.Chart:
    """docstring"""
    census = census.rename(
        columns={
            "hosp": "Hospital Census",
            "icu": "ICU Census",
            "vent": "Ventilated Census",
        }
    )

    return (
        alt.Chart(census)
        .transform_fold(fold=["Hospital Census", "ICU Census", "Ventilated Census"])
        .mark_line(point=True)
        .encode(
            x=alt.X("day", title="Days from today"),
            y=alt.Y("value:Q", title="Census"),
            color="key:N",
            tooltip=[
                "day",
                alt.Tooltip("value:Q", format=".0f", title="Census"),
                "key:N",
            ],
        )
        .interactive()
    )


def additional_projections_chart(alt, i: np.ndarray, r: np.ndarray) -> alt.Chart:
    dat = pd.DataFrame({"Infected": i, "Recovered": r})

    return (
        alt.Chart(dat.reset_index())
        .transform_fold(fold=["Infected", "Recovered"])
        .mark_line()
        .encode(
            x=alt.X("index", title="Days from today"),
            y=alt.Y("value:Q", title="Case Volume"),
            tooltip=["key:N", "value:Q"],
            color="key:N",
        )
        .interactive()
    )


def show_additional_projections(st, alt, charting_func, i, r):
    st.subheader(
        "The number of infected and recovered individuals in the hospital catchment region at any given moment"
    )

    st.altair_chart(charting_func(alt, i, r), use_container_width=True)


##########
# Tables #
##########


def draw_projected_admissions_table(st, projection_admits: pd.DataFrame):
    admits_table = projection_admits[np.mod(projection_admits.index, 7) == 0].copy()
    admits_table["day"] = admits_table.index
    admits_table.index = range(admits_table.shape[0])
    admits_table = admits_table.fillna(0).astype(int)

    st.table(admits_table)
    return None


def draw_raw_sir_simulation_table(st, n_days, s, i, r):
    days = np.array(range(0, n_days + 1))
    data_list = [days, s, i, r]
    data_dict = dict(zip(["day", "susceptible", "infections", "recovered"], data_list))
    projection_area = pd.DataFrame.from_dict(data_dict)
    infect_table = (projection_area.iloc[::7, :]).apply(np.floor)
    infect_table.index = range(infect_table.shape[0])

    st.table(infect_table)
