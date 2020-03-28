# Manual Testing Procedure

[Source](https://docs.google.com/document/d/19wl9BHUE5PXYQdSiljIGkWTPfYzHXqlyht8yIpCXukg/edit#)

1. Open up the live (production) app at http://penn-chime.phl.io/
    a. Refresh the page to make sure no inputs are cached
2. In a second tab/window run the app locally (e.g. http://127.0.0.1:8000/)
3. Verify one by one that each of the inputs in the sidebar have not moved (unless this was an explicit part of the issue being addressed). If the issue changed the input on purpose, make sure the rest of the inputs are in the same order as they were before
4. Line up the main frame of the app (the right hand side)
5. Go through the live and local version of the app one page at a time, keeping them in line so you can easily see if there are differences.
    a. Click all the check boxes and carefully inspect that the results are the same
    b. Look at all graphs and verify that the scale on the y-axis matches and that the scale on the x-axis matches. Verify that the values match
    c. Look at each of the data tables and verify that the data in the matches
    d. Pay special attention to the bold numbers at the top of the app and the various numbers in "Show more info about this tool" section near the top
6. Change the values for "Currently Hospitalized COVID-19 Patients", "Doubling time before social distancing (days)" and "Number of days to project" (slider on the right hand panel) to new values.
    a. Make sure these values are exactly the same in both the live (production) app and in the local app
7. Repeat steps 3-5
