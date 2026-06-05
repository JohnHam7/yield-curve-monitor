import sys
import streamlit as st
import matplotlib.pyplot as plt
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.metrics import get_yield_data, calculate_spread, calculate_zscore, get_recession_data
from fredapi import Fred

st.set_page_config(page_title='Yield Curve Monitor', layout='wide')

st.title('U.S. Treasury Yield Curve Monitor')

st.markdown('Real-time yield curve analysis — inversion detection & macro signals')

@st.cache_data
def load_data():
    fred = Fred(api_key=st.secrets['FRED_API_KEY'])
    curve_df = get_yield_data(fred)           
    curve_df = calculate_spread(curve_df)    
    curve_df['z_score'] = calculate_zscore(curve_df['spread']) 
    recession = get_recession_data(fred)   
    return curve_df, recession

curve_df, recession = load_data()

with st.sidebar:
    st.header('Settings')
    start_year = st.slider('Start Year', 2000, 2024, 2000)

df_filtered = curve_df[curve_df.index.year >= start_year]
recession_filtered = recession[recession.index.year >= start_year]

fig1, ax1 = plt.subplots(figsize=(14, 4))
ax1.fill_between(df_filtered.index, df_filtered['spread'].min() - 0.2, df_filtered['spread'].max() + 0.2,
                 where=recession_filtered.reindex(df_filtered.index).fillna(0) == 1,
                 color='gray', alpha=0.2, label='Recession (NBER)')
ax1.plot(df_filtered.index, df_filtered['spread'], color='steelblue', linewidth=1.2, label='2s10s Spread')
ax1.fill_between(df_filtered.index, df_filtered['spread'], 0,
                 where=df_filtered['inverted'], color='red', alpha=0.3, label='Inversion')
ax1.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax1.set_ylabel('Spread (%p)')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)
plt.close(fig1)

fig2, ax2 = plt.subplots(figsize=(14, 3))
ax2.plot(df_filtered.index, df_filtered['z_score'], color='purple', linewidth=1.2, label='Z-Score')
ax2.axhline(2, color='red', linewidth=0.8, linestyle='--', label='±2 Threshold')
ax2.axhline(-2, color='red', linewidth=0.8, linestyle='--')
ax2.axhline(0, color='black', linewidth=0.8, alpha=0.3)
ax2.fill_between(df_filtered.index, df_filtered['z_score'], 2,
                 where=df_filtered['z_score'] > 2, color='red', alpha=0.2, label='Anomaly')
ax2.fill_between(df_filtered.index, df_filtered['z_score'], -2,
                 where=df_filtered['z_score'] < -2, color='red', alpha=0.2)
ax2.set_ylabel('Z-Score')
ax2.set_xlabel('Date')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)
plt.close(fig2)

available_dates = curve_df.index.strftime('%Y-%m-%d').tolist()
maturity_labels = ['3M', '1Y', '2Y', '5Y', '7Y', '10Y', '20Y', '30Y']

col1, col2 = st.columns(2)
with col1:
    date1 = st.selectbox('Date 1', available_dates, index=available_dates.index('2021-01-01'))
    date2 = st.selectbox('Date 2', available_dates, index=available_dates.index('2022-10-01'))
with col2:
    date3 = st.selectbox('Date 3', available_dates, index=available_dates.index('2023-07-01'))
    date4 = st.selectbox('Date 4', available_dates, index=len(available_dates) - 1)

selected = {date1: 'steelblue', date2: 'orange', date3: 'red', date4: 'green'}

fig3, ax3 = plt.subplots(figsize=(10, 5))
for date, color in selected.items():
    row = curve_df.loc[date]
    ax3.plot(maturity_labels, row[maturity_labels], marker='o',
             label=date, color=color, linewidth=2)

ax3.set_xlabel('Maturity')
ax3.set_ylabel('Yield (%)')
ax3.legend()
ax3.grid(True, alpha=0.3)
st.pyplot(fig3)