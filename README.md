![AutoUpdate](https://github.com/Sikerdebaard/netherlands-vaccinations-scraper/workflows/AutoUpdate/badge.svg)


# netherlands-vaccinations-scraper
Vaccination data as scraped from [Corona Dashboard](https://coronadashboard.rijksoverheid.nl/landelijk/vaccinaties) and the [RIVM](https://www.rivm.nl/covid-19-vaccinatie/cijfers-vaccinatieprogramma).  

# ACTIVE
NOTE: datasets are moved to deprecated without warning. This is because the Netherlands changes data format quite often, and we can't keep up with conversions.

## vaccine_administered_total.csv
`date` timestamp of the record
`estimated` the estimated number of doses administered as reported by the RIVM
`reported` the actual reported number of doses administered by various instances
`date_of_insertion_unix` technical record from the coronadashboard

## vaccine_administered_<instance>.csv
See `vaccine_administered_total.csv`. The difference is that while totals is an aggregation, these files contain the numbers per instance and might include either estimates, reported or combination of both.

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


## doses-administered-per-manufacturer.csv
`date` the cumulative numbers up till this date  
`Dosis` indicates if the numbers are for first-dose administered or second dose administered  
`Vaccin` indicates the vaccine, e.g. COM = BioNTech/Pfizer, MOD = Moderna  

All other columns represent groups specifically targeted to be vaccinated as reported by the RIVM.  

# DEPRECATED
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

