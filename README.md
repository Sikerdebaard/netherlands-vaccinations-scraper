![AutoUpdate](https://github.com/Sikerdebaard/netherlands-vaccinations-scraper/workflows/AutoUpdate/badge.svg)

# netherlands-vaccinations-scraper
Vaccination data as scraped from https://coronadashboard.rijksoverheid.nl/landelijk/vaccinaties

## people-vaccinated.csv
`date` iso datestamp when the row was published.  
`total_vaccinations` total vaccination doses administered.

## people-vaccinated-by-instance.csv
`date` iso datestamp when the row was published.
Every column name is an instance as reported by the dashboard. The column names might change over time as we add or remove mappings.

## expected-doses-delivered-within-six-weeks.csv
`date` iso datestamp when the row was published.  
`expected_deliveries_within_six_weeks` the number of doses that are expected to be delivered to the Netherlands within six weeks.

## vaccine-doses-deliveries-by-vaccine.csv
`year-week` the year and isoweek when the delivery should take place  
`sum` the sum of all the expected doses that are to be delivered in that specific week for all manufacturers  
`cumulative` the cumulative total  
All other columns are names of manufacturers and show the number of vaccine doses that are expected to be delivered in that specific week.
