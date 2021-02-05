![AutoUpdate](https://github.com/Sikerdebaard/netherlands-vaccinations-scraper/workflows/AutoUpdate/badge.svg)


# netherlands-vaccinations-scraper
Vaccination data as scraped from https://coronadashboard.rijksoverheid.nl/landelijk/vaccinaties

## people-vaccinated.csv
`date` iso datestamp when the row was published.  
`total_vaccinations` total vaccination doses administered.

## estimated-people-vaccinated.csv
`date` iso datestamp when the row was published  
`total_vaccinations` total vaccination doses administered as estimated by a mathematical model from the RIVM  

## people-vaccinated-by-instance.csv
`date` iso datestamp when the row was published.  

Every column name is an organisation involved in the vaccination process as reported by the dashboard. The column names might change over time as we add or remove mappings.  

## estimated-people-vaccinated-by-instance.csv
`date` iso datestamp when the row was published  

Every column name is an organisation involved in the vaccination process as reported by the mathematical model from the RIVM. The column names might change over time as we add or remove mappings.  

## expected-doses-delivered-within-six-weeks.csv
`date` iso datestamp when the row was published.  
`expected_deliveries_within_six_weeks` the number of doses that are expected to be delivered to the Netherlands within six weeks.

## vaccine-dose-deliveries-by-manufacturer.csv 
`year-week` the iso year and week, date_start_unix is used to generate this value  
`date_start` start of the week when the delivery should take place  
`date_end` end of the week when the delivery should take place  
`date_of_insertion` technical record, it is unclear what it means exactly but most likely this is the date when the record was added to the dashboard data  

All other columns are names of manufacturers and show the number of vaccine doses that are expected to be delivered in that specific week.



## vaccine-support.csv 
`year-week` the iso year and week, date_start_unix is used to generate this value  
`percentage_in_favor` percentage in favor of vaccination  
`percentage_already_vaccinated` percentage of population vaccinated  
`date_start_unix` start date of this rows values  
`date_end_unix` end date of this rows values    
`date_of_insertion_unix` technical record, it is unclear what it means exactly but most likely this is the date when the record was added to the dashboard data  
