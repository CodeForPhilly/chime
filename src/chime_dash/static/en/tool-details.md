## [Discrete-time SIR modeling](https://mathworld.wolfram.com/SIRModel.html) of infections/recovery

The model consists of individuals who are either _Susceptible_ ($S$), _Infected_ ($I$), or _Recovered_ ($R$).

The epidemic proceeds via a growth and decline process. This is the core model of infectious disease spread and has been in use in epidemiology for many years.

The dynamics are given by the following 3 equations.

$$S_{{t+1}}  = (-\\beta S_t I_t) + S_t$$

$$"I_{{t+1}} = (\\beta S_t I_t - \\gamma I_t) + I_t$$

$$R_{{t+1}}  = (\\gamma I_t) + R_t$$

To project the expected impact to Penn Medicine, we estimate the terms of the model.

To do this, we use a combination of estimates from other locations, informed estimates based on logical reasoning, and best guesses from the American Hospital Association.

### Parameters

The model's parameters, $\\beta$ and $\\gamma$, determine the virulence of the epidemic.

$$\\beta$$ can be interpreted as the _effective contact rate_:
$$\\beta = \\tau \\times c$$

"which is the transmissibility ($\\tau$) multiplied by the average number of people exposed ($$c$$).  The transmissibility is the basic virulence of the pathogen.  The number of people exposed $c$ is the parameter that can be changed through social distancing.

$\\gamma$ is the inverse of the mean recovery time, in days.  I.e.: if $\\gamma = 1/{recovery_days}$, then the average infection will clear in {recovery_days} days.

An important descriptive parameter is the _basic reproduction number_, or $R_0$.  This represents the average number of people who will be infected by any given infected person.  When $R_0$ is greater than 1, it means that a disease will grow.  Higher $R_0$'s imply more rapid growth.  It is defined as
$$R_0 = \\beta /\\gamma$$

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
$g = 2^{{1/T_d}} - 1$
- Since the rate of new infections in the SIR model is $g = \\beta S - \\gamma$, and we've already computed $\\gamma$, $\\beta$ becomes a function of the initial population size of susceptible individuals.
$$\\beta = (g + \\gamma)$$.


### Initial Conditions

- The total size of the susceptible population will be the entire catchment area for Penn Medicine entities (HUP, PAH, PMC, CCH)
{regions}
