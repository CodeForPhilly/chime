import json
import io
from typing import Tuple

from .defaults import (
    Constants, 
    Regions, 
    RateLos,
)


def constants_from_uploaded_file(file: io.StringIO) -> Tuple[Constants, dict]:
    imported_params = json.loads(file.read())
    constants = Constants(
        region=Regions(area=imported_params["RegionalPopulation"]),
        current_hospitalized=imported_params["CurrentlyHospitalizedCovidPatients"],
        doubling_time=imported_params["DoublingTimeBeforeSocialDistancing"],
        known_infected=imported_params["CurrentlyKnownRegionalInfections"],
        n_days=imported_params["NumberOfDaysToProject"],
        market_share=float(imported_params["HospitalMarketShare"]),
        relative_contact_rate=imported_params["SocialDistancingPercentReduction"],
        hospitalized=RateLos(float(imported_params["HospitalizationPercentage"]), 7),
        icu=RateLos(float(imported_params["ICUPercentage"]), 9),
        ventilated=RateLos(float(imported_params["VentilatedPercentage"]), 10),
    )
    return constants, imported_params
