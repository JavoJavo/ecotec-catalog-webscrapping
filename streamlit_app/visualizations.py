import os
import streamlit as st
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt

dataset = st.selectbox('data', ['stoves','philips'], key='225sddssdd4')
if dataset == 'stoves':

    DATA_URL = os.path.join(os.path.dirname(__file__), 'stoves4.csv')
    st.title("CLEAN COOKING CATALOG data")

    @st.cache(persist=False)
    def load_data():
        data = pd.read_csv(DATA_URL, na_values=['Not Available','null'])
        data.drop(data.columns[[11,12,13,14,16,18,23,28,33,38,43,48,53]],axis=1,inplace=True)
        return data

    data = load_data()
    name = 'stove_details_name'

elif dataset == 'philips':
    DATA_URL = os.path.join(os.path.dirname(__file__), 'focos_philips5.csv')
    st.title("Philips Catalog data")

    @st.cache(persist=False)
    def load_data():
        data = pd.read_csv(DATA_URL, na_values=['Not Available','null'])
        #data.drop(data.columns[[11,12,13,14,16,18,23,28,33,38,43,48,53]],axis=1,inplace=True)
        return data

    data = load_data()
    name = 'Nombre del producto del pedido'
st.markdown('## Variable count')
non_nans_per_column = {}
for col,val in zip(data.columns,data.count()):
    non_nans_per_column[col] = val
    
non_nans_per_column = dict(sorted(non_nans_per_column.items(), key=lambda x:x[1], reverse=True))
st.plotly_chart(px.histogram(x=non_nans_per_column.keys(), y=non_nans_per_column.values()))


st.markdown('## Scatterplot')

import numpy as np

continuous_variables = data.select_dtypes(include=np.number).columns
#print(continuous_variables)
y = st.selectbox('y', continuous_variables)
sub_data = data[data[y].notna()]
x = st.selectbox('x', set(sub_data.columns)-set(y), key='2254')

color=None
if st.checkbox('Color', value=False):
    sub_data = sub_data[sub_data[x].notna()]
    color = st.selectbox('color', set(sub_data.columns)-set([y,x]), key='225d4')
    
#symbol=None
#if st.checkbox('Symbol', value=False):
#    try:
#        sub_data = sub_data[sub_data[color].notna()]
#    except:
#        pass
#    symbol = st.selectbox('symbol', set(sub_data.columns)-set([y,x,color]), key='225ddsf4')
#    sub_data = sub_data[sub_data[symbol].notna()]
    

size=None
agg=False
import copy
if st.checkbox('Size', value=False):
    if st.checkbox('Aggregate size (and mean of other values)', value=False):
        size = st.selectbox('size', set(sub_data.columns)-set([y,x,color]), key='225dfsddsf4')
        count = sub_data[size].value_counts().to_dict()
        sub_data_copy = copy.deepcopy(sub_data)
        sub_data = sub_data.groupby(size).mean()
        sub_data[size+' count'] = [count[i] for i in sub_data_copy[size].value_counts().index]
        #size = st.selectbox('size', set(sub_data.columns)-set([y,x,color]), key='225dfsddsf4')
        size = size+' count'
        agg=True
    else:
        agg=False
        try:
            sub_data = sub_data[sub_data[color].notna()]
            #sub_data = sub_data[sub_data[symbol].notna()]
        except:
            pass
        size = st.selectbox('size', set(sub_data.columns)-set([y,x,color]), key='225dfsddsf4')
    sub_data = sub_data[sub_data[size].notna()]
#print(data.columns)

    
if agg==True:
    fig2 = px.scatter(sub_data, x=x, y=y,
                 size=size, color=color,
                      hover_name=['Value for aggregated count: '+str(c) for c in count.keys()]
                     #hover_name=sub_data[name]
                     )
    st.plotly_chart(fig2)
else:
    if st.checkbox('Fit line', value=False):
        fig2 = px.scatter(sub_data, x=x, y=y,
                     size=size, color=color,
                         hover_name=sub_data[name],
                          trendline="lowess")#, text=sub_data.stove_details_name)
        st.plotly_chart(fig2)
    else:
        fig2 = px.scatter(sub_data, x=x, y=y,
                     size=size, color=color,
                         hover_name=sub_data[name])
        st.plotly_chart(fig2)
