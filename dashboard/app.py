import sys
import streamlit as st
import matplotlib.pyplot as plt

sys.path.append('/Users/seunghoham/Desktop/python/yield_curve_analysis')
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

latest = curve_df.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric('2s10s Spread', f"{latest['spread']:.2f}%p")
col2.metric('Z-Score', f"{latest['z_score']:.2f}")
col3.metric('Inverted', '🔴 Yes' if latest['inverted'] else '🟢 No')
st.divider()
st.subheader('2s10s Yield Spread & NBER Recessions')

fig1, ax1 = plt.subplots(figsize=(14, 4))
ax1.fill_between(curve_df.index, curve_df['spread'].min() - 0.2, curve_df['spread'].max() + 0.2,
                 where=recession.reindex(curve_df.index).fillna(0) == 1,
                 color='gray', alpha=0.2, label='Recession (NBER)')
ax1.plot(curve_df.index, curve_df['spread'], color='steelblue', linewidth=1.2, label='2s10s Spread')
ax1.fill_between(curve_df.index, curve_df['spread'], 0,
                 where=curve_df['inverted'], color='red', alpha=0.3, label='Inversion')
ax1.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax1.set_ylabel('Spread (%p)')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

st.divider()

st.subheader('Z-Score (24M Rolling)')

fig2, ax2 = plt.subplots(figsize=(14, 3))
ax2.plot(curve_df.index, curve_df['z_score'], color='purple', linewidth=1.2, label='Z-Score')
ax2.axhline(2, color='red', linewidth=0.8, linestyle='--', label='±2 Threshold')
ax2.axhline(-2, color='red', linewidth=0.8, linestyle='--')
ax2.axhline(0, color='black', linewidth=0.8, alpha=0.3)
ax2.fill_between(curve_df.index, curve_df['z_score'], 2,
                 where=curve_df['z_score'] > 2, color='red', alpha=0.2, label='Anomaly')
ax2.fill_between(curve_df.index, curve_df['z_score'], -2,
                 where=curve_df['z_score'] < -2, color='red', alpha=0.2)
ax2.set_ylabel('Z-Score')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)

st.divider()

st.subheader('Yield Curve Shape Comparison')

maturity_labels = ['3M', '1Y', '2Y', '5Y', '7Y', '10Y', '20Y', '30Y']

dates = {
    'Jan 2021 (Normal)': '2021-01-01',
    'Oct 2022 (Flat)': '2022-10-01',
    'Jul 2023 (Inverted)': '2023-07-01',
    'May 2026 (Current)': '2026-05-01',
}
colors = ['steelblue', 'orange', 'red', 'green']

fig3, ax3 = plt.subplots(figsize=(10, 5))

for (label, date), color in zip(dates.items(), colors):
    row = curve_df.loc[date]
    ax3.plot(maturity_labels, row[maturity_labels], marker='o',
             label=label, color=color, linewidth=2)

ax3.set_xlabel('Maturity')
ax3.set_ylabel('Yield (%)')
ax3.legend()
ax3.grid(True, alpha=0.3)
st.pyplot(fig3)