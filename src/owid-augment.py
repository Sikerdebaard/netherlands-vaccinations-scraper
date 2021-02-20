import pandas as pd

df_owid = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/79bc3c1a690454579ff275be34a347ab6125fb04/public/data/vaccinations/country_data/Netherlands.csv', index_col=['date'])
df_owid.index = pd.to_datetime(df_owid.index)

df_netherlands = pd.read_csv('vaccine_administered_total.csv', index_col=0)
df_netherlands['source'] = 'https://coronadashboard.rijksoverheid.nl/landelijk/vaccinaties'
df_netherlands.index = pd.to_datetime(df_netherlands.index)
df_netherlands.sort_index(inplace=True)

rename = {
    'source_url': 'source',
    'total_vaccinations': 'reported',
}
df_owid_mod = df_owid[rename.keys()].rename(columns=rename)
df_owid_mod['estimated'] = df_owid_mod['reported']
df_merged = pd.concat([df_netherlands, df_owid_mod[df_owid_mod.index < df_netherlands.index[0]]])
df_merged.sort_index(inplace=True)

df_merged = df_merged[['reported', 'estimated', 'source']]

df_merged.to_csv('augmented/doses_administered_raw.csv')

df_diff = df_merged['reported'].diff()
df_cumulative = df_merged[~(df_merged.index.isin(df_diff[df_diff < 0].index))]

df_merged.to_csv('augmented/doses_administered_cumulative.csv')
