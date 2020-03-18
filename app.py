from functools import reduce
from typing import Tuple, Dict, Any
import pandas as pd
import streamlit as st
import numpy as np
import altair as alt

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

delaware = 564696
chester = 519293
montgomery = 826075
bucks = 628341
philly = 1581000
S_default = delaware + chester + montgomery + bucks + philly
known_infections = 63 # update daily
known_cases = 4 # update daily

# Widgets
current_hosp = st.sidebar.number_input(
    "Currently Hospitalized COVID-19 Patients", value=known_cases, step=1, format="%i"
)
initial_infections = st.sidebar.number_input(
    "Currently Known Regional Infections", value=known_infections, step=10, format="%i"
)
doubling_time = st.sidebar.number_input(
    "Doubling time before social distancing (days)", value=6, step=1, format="%i"
)
relative_contact_rate = st.sidebar.number_input(
    "Social distancing (% reduction in social contact)", 0, 100, value=0, step=5, format="%i"
)/100.0

hosp_rate = (
    st.sidebar.number_input("Hospitalization %(total infections)", 0, 100, value=5, step=1, format="%i")
    / 100.0
)
icu_rate = (
    st.sidebar.number_input("ICU %(total infections)", 0, 100, value=2, step=1, format="%i") / 100.0
)
vent_rate = (
    st.sidebar.number_input("Ventilated %(total infections)", 0, 100, value=1, step=1, format="%i")
    / 100.0
)
hosp_los = st.sidebar.number_input("Hospital Length of Stay", value=7, step=1, format="%i")
icu_los = st.sidebar.number_input("ICU Length of Stay", value=9, step=1, format="%i")
vent_los = st.sidebar.number_input("Vent Length of Stay", value=10, step=1, format="%i")
Penn_market_share = (
    st.sidebar.number_input(
        "Hospital Market Share (%)", 0.0, 100.0, value=15.0, step=1.0, format="%f"
    )
    / 100.0
)
S = st.sidebar.number_input(
    "Regional Population", value=S_default, step=100000, format="%i"
)

total_infections = current_hosp / Penn_market_share / hosp_rate
detection_prob = initial_infections / total_infections

S, I, R = S, initial_infections / detection_prob, 0

intrinsic_growth_rate = 2 ** (1 / doubling_time) - 1

recovery_days = 14.0
# mean recovery rate, gamma, (in 1/days).
gamma = 1 / recovery_days

# Contact rate, beta
beta = (
    intrinsic_growth_rate + gamma
) / S * (1-relative_contact_rate) # {rate based on doubling time} / {initial S}

r_t = beta / gamma * S # r_t is r_0 after distancing
r_naught = r_t / (1-relative_contact_rate)
doubling_time_t = 1/np.log2(beta*S - gamma +1) # doubling time after distancing

st.title("COVID-19 Hospital Impact Model for Epidemics")
st.markdown(
    """*This tool was developed by the [Predictive Healthcare team](http://predictivehealthcare.pennmedicine.org/) at
Penn Medicine. For questions and comments please see our
[contact page](http://predictivehealthcare.pennmedicine.org/contact/). Code can be found on [Github](https://github.com/pennsignals/chime).
Join our [Slack channel](https://codeforphilly.org/chat?channel=covid19-chime-penn) if you would like to get involved!*""")

st.markdown(
    """The estimated number of currently infected individuals is **{total_infections:.0f}**. The **{initial_infections}** 
confirmed cases in the region imply a **{detection_prob:.0%}** rate of detection. This is based on current inputs for 
Hospitalizations (**{current_hosp}**), Hospitalization rate (**{hosp_rate:.0%}**), Region size (**{S}**), 
and Hospital market share (**{Penn_market_share:.0%}**).

An initial doubling time of **{doubling_time}** days and a recovery time of **{recovery_days}** days imply an $R_0$ of 
**{r_naught:.2f}**.

**Mitigation**: A **{relative_contact_rate:.0%}** reduction in social contact after the onset of the 
outbreak reduces the doubling time to **{doubling_time_t:.1f}** days, implying an effective $R_t$ of **${r_t:.2f}$**.
""".format(
        total_infections=total_infections,
        current_hosp=current_hosp,
        hosp_rate=hosp_rate,
        S=S,
        Penn_market_share=Penn_market_share,
        initial_infections=initial_infections,
        detection_prob=detection_prob,
        recovery_days=recovery_days,
        r_naught=r_naught,
        doubling_time=doubling_time,
        relative_contact_rate=relative_contact_rate,
        r_t=r_t,
        doubling_time_t=doubling_time_t
    )
)




if st.checkbox("Show more info about this tool"):
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
""")
    st.latex("\\beta = \\tau \\times c")

    st.markdown(
"""which is the transmissibility ($\\tau$) multiplied by the average number of people exposed ($$c$$).  The transmissibility is the basic virulence of the pathogen.  The number of people exposed $c$ is the parameter that can be changed through social distancing.


$\\gamma$ is the inverse of the mean recovery time, in days.  I.e.: if $\\gamma = 1/{recovery_days}$, then the average infection will clear in {recovery_days} days.

An important descriptive parameter is the _basic reproduction number_, or $R_0$.  This represents the average number of people who will be infected by any given infected person.  When $R_0$ is greater than 1, it means that a disease will grow.  Higher $R_0$'s imply more rapid growth.  It is defined as """.format(recovery_days=int(recovery_days)    , c='c'))
    st.latex("R_0 = \\beta /\\gamma")

    st.markdown("""

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
""".format(doubling_time=doubling_time,
           recovery_days=recovery_days,
           r_naught=r_naught,
           relative_contact_rate=relative_contact_rate,
           doubling_time_t=doubling_time_t,
           r_t=r_t)
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

# The SIR model, one time step
def sir(y, beta, gamma, N):
    S, I, R = y
    Sn = (-beta * S * I) + S
    In = (beta * S * I - gamma * I) + I
    Rn = gamma * I + R
    if Sn < 0:
        Sn = 0
    if In < 0:
        In = 0
    if Rn < 0:
        Rn = 0

    scale = N / (Sn + In + Rn)
    return Sn * scale, In * scale, Rn * scale


# Run the SIR model forward in time
def sim_sir(S, I, R, beta, gamma, n_days, beta_decay=None):
    N = S + I + R
    s, i, r = [S], [I], [R]
    for day in range(n_days):
        y = S, I, R
        S, I, R = sir(y, beta, gamma, N)
        if beta_decay:
            beta = beta * (1 - beta_decay)
        s.append(S)
        i.append(I)
        r.append(R)

    s, i, r = np.array(s), np.array(i), np.array(r)
    return s, i, r


n_days = st.slider("Number of days to project", 30, 200, 60, 1, "%i")

beta_decay = 0.0
s, i, r = sim_sir(S, I, R, beta, gamma, n_days, beta_decay=beta_decay)


hosp = i * hosp_rate * Penn_market_share
icu = i * icu_rate * Penn_market_share
vent = i * vent_rate * Penn_market_share

days = np.array(range(0, n_days + 1))
data_list = [days, hosp, icu, vent]
data_dict = dict(zip(["day", "hosp", "icu", "vent"], data_list))

projection = pd.DataFrame.from_dict(data_dict)

st.subheader("New Admissions")
st.markdown("Projected number of **daily** COVID-19 admissions at Penn hospitals")

# New cases
projection_admits = projection.iloc[:-1, :] - projection.shift(1)
projection_admits[projection_admits < 0] = 0

plot_projection_days = n_days - 10
projection_admits["day"] = range(projection_admits.shape[0])


def new_admissions_chart(projection_admits: pd.DataFrame, plot_projection_days: int) -> alt.Chart:
    """docstring"""
    projection_admits = projection_admits.rename(columns={"hosp": "Hospitalized", "icu": "ICU", "vent": "Ventilated"})
    return (
        alt
        .Chart(projection_admits.head(plot_projection_days))
        .transform_fold(fold=["Hospitalized", "ICU", "Ventilated"])
        .mark_line(point=True)
        .encode(
            x=alt.X("day", title="Days from today"),
            y=alt.Y("value:Q", title="Daily admissions"),
            color="key:N",
            tooltip=["day", "key:N"]
        )
        .interactive()
    )

st.altair_chart(new_admissions_chart(projection_admits, plot_projection_days), use_container_width=True)


admits_table = projection_admits[np.mod(projection_admits.index, 7) == 0].copy()
admits_table["day"] = admits_table.index
admits_table.index = range(admits_table.shape[0])
admits_table = admits_table.fillna(0).astype(int)

if st.checkbox("Show Projected Admissions in tabular form"):
    st.dataframe(admits_table)

st.subheader("Admitted Patients (Census)")
st.markdown(
    "Projected **census** of COVID-19 patients, accounting for arrivals and discharges at Penn hospitals"
)

# ALOS for each category of COVID-19 case (total guesses)

los_dict = {
    "hosp": hosp_los,
    "icu": icu_los,
    "vent": vent_los,
}

census_dict = dict()
for k, los in los_dict.items():
    census = (
        projection_admits.cumsum().iloc[:-los, :]
        - projection_admits.cumsum().shift(los).fillna(0)
    ).apply(np.ceil)
    census_dict[k] = census[k]


census_df = pd.DataFrame(census_dict)
census_df["day"] = census_df.index
census_df = census_df[["day", "hosp", "icu", "vent"]]

census_table = census_df[np.mod(census_df.index, 7) == 0].copy()
census_table.index = range(census_table.shape[0])
census_table.loc[0, :] = 0
census_table = census_table.dropna().astype(int)

def admitted_patients_chart(census: pd.DataFrame) -> alt.Chart:
    """docstring"""
    census = census.rename(columns={"hosp": "Hospital Census", "icu": "ICU Census", "vent": "Ventilated Census"})

    return (
        alt
        .Chart(census)
        .transform_fold(fold=["Hospital Census", "ICU Census", "Ventilated Census"])
        .mark_line(point=True)
        .encode(
            x=alt.X("day", title="Days from today"),
            y=alt.Y("value:Q", title="Census"),
            color="key:N",
            tooltip=["day", "key:N"]
        )
        .interactive()
    )

st.altair_chart(admitted_patients_chart(census_table), use_container_width=True)

if st.checkbox("Show Projected Census in tabular form"):
    st.dataframe(census_table)

st.markdown(
    """**Click the checkbox below to view additional data generated by this simulation**"""
)
if st.checkbox("Show Additional Projections"):
    st.subheader(
        "The number of infected and recovered individuals in the hospital catchment region at any given moment"
    )

    def additional_projections_chart(i: np.ndarray, r: np.ndarray) -> alt.Chart:
        dat = pd.DataFrame({"Infected": i, "Recovered": r})

        return (
            alt
            .Chart(dat.reset_index())
            .transform_fold(fold=["Infected", "Recovered"])
            .mark_line()
            .encode(
                x=alt.X("index", title="Days from today"),
                y=alt.Y("value:Q", title="Case Volume"),
                tooltip=["key:N", "value:Q"],
                color="key:N"
            )
            .interactive()
        )

    st.altair_chart(additional_projections_chart(i, r), use_container_width=True)

    # Show data
    days = np.array(range(0, n_days + 1))
    data_list = [days, s, i, r]
    data_dict = dict(zip(["day", "susceptible", "infections", "recovered"], data_list))
    projection_area = pd.DataFrame.from_dict(data_dict)
    infect_table = (projection_area.iloc[::7, :]).apply(np.floor)
    infect_table.index = range(infect_table.shape[0])

    if st.checkbox("Show Raw SIR Similation Data"):
        st.dataframe(infect_table)

st.subheader("Guidance on Selecting Inputs")
st.markdown(
    """* **Hospitalized COVID-19 Patients:** The number of patients currently hospitalized with COVID-19. This number is used in conjunction with Hospital Market Share and Hospitalization % to estimate the total number of infected individuals in your region.
* **Currently Known Regional Infections**: The number of infections reported in your hospital's catchment region. This input is used to estimate the detection rate of infected individuals. 
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
    """
)


st.subheader("References & Acknowledgements")
st.markdown(
    """* AHA Webinar, Feb 26, James Lawler, MD, an associate professor University of Nebraska Medical Center, What Healthcare Leaders Need To Know: Preparing for the COVID-19
* We would like to recognize the valuable assistance in consultation and review of model assumptions by Michael Z. Levy, PhD, Associate Professor of Epidemiology, Department of Biostatistics, Epidemiology and Informatics at the Perelman School of Medicine
    """
)
st.markdown("© 2020, The Trustees of the University of Pennsylvania")
