import pytest

import penn_chime.cli

from datetime import date, timedelta

def test_main_with_doubling_time():
    """"
    Tests a run via CLI with the minimum amount of parameters. Exponential
    factor is defined by doubling-time.
    """
    arguments = [
        "pytest",
        "--current-hospitalized", "1",
        "--doubling-time", "2.5",
        "--hospitalized-days", "5",
        "--hospitalized-rate",  "0.01",
        "--icu-days", "10",
        "--icu-rate", "0.5",
        "--market-share", "0.1",
        "--infectious-days", "5",
        "--max-y-axis", "10000",
        "--n-days", "30",
        "--recovered", "10",
        "--relative-contact-rate", "0.1",
        "--population", "1000000",
        "--ventilated-days",  "5",
        "--ventilated-rate", "0.025"
        ]
    
    penn_chime.cli.run(arguments)
    
def test_main_with_date_first_hospitalized():
    """"
    Tests a run via CLI with the minimum amount of parameters. Exponential
    factor is defined by date-first-hospitalized.
    """
    arguments = [
        "pytest",
        "--current-hospitalized", "69",
        "--current-date", "2020-04-14",
        "--date-first-hospitalized", "2020-04-01",
        "--hospitalized-days", "5",
        "--hospitalized-rate",  "0.025",
        "--icu-days", "9",
        "--icu-rate", "0.075",
        "--market-share", "0.1",
        "--infectious-days", "14",
        "--max-y-axis", "1000",
        "--n-days", "30",
        "--recovered", "0",
        "--relative-contact-rate", "0.1",
        "--population", "1000000",
        "--ventilated-days",  "10",
        "--ventilated-rate", "0.005"
        ]
    
    penn_chime.cli.run(arguments)

def test_failure_on_missing_parameters():
    """Negative test to verify that an error is given when neither defining
       doubling-time nor date-first-hospitalized."""
    arguments = [
        "pytest",
        "--current-hospitalized", "69",
        "--hospitalized-days", "5",
        "--hospitalized-rate",  "0.025",
        "--icu-days", "9",
        "--icu-rate", "0.075",
        "--market-share", "0.1",
        "--infectious-days", "14",
        "--max-y-axis", "1000",
        "--n-days", "30",
        "--recovered", "0",
        "--relative-contact-rate", "0.1",
        "--population", "1000000",
        "--ventilated-days",  "10",
        "--ventilated-rate", "0.005"
        ]
    
    with pytest.raises(AssertionError):
        penn_chime.cli.run(arguments)

def test_main_with_csv_verification():
    """Integration test for CLI. Runs a five-day simulation and verifies the
       content of the resulting csv files."""
    current_date = date.today().strftime("%Y-%m-%d")
    n_days = 5
    arguments = [
        "pytest",
        "--current-hospitalized", "1",
        "--current-date", current_date,
        "--doubling-time", "2.5",
        "--hospitalized-days", "5",
        "--hospitalized-rate",  "0.01",
        "--icu-days", "10",
        "--icu-rate", "0.5",
        "--market-share", "0.1",
        "--infectious-days", "5",
        "--max-y-axis", "10000",
        "--n-days", str(n_days),
        "--recovered", "10",
        "--relative-contact-rate", "0.1",
        "--population", "1000000",
        "--ventilated-days",  "5",
        "--ventilated-rate", "0.025"
        ]
    
    penn_chime.cli.run(arguments)

    #Verify content of projected_admits.csv
    projected_admits_content = [
        [None, None, None],
        [0.5195079107728944,25.97539553864472,1.298769776932236],
        [0.6851383215271454,34.25691607635727,1.7128458038178636],
        [0.8129161146846768,40.64580573423383,2.0322902867116914],
        [1.029120162473117,51.456008123655835,2.5728004061827923],
        [1.3021513067257287,65.10756533628646,3.255378266814322],
        [1.6465388184586223,82.32694092293116,4.116347046146558],
        [2.0802813033400414,104.01406516700195,5.200703258350099]
    ]
    
    __validate_file(projected_admits_content, ",day,date,admits_hospitalized,admits_icu,admits_ventilated\n", current_date + "_projected_admits.csv")
            
    #Verify content of projected_admits.csv
    projected_census_content = [
        [0.0,0.0,0.0],
        [0.5195079107728944,25.97539553864472,1.298769776932236],
        [1.2046462323000398,60.23231161500199,3.0116155807500995],
        [2.0175623469847164,100.87811734923582,5.043905867461791],
        [3.0466825094578334,152.33412547289166,7.616706273644583],
        [4.3488338161835625,217.4416908091781,10.872084540458905],
        [5.47586472386929,299.76863173210927,13.689661809673227],
        [6.871007705682186,403.7826968991112,17.17751926420546]
    ]
    
    __validate_file(projected_census_content, ",day,date,census_hospitalized,census_icu,census_ventilated\n", current_date + "_projected_census.csv")
            
    #Verify content of sim_sir_w_date.csv
    sim_sir_w_date_content = [
        [999000.0,1000.0,10.0],
        [998480.4920892271,1319.5079107728943,210.0],
        [997795.3537677001,1740.7446501454608,473.901582154579],
        [996982.4376530153,2205.5118348010456,822.0505121836709],
        [995953.3174905422,2793.529630313953,1263.15287914388],
        [994651.1661838164,3536.9750109768916,1821.8588052066705],
        [993004.6273653577,4476.118827240136,2529.2538074020486],
        [990924.346062018,5661.176365132148,3424.4775728500767]
    ]
    
    __validate_file(sim_sir_w_date_content, ",day,date,susceptible,infected,recovered\n", current_date + "_sim_sir_w_date.csv")
    
    
def __validate_file(reference_file_content, reference_file_header, reference_file_name):
    with open(reference_file_name, "r") as f:
        lines = f.readlines()
        assert len(lines) == len(reference_file_content) + 1
        assert lines[0] == reference_file_header

        for i, row in enumerate(lines[1:]):
            reference_row = reference_file_content[i]
            tokens = row.split(",")
            row_date = date.today() + timedelta(days=i-2)
            assert int(tokens[0]) == i, f"Failed for file {reference_file_name} row {i+1}."
            assert int(tokens[1]) == i-2, f"Failed for file {reference_file_name} row {i+1}."
            assert tokens[2] == row_date.strftime("%Y-%m-%d"), f"Failed for file {reference_file_name} row {i+1}."
            print(f"'{tokens[3]},{tokens[4]},{tokens[5]}'")
            assert not tokens[3].strip() or float(tokens[3]) == pytest.approx(reference_row[0], 1e-10, 1e-1), f"Failed for file {reference_file_name} row {i+1}."
            assert not tokens[4].strip() or float(tokens[4]) == pytest.approx(reference_row[1], 1e-10, 1e-2), f"Failed for file {reference_file_name} row {i+1}."
            assert not tokens[5].strip() or float(tokens[5]) == pytest.approx(reference_row[2], 1e-10, 1e-3), f"Failed for file {reference_file_name} row {i+1}."
            
            
            