import dateparser
import requests
import pandas as pd
from datetime import datetime, date
from pathlib import Path
import numpy as np



def dict_to_csv(d, file):
    df = pd.DataFrame(d, index=[0])
    df = df.set_index('date')
    df.index = pd.to_datetime(df.index)

    if Path(file).exists():
        df_org = pd.read_csv(file, index_col=0)
        df_org.index = pd.to_datetime(df_org.index)

        for idx, row in df.iterrows():
            for col in df.columns:
                df_org.at[idx, col] = row[col]

        df = df_org

    df.sort_index(inplace=True)
    df = df.fillna(0).astype(int)
    df.to_csv(file)


def parse_expected_delivery_vaccins(data):
    data_delv = {}

    data_delv['expected_deliveries_within_six_weeks'] = int(data["vaccinaties"]["data"]['kpi_expected_delivery']['value'])

    date = data["vaccinaties"]["data"]['kpi_expected_delivery']['date_of_report_unix']
    date = dateparser.parse(date).date()
    data_delv['date'] = date

    print(data_delv)
    dict_to_csv(data_delv, 'expected-doses-delivered-within-six-weeks.csv')


def parse_administered_doses(data):
    data_doses = {}
    data_doses_by_administering_instance = {}

    data_doses['total_vaccinations'] = int(data["vaccinaties"]["data"]['kpi_total']['value'])

    date = data["vaccinaties"]["data"]["sidebar"]["last_value"]["date_unix"]
    date = dateparser.parse(date).date()

    data_doses['date'] = date
    data_doses_by_administering_instance['date'] = date

    for administered in data["vaccinaties"]["data"]['kpi_total']['administered']:
        if administered['value'].strip() == '':
            continue
        administered_by = administered['description']

        for rep in remove_map:
            administered_by = administered_by.replace(rep, '')
            
        administered_by = administered_by.strip().strip('*')

        if administered_by in admby_mapper:
            administered_by = admby_mapper[administered_by]

        amount = int(administered['value'])
        data_doses_by_administering_instance[administered_by] = amount

    print(data_doses)
    print(data_doses_by_administering_instance)
    dict_to_csv(data_doses, 'people-vaccinated.csv')
    dict_to_csv(data_doses_by_administering_instance, 'people-vaccinated-by-instance.csv')
    
admby_mapper = {
    'gezet door GGD\'en': 'municipal health services (GGDs)',
    'GGD-GHOR': 'municipal health services (GGDs)',
    'LNAZ': 'hospitals',
    'GGDs': 'municipal health services (GGDs)',
}
remove_map = [
    'administered by',
    'reported by',
    'administered in',
]
    
def parse_estimates(data):
    data_doses = {}
    data_doses_by_administering_instance = {}

    data_doses['total_vaccinations'] = int(data["vaccinaties"]["data"]['kpi_total']['tab_total_estimated']['value'])

    date = data["vaccinaties"]["data"]["sidebar"]["last_value"]["date_unix"]
    date = dateparser.parse(date).date()

    data_doses['date'] = date
    data_doses_by_administering_instance['date'] = date

    for administered in data["vaccinaties"]["data"]['kpi_total']['tab_total_estimated']['administered']:
        if administered['value'].strip() == '':
            continue
        administered_by = administered['description']
        
        for rep in remove_map:
            administered_by = administered_by.replace(rep, '')
            
        administered_by = administered_by.strip().strip('*')
        
        if administered_by in admby_mapper:
            administered_by = admby_mapper[administered_by]
        
        amount = int(administered['value'])
        data_doses_by_administering_instance[administered_by] = amount

    print(data_doses)
    print(data_doses_by_administering_instance)
    dict_to_csv(data_doses, 'estimated-people-vaccinated.csv')
    dict_to_csv(data_doses_by_administering_instance, 'estimated-people-vaccinated-by-instance.csv')


data = requests.get('https://raw.githubusercontent.com/minvws/nl-covid19-data-dashboard/master/packages/app/src/locale/en.json').json()
parse_administered_doses(data)
parse_expected_delivery_vaccins(data)

parse_estimates(data)

