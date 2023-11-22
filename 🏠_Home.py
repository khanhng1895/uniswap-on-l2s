import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from millify import millify
from streamlit_extras.colored_header import colored_header

# st.cache_data.clear()

st.set_page_config(
    page_title="Uniswap On L2s",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": "https://twitter.com/sageOlamide",
        "About": None
    }
)

#style metric containers
st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: #c8d7db;
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: #b0020d;
}
</style>
"""
            , unsafe_allow_html=True)

text_1 = '<p style="font-family:sans-serif; color:#4d372c; font-size: 20px;">Back in November 2018, Uniswap introduced its V1 contract on the Ethereum mainnet, setting the stage for a new kind of decentralized exchange. Fast forward five years, and Uniswap has been on quite a journey, constantly evolving with each new version. But it\'s not just Ethereum—it has spread its wings to different blockchains, attracting more users and becoming a hub for trading, swaps, and Total Value Locked (TVL).</p>'

text_2 = '<p style="font-family:sans-serif; color:#4d372c; font-size: 20px;">In this dashboard, we\'ll take a closer look at how people are utilizing Uniswap across various L2 chains — Arbitrum, Optimism, Polygon, BSC (Binance Smart Chain), and Base. We\'ll unravel the details and common trends that define Uniswap\'s functionality within these scaling environments.</p>'

text_3 = '<p style="font-family:sans-serif; color:#4d372c; font-size: 20px;">The data used for this dashboard is <a href="https://flipsidecrypto.xyz/">Flipside Crypto’s</a> <code>defi.ez_dex_swaps</code> tables. Data refreshes every <b>24 hours</b>. You can click on <b>View SQL</b> under each chart to view the underlying SQL code.</p>'

# st.info("Use the menu on the left to select a page (click on > if closed).", icon="👈")
st.markdown(f'<h1 style="color:#434346;font-size:60px;text-align:center;">{"Uniswap On L2s"}</h1>', unsafe_allow_html=True)


st.markdown(text_1, unsafe_allow_html=True)
st.markdown(text_2, unsafe_allow_html=True)
st.markdown(text_3, unsafe_allow_html=True)


############################# cache datasets ########################################

url7 = "https://flipsidecrypto.xyz/edit/queries/6349f677-143b-4774-94d2-c0704633f365"
@st.cache_data
def load_df7():
    df7 = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{url7.split('/')[-1]}/data/latest")
    return df7

url8 = "https://flipsidecrypto.xyz/edit/queries/67409c8d-a5dd-4b4d-b611-710ef891281b"
@st.cache_data
def load_df8():
    df8 = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{url8.split('/')[-1]}/data/latest")
    return df8

url22 = "https://flipsidecrypto.xyz/edit/queries/95beab6d-99e4-4133-ae87-f3f000c46258"
@st.cache_data
def load_df22():
    df22 = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{url22.split('/')[-1]}/data/latest")
    return df22

############################### load datasets ###########################################

df7 = load_df7()
df8 = load_df8()
df22 = load_df22()

################################   charts   ##############################################


###############################___________________DF7_____________________#############################

df7_fig1 = px.pie(df7,
               names='CHAIN',
               values='UNIQUE_USERS',
               title='Unique Users on Uniswap',
               color='CHAIN')

df7_fig2 = px.pie(df7,
               names='CHAIN',
               values='VOLUME',
               title='Swap Volume (USD) on Uniswap',
               color='CHAIN')
df7_fig2.update_traces(hovertemplate='%{label}: $%{value:,.0f}')

# Bar chart for avg swap size by chain
df7_fig3 = px.bar(df7, x='CHAIN', y='AVG_SWAP_SIZE_USD', color='CHAIN',
                    title='Average Swap Size (USD) by Chain',
                    labels={'AVG_SWAP_SIZE_USD': 'Average Swap Size'})
df7_fig3.update_traces(hovertemplate='%{label}: $%{value:,.0f}')

# Bar chart for median swap size by chain
df7_fig4 = px.bar(df7, x='CHAIN', y='MEDIAN_SWAP_SIZE_USD', color='CHAIN',
                   title='Median Swap Size (USD) by Chain',
                   labels={'MEDIAN_SWAP_SIZE_USD': 'Median Swap Size'})
df7_fig4.update_traces(hovertemplate='%{label}: $%{value:,.0f}')

###############################___________________DF8_____________________#############################
# single number
# UNIQUE_USERS	VOLUME	AVG_SWAP_SIZE_USD	MEDIAN_SWAP_SIZE_USD

###############################___________________DF22_____________________#############################

df22_fig1 = px.line(df22,
              x="WEEK",
              y="ACTIVE_USERS",
              color="CHAIN",
              title="Uniswap Weekly Active Users")
df22_fig1.update_layout(hovermode="x unified")

df22_fig2 = px.line(df22,
              x="WEEK",
              y="SWAP_COUNT",
              color="CHAIN",
              title="Uniswap Weekly Swap Count")
df22_fig2.update_layout(hovermode="x unified")


#################################################### LAYOUT #############################################

colored_header(
    label="",
    description="",
    color_name="gray-70",
)
st.markdown(f'<h1 style="color:#434346;font-size:40px;text-align:center;">{"General Overview"}</h1>', unsafe_allow_html=True)
colored_header(
    label="",
    description="",
    color_name="gray-70",
)

col_1a, col_1b, col_1c = st.columns(3)
with col_1a:
    st.metric("Swap Volume", f"${millify(df8['VOLUME'].sum(), precision=2)}")
with col_1b:
    st.metric("Average Swap Size", f"${millify(df8['AVG_SWAP_SIZE_USD'].sum(), precision=2)}")
with col_1c:
    st.metric("Median Swap Size", f"${millify(df8['MEDIAN_SWAP_SIZE_USD'].sum(), precision=2)}")


col_2a, col_2b = st.columns(2)
with col_2a:
    st.plotly_chart(df7_fig1, theme="streamlit", use_container_width=True)
with col_2b:
    st.plotly_chart(df7_fig2, theme="streamlit", use_container_width=True)

col_3a, col_3b = st.columns(2)
with col_3a:
    st.plotly_chart(df22_fig1, theme="streamlit", use_container_width=True)
with col_3b:
    st.plotly_chart(df22_fig2, theme="streamlit", use_container_width=True)

insight_1 = '<p style="font-family:sans-serif; color:#4d372c; font-size: 16px;">Back in November 2018, Uniswap introduced its V1 contract on the Ethereum mainnet, setting the stage for a new kind of decentralized exchange. Fast forward five years, and Uniswap has been on quite a journey, constantly evolving with each new version. But it\'s not just Ethereum—it has spread its wings to different blockchains, attracting more users and becoming a hub for trading, swaps, and Total Value Locked (TVL).</p>'

st.markdown(insight_1, unsafe_allow_html=True)