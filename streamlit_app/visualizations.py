import os
import streamlit as st
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt


DATA_URL = os.path.join(os.path.dirname(__file__), 'stoves2.csv')


st.title("CLEAN COOKING CATALOG data")


col_data_type = [['stove_details_name', 'unique'],
 ['details_manu', 'cat'],
 ['details_web', 'cat'],
 ['stove_desc', 'text'],
 ['details_tiers_eff_num', 'cat'],
 ['details_tiers_safe_num', 'cat'],
 ['details_tiers_co_num', 'cat'],
 ['details_tiers_pm_num', 'cat'],
 ['details_tiers_dur_num', 'nan'],
 ['details_tiers_iwa_ie_num', 'cat'],
 ['stove_life', 'float'],
 ['pot_rec', 'cat'],
 ['pot_cap', 'float'],
 ['stove_feed', 'range'],
 ['stove_food_common', 'text,multicat'],
 ['stove_price', 'range'],
 ['stove_dimensions', 'multiint'],
 ['stove_weight', 'float'],
 ['stove_assembly_materials', 'multicat, text'],
 ['iso_co_val', 'float'],
 ['iso_co_sd', 'range'],
 ['iso_co_num', '??'],
 ['iso_co_date', 'date'],
 ['iso_co_fuel', 'cat'],
 ['iso_pm_val', 'float'],
 ['iso_pm_sd', 'range'],
 ['iso_pm_num', '?'],
 ['iso_pm_date', 'date'],
 ['iso_pm_fuel', 'cat'],
 ['iso_eff_char_val', 'float'],
 ['iso_eff_char_sd', 'range'],
 ['iso_eff_char_num', '?'],
 ['iso_eff_char_date', 'date'],
 ['iso_eff_char_fuel', 'cat'],
 ['iso_eff_val', 'nan'],
 ['iso_eff_sd', 'nan'],
 ['iso_eff_num', '?'],
 ['iso_eff_date', 'nan'],
 ['iso_eff_fuel', 'nan'],
 ['iso_safe_val', 'nan'],
 ['iso_safe_sd', 'nan'],
 ['iso_safe_num', '?'],
 ['iso_safe_date', 'nan'],
 ['iso_safe_fuel', 'nan'],
 ['iso_dur_val', 'nan'],
 ['iso_dur_sd', 'nan'],
 ['iso_dur_num', '?'],
 ['iso_dur_date', 'nan'],
 ['iso_dur_fuel', 'nan'],
 ['iwa_co_val', 'float'],
 ['iwa_co_sd', 'range'],
 ['iwa_co_num', 'float'],
 ['iwa_co_date', 'cat'],
 ['hp_co_fuel', 'cat'],
 ['iwa_pm_val', 'float'],
 ['iwa_pm_sd', 'range'],
 ['iwa_pm_num', 'cat'],
 ['iwa_pm_date', 'cat'],
 ['hp_pm_fuel', 'cat'],
 ['iwa_co_low_val', 'float'],
 ['iwa_co_low_sd', 'range'],
 ['iwa_co_low_num', 'cat'],
 ['iwa_co_low_date', 'cat'],
 ['lp_co_fuel', 'cat'],
 ['iwa_pm_low_val', 'float'],
 ['iwa_pm_low_sd', 'range'],
 ['iwa_pm_low_num', 'cat'],
 ['iwa_pm_low_date', 'cat'],
 ['lp_pm_fuel', 'cat'],
 ['iwa_eff_val', 'float'],
 ['iwa_eff_sd', 'range'],
 ['iwa_eff_num', 'cat'],
 ['iwa_eff_date', 'cat'],
 ['hp_eff_fuel', 'cat']]
# Deleting repeated columns
def delete_repeated_columns(data):
    for col in data.columns:
        if col[-2:] == '.1':
            data.drop(columns=[col], inplace=True)
    return data
def average_from_range(series):
    new_series = []
    for string in series:
        integer = string
        try:
            integer = float(string)
        except:
            try:
                integer = sum([float(s) for s in string.split('-')])/2
            except:
                integer = 'nan'
        new_series.append(integer)
    return new_series
@st.cache(persist=False)
def load_data():
    data = pd.read_csv(DATA_URL, na_values=['Not Available','null'])
    #data['FechaComision'] = data.apply(lambda x: serial_2_dt(x['FechaComision']), axis=1)
    #data['FechaComision'] = pd.to_datetime(data['FechaComision'])
    #data.rename(columns={'Longitud':'lon','Latitud':'lat'}, inplace=True)
    delete_repeated_columns(data)
    data.dropna(how='all', axis=1, inplace=True)
    data.drop(columns=['stove_desc'])
    for col in col_data_type:
        if col[1] == 'range':
            data[col[0]] = average_from_range(data[col[0]])
    return data

data = load_data()

st.markdown('## Variable count')
non_nans_per_column = {}
for col,val in zip(data.columns,data.count()):
    non_nans_per_column[col] = val
    
non_nans_per_column = dict(sorted(non_nans_per_column.items(), key=lambda x:x[1], reverse=True))
st.plotly_chart(px.histogram(x=non_nans_per_column.keys(), y=non_nans_per_column.values()))


st.markdown('## Scatterplots')



continuous_variables = [var[0] for var in col_data_type if 'int' == var[1] or 'float' == var[1]]
#print(continuous_variables)
y = st.selectbox('y', continuous_variables)
sub_data = data[data[y].notna()]
x = st.selectbox('x', set(sub_data.columns)-set(y), key='2254')

color=None
if st.checkbox('Color', value=False):
    sub_data = sub_data[sub_data[x].notna()]
    color = st.selectbox('color', set(sub_data.columns)-set([y,x]), key='225d4')
    
symbol=None
if st.checkbox('Symbol', value=False):
    try:
        sub_data = sub_data[sub_data[color].notna()]
    except:
        pass
    symbol = st.selectbox('symbol', set(sub_data.columns)-set([y,x,color]), key='225ddsf4')
    sub_data = sub_data[sub_data[symbol].notna()]
    


fig = px.scatter(sub_data, x=x, y=y, color=color, symbol=symbol, hover_name=sub_data.stove_details_name)
st.plotly_chart(fig)


#print(data.columns)
