import base64
from datetime import datetime
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
        relative_contact_rate=float(imported_params["SocialDistancingPercentReduction"]),
        hospitalized=RateLos(float(imported_params["HospitalizationPercentage"]), imported_params["HospitalLengthOfStay"]),
        icu=RateLos(float(imported_params["ICUPercentage"]), imported_params["ICULengthOfStay"]),
        ventilated=RateLos(float(imported_params["VentilatedPercentage"]),imported_params["VentLengthOfStay"]),
    )
    return constants, imported_params

def param_download_widget(st, parameters, as_date, max_y_axis_set, max_y_axis):
    if parameters.author == "Jane Doe" or parameters.scenario == "COVID Model":
        st.sidebar.markdown("""
        **Enter a unique author name and scenario name to enable parameter download.**""")
    else:
        filename = "ModelParameters" + "_" + parameters.author + "_" + parameters.scenario + "_" + datetime.now().isoformat() + ".json"
        out_obj = {
            "Author": parameters.author,
            "Scenario": parameters.scenario,
            "NumberOfDaysToProject": parameters.n_days,
            "CurrentlyHospitalizedCovidPatients": parameters.current_hospitalized,
            "DoublingTimeBeforeSocialDistancing": parameters.doubling_time,
            "SocialDistancingPercentReduction": parameters.relative_contact_rate,
            "HospitalizationPercentage": parameters.hospitalized.rate,
            "ICUPercentage": parameters.icu.rate,
            "VentilatedPercentage": parameters.ventilated.rate,
            "HospitalLengthOfStay": parameters.hospitalized.length_of_stay,
            "ICULengthOfStay": parameters.icu.length_of_stay,
            "VentLengthOfStay": parameters.ventilated.length_of_stay,
            "HospitalMarketShare": parameters.market_share,
            "RegionalPopulation": parameters.susceptible,
            "CurrentlyKnownRegionalInfections": parameters.known_infected,
            "PresentResultAsDates": as_date,
            "MaxYAxisSet":max_y_axis_set,
            "MaxYAxis":max_y_axis,
        }
        out_json = json.dumps(out_obj)
        b64_json = base64.b64encode(out_json.encode()).decode()
        st.sidebar.markdown(
            """<a download="{filename}" href="data:text/plain;base64,{b64_json}" style="padding:.75em;border-radius:10px;background-color:#00aeff;color:white;font-family:sans-serif;text-decoration:none;">Save Parameters</a>"""
            .format(b64_json=b64_json,filename=filename), 
            unsafe_allow_html=True,
        )
