from bs4 import BeautifulSoup
import requests

baseurl = 'https://coronadashboard.rijksoverheid.nl'
page = requests.get(baseurl + '/landelijk/vaccinaties')
soup = BeautifulSoup(page.text)

svgfile = '/tmp/dashboard.svg'
pngfile = '/tmp/dashboard.png'

for article in soup.find_all('article'):
    for h3 in article.find_all('h3'):
        key = h3.text.strip()
        if key in 'Verwachte leveringen per week':
            svg = str(article.find('svg'))
            with open(svgfile, 'w') as fh:
                fh.write(svg)



from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

drawing = svg2rlg(svgfile)
renderPM.drawToFile(drawing, pngfile, fmt="PNG")

import numpy as np
import cv2

org_img = cv2.imread(pngfile)


import pytesseract

def linecastlegend(img, y):
    color = 0
    legend_labels = []
    indicator = 0
    label_num = 0
    current_label = {}
    white_pixel_counter = 0
    for x in range(0, img.shape[1]):
        if img[y, x].sum() != 765:
            white_pixel_counter = 0
            if indicator == 0:
                current_label['label_color'] = img[y, x+3]
                indicator = 1
            elif indicator == 2:
                if 'x_left' not in current_label:
                    current_label['x_left'] = x

                y_high = y
                y_low = y
                while img[y_high, x].sum() != 765:
                    y_high += 1
                while img[y_low, x].sum() != 765:
                    y_low -= 1

                current_label['x_right'] = x

                if 'y_high' not in current_label:
                    current_label['y_high'] = y_high
                    current_label['y_low'] = y_low

                if y_high > current_label['y_high']:
                    current_label['y_high'] = y_high

                if y_low > current_label['y_low']:
                    current_label['y_low'] = y_low

        if img[y, x].sum() == 765 and indicator == 2:
            white_pixel_counter += 1

            if white_pixel_counter > 25:
                white_pixel_counter = 0
                legend_labels.append(current_label)
                current_label = {}
                indicator = 0

        if img[y, x].sum() == 765 and indicator == 1:
            indicator = 2


    counter = 0
    for label in legend_labels:
        img_label = img[y_low-5:y_high+5, label['x_left']-5:label['x_right']+5]
        text = pytesseract.image_to_string(img_label)
        label['text'] = text.strip()
        counter+=1

    return legend_labels

legend = 374
img = org_img.copy()


legend = linecastlegend(img, legend)


import pandas as pd

y = 300
x = 795

img = org_img.copy()

barchart = {}

while img[y, x].sum() == 765:
    y += 1
    
barchart['y_barchart_start'] = y
barchart['bars'] = []

y -= 2
x = 30
bar = {}
indicator = 0
for x in range(x, img.shape[1]):
    if img[y, x].sum() != 765 and indicator == 0:
        indicator = 1
        bar['x_left'] = x
    elif img[y, x].sum() == 765 and indicator == 1:
        indicator = 0
        bar['x_right'] = x - 1
        bar['x_middle'] = bar['x_left'] + (bar['x_right'] - bar['x_left']) // 2
        barchart['bars'].append(bar)
        bar = {}
        
indicator = 0
line = {}
barchart['lines'] = []
x = 795
for y in range(barchart['y_barchart_start'] + 1, -1, -1):
    if img[y, x].sum() != 765 and indicator == 0:
        indicator = 1
        line['y_bottom'] = y
    elif img[y, x].sum() == 765 and indicator == 1:
        indicator = 0
        line['y_top'] = y - 1
        line['y_middle'] = line['y_top'] + ((line['y_bottom'] - line['y_top']) // 2)
        barchart['lines'].append(line)
        line = {}
        
    
from pytesseract import Output



d = pytesseract.image_to_data(img, output_type=Output.DICT)
n_boxes = len(d['level'])
rows = []
for i in range(n_boxes):
    row = [d['left'][i], d['top'][i], d['width'][i], d['height'][i], d['text'][i]]
    
    area = row[2] * row[3]
    area_perc = area / np.prod(img.shape[:2])
    
    row.append(area)
    row.append(area_perc)
    
    rows.append(row)

df = pd.DataFrame(rows)
df.columns = ['left', 'top', 'width', 'height', 'text', 'area', 'area_perc_total']

df_scale = df[df['top'] < 30]
scale = ' '.join([x for x in df_scale['text'].values if x != ''])
scale = scale.replace('x', '*').replace('.', '')

if '*' not in scale:
    raise SystemExit('Something changed')

df_bars = df[(df['left'] + df['width'] < barchart['y_barchart_start'] - 1) & (~df.index.isin(df_scale.index))]

for line in barchart['lines']:
    y = line['y_middle']
    
    text = ' '.join([x for x in df_bars.iloc[(df_bars['top']-y).abs().argsort()[:2]]['text'].values if x != ''])
    if text.strip() != '':
        line['value'] = text
        

df_lines = pd.DataFrame(barchart['lines'])
df_lines = df_lines.sort_values('y_top', ascending=False)
mean_increment = df_lines['value'].dropna().astype(int).diff().dropna().mean()

df_lines.at[0, 'value'] = 0
prev = 0
for idx in df_lines.index:
    if pd.isna(df_lines.at[idx, 'value']):
        df_lines.at[idx, 'value'] = prev + mean_increment
    prev = int(df_lines.at[idx, 'value'])

df_lines['value'] = df_lines['value'].astype(int)

df_lines['real_value'] = df_lines['value'].apply(lambda x: eval(f'{x} {scale}'))

avg_pixels_per_line = int(abs(df_lines['y_middle'].diff().mean()))
mean_value_per_line = int(df_lines['real_value'].diff().mean())

mean_value_per_pixel = int(mean_value_per_line / avg_pixels_per_line)


import re

img_view = img.copy()

legend_mapper = {tuple(x['label_color']): x['text'] for x in legend}

for bar in barchart['bars']:
    bar['parts'] = {}
    part = {'y_start': barchart['y_barchart_start']}
    y = barchart['y_barchart_start']
    x = bar['x_middle']
    vaccine = None
    while img[y, x].sum() != 765:
        coltuple = tuple(img[y, x])
        if coltuple in legend_mapper:

            if vaccine is not None and vaccine != legend_mapper[coltuple]:
                part['y_end'] = y-1
                bar['parts'][vaccine] = part
                part = {'y_start': y}
            vaccine = legend_mapper[coltuple]

        img_view[y, x] = 0
        y -= 1

    if vaccine:
        part['y_end'] = y-1
        bar['parts'][vaccine] = part



df_bar_labels = df[(df['top'] > barchart['y_barchart_start']) & (df['top'] < min([x['y_low'] for x in legend]) - 10)]

print(mean_value_per_pixel)
for bar in barchart['bars']:
    for k, v in bar['parts'].items():
        part = bar['parts'][k]
        part['pixels'] = part['y_start'] - part['y_end']
        part['estimated_value'] = (part['pixels']) * ean_value_per_pixel
        print(part['pixels'])

    x = bar['x_middle']

    bar_timestamp = {}
    for idx, row in df_bar_labels.iloc[(df_bar_labels['left']-x).abs().argsort()].iterrows():
        val = row['text'].strip()

        if val == '':
            continue

        if re.match(r'^\d*$', val):
            if int(val) > 53 and 'year' not in bar_timestamp:
                bar_timestamp['year'] = int(val)
            elif int(val) <= 53 and 'week' not in bar_timestamp:
                bar_timestamp['week'] = int(val)

        if 'week' in bar_timestamp and 'year' in bar_timestamp:
            break

    bar['label'] = f"{bar_timestamp['year']}-{bar_timestamp['week']:02d}"


vaccines = [x['text'] for x in legend]

numvaccines = []
for bar in barchart['bars']:
    bardata = {'year-week': bar['label'], **{k: v['estimated_value'] for k, v in bar['parts'].items()}}
    numvaccines.append(bardata)
    
df_vaccines = pd.DataFrame(numvaccines)
df_vaccines = df_vaccines.set_index('year-week')

df_vaccines = df_vaccines.sort_index().round(0).fillna(0).astype(int)

def specialround(x):
    if x >= 100_000_000:
        base = 50_000_000
    elif x >= 10_000_000:
        base = 5_000_000
    elif x >= 1_000_000:
        base = 500_000
    elif x >= 100_000:
        base = 50_000
    elif x >= 10_000:
        base = 5_000
    elif x >= 1_000:
        base = 500
    elif x >= 100:
        base = 50
    else:
        base = 5
    
    return base * round(x/base)


#for col in df_vaccines.columns:
#    df_vaccines[col] = df_vaccines[col].apply(specialround)



df_vaccines['sum'] = df_vaccines.sum(axis=1)
from pathlib import Path
csv_out = Path('vaccine-doses-deliveries-by-vaccine.csv')

if csv_out.exists():
    df_vaccines_old = pd.read_csv(csv_out, index_col=0)

    for idx, row in df_vaccines.iterrows():
        for col in df_vaccines.columns:
            df_vaccines_old.at[idx, col] = row[col]

    df_vaccines = df_vaccines_old

df_vaccines['cumulative'] = df_vaccines['sum'].cumsum()

df_vaccines.to_csv('vaccine-dose-deliveries-by-manufacturer.csv')
