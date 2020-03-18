# Glossary

## Currently Known Regional Infections
This variable represents the number of currently known cases in the within the catchment area of interest (the catchment area served by your hospital). 

## Currently Hospitalized COVID-19 Patients 
This variable represents the number of inpatient hospitalizations within the hospital of interest (your hospital).  /**"note this is what I'm seeing in the python code" - natehscha /** 

## Doubling Time (days)
This variable represents the time it takes for the number of infected persons within the region/catchment area to double. This can be informed by/home/nate/chime/.env.examplede either local, national, or global data. The default value is /*6/* days.

## Hospitalization %
This represents the percentage of all cases that need to be hospitalized. In the real world, this may be informed by demographic information in your region (e.g. the age distribution of the population, where older cases are more likely to be hospitalized). This may be addressed in future versions of this app. The default value is /*5/*%, which is informed by _______________.

## ICU %
This represents the percentage of all cases that need admission to intensive care units (ICUs). In the real world, this may be informed by demographic information in your region (e.g. the age distribution of the population, where older cases are more likely to be admitted to the ICU). This may be addressed in future versions of this app. The default value is /*2/*%, which is informed by _______________.

## Ventilated %
This represents the percentage of all cases that are critically ill and require mechanical ventilation. In the real world, this may be informed by demographic information in your region (e.g. the age distribution of the population, where older cases are more likely to be need ventilation). This may be addressed in future versions of this app. The default value is /*2/*%, which is informed by _______________.

## Hospital LOS (Length of Stay)
This is the estimated amount of time that a hospitalized patient who does NOT need to be admitted to the ICU and does NOT need mechanical ventilation will stay at the hospital. The default value for this variable is /*7/* days. /*After patients are out of the hospital, they will move into self-quarantine and still be infectious for a number of days after (modeled to be 14 in total). Does this mean that they are still infectious in the model for only 7 more days? /*

## ICU LOS (Length of Stay)
This is the estimated amount of time that a hospitalized patient who needs to be admitted to the ICU and does NOT need mechanical ventilation will stay at the hospital. The default value for this variable is /*9/* days. 

## Ventilation LOS (Length of Stay)
This is the estimated amount of time that a hospitalized patient who needs mechanical ventilation will stay at the hospital. The default value for this variable is /*10/* days. 

## Hospital Market Share
This is the percent of the population in the hospital catchment area that the hospital of interest (your hospital) serves. For example, if you have a metro area that is served by two hospitals, and your hospital serves 40% of the people in that area, then your Hospital Market Share would be 40%.

## Regional Population
This variable is the population of the region/catchment area  which the hospital of interest (your hospital) serves. The current default value for this is /*4,119,405/* which represents the region which U Penn Hospital serves, including the city of Philadelphia as well as Chester, Montgomery, Bucks Counties and the State of Delaware. 
