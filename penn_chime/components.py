import altair as alt
from penn_chime.presentation import new_admissions_chart
from penn_chime.models import get_hospitalizations, sim_sir
from penn_chime.utils import build_admissions_df

# TODO: this is python>=3.7, if we are targeting earlier versions we will need
#       this backport: https://github.com/ericvsmith/dataclasses
from dataclasses import dataclass

# UI ----------
@dataclass
class EstimateNewAdmissions:
    """Estimate new admissions based on model parameters.

    Examples:
      >>> EstimateNewAdmissions(
              n_days = 60,
              S = 4119405,
              current_hosp = 4,
              market_share = 15.0,
              hosp_rate = 5.0,
              icu_rate = 2.0,
              vent_rate = 1.0,
              doubling_time = 6,
              relative_contact_rate = 0
              )
              

    """
    n_days: int
    S: float
    current_hosp: float
    market_share: float
    hosp_rate: float
    icu_rate: float
    vent_rate: float
    doubling_time: float
    relative_contact_rate: float

    # params with defaults ----
    recovery_days: float = 14.0
    beta_decay: float = 0.0

    def plot_new_admissions(self):#, projection_admits, projection_days):
        total_infections = self.current_hosp / self.market_share / self.hosp_rate

        # TODO: are these usually derived? note sure why just renaming vars
        I, R = total_infections, 0

        # Note: could make a lot of these intermediate parameters properties
        #       maybe suffix with _ to make clear, since so many pars? (eg gamma_)
        intrinsic_growth_rate = 2 ** (1 / self.doubling_time) - 1

        gamma = 1 / self.recovery_days
        beta = (
            (intrinsic_growth_rate + gamma) / self.S * (1 - self.relative_contact_rate)
        )

        s, i, r = sim_sir(self.S, I, R, beta, gamma, self.n_days, beta_decay = self.beta_decay)
        hosp, icu, vent = get_hospitalizations(
                i,
                (self.hosp_rate, self.icu_rate, self.vent_rate),
                self.market_share
                )
        projection_admits = build_admissions_df(self.n_days, hosp, icu, vent)
        return new_admissions_chart(alt, projection_admits, self.n_days - 10) 


