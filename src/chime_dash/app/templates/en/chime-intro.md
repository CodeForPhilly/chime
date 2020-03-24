# CHIME
### A Tool for COVID-19 Capacity Planning

As we prepare for the additional demands that the COVID-19 
outbreak will place on our hospital system, our operational 
leaders need up-to-date projections of what additional resources 
will be required. Informed estimates of how many patients will 
need hospitalization, ICU beds, and mechanical ventilation over 
the coming days and weeks will be crucial inputs to readiness responses 
and mitigation strategies.

CHIME allows hospitals to enter information about their population and modify assumptions around the spread and behavior of COVID-19. It then runs a standard SIR model to project the number of new hospital admissions each day, along with the daily hospital census. These projections can then be used to create best- and worst-case scenarios to assist with capacity planning. We’re announcing today that we’re open-sourcing CHIME and making it available to the healthcare community.

While the default parameters are customized and continually updated to reflect the situation at Penn Medicine, CHIME can be adapted for use by any hospital system by modifying parameters to reflect local contexts.

The most impactful parameter in a SIR model is the Doubling Time. This parameter defines how rapidly a disease spreads. Experiences in other geographical contexts suggest that doubling time may range from 3 to 13 days or more, with notable examples:

Wuhan, China: 6 days
South Korea: 13 days (As of March 14, 2020)
Italy: 5 days (As of March 14, 2020)
This value is particularly important because of the exponential nature of the spread of infectious diseases such as COVID-19. This is also why public health officials recommend measures like social distancing and hand washing: the more we can slow down the spread of COVID-19, the lower the peak demand on our healthcare system. Try out our live version of CHIME and see what happens when you modify the Doubling Time parameter. You can also experiment with scenarios involving different levels of incidence severity and average lengths of stay for each severity class.

We’ve put effort into determining good estimates for all model parameters and have set default values accordingly. Some of the default values are based on the current situation in our home region of Philadelphia. If you’re working somewhere outside of the Philadelphia region you can simply modify the following parameters to suit your patient population:

Currently Known Regional Infections
Currently Hospitalized COVID-19 Patients
Hospital Market Share (%)
As local spread progresses, revised estimates can be made for some of the values in CHIME. We will try our best to keep things up to date with the latest research, but if you find an issue with any of the values we are using we’d appreciate your feedback and contributions. We also set up a Slack channel if you’d like to chat with us.

– Penn Predictive Healthcare Team