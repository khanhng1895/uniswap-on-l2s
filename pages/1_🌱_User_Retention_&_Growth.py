import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from millify import millify

# st.cache_data.clear()

st.set_page_config(
    page_title="Uniswap On L2s",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="auto",
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

st.markdown(f'<h1 style="color:#434346;font-size:60px;text-align:center;">{"User Retention & Growth"}</h1>', unsafe_allow_html=True)
st.info("Focusing on user dynamics, this page dissects user retention rates and growth patterns across Layer 2s. Understanding how users persist on different chains and exploring factors contributing to user growth provides valuable insights into the user experience and network effects.", icon="ℹ️")

############################# cache datasets ########################################

url1 = "https://flipsidecrypto.xyz/edit/queries/9eb769df-c80d-40af-81e9-2a9f3d00d95f"
@st.cache_data
def load_df1():
    df1 = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{url1.split('/')[-1]}/data/latest")
    return df1

url6 = "https://flipsidecrypto.xyz/edit/queries/ddca2c5e-2626-4303-bb77-3b7a44152587"
@st.cache_data
def load_df6():
    df6 = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{url6.split('/')[-1]}/data/latest")
    return df6

url16 = "https://flipsidecrypto.xyz/edit/queries/510159c8-01fb-4cfb-8945-532f510bc75c"
@st.cache_data
def load_df16():
    df16 = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{url16.split('/')[-1]}/data/latest")
    return df16

url17 = "https://flipsidecrypto.xyz/edit/queries/87050e70-1b02-4012-973d-6524766ce87b"
@st.cache_data
def load_df17():
    df17 = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{url17.split('/')[-1]}/data/latest")
    return df17

url26 = "https://flipsidecrypto.xyz/edit/queries/fddcceb6-6ee6-4220-8e6f-7b14cf8db853"
@st.cache_data
def load_df26():
    df26 = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{url26.split('/')[-1]}/data/latest")
    return df26

############################### load datasets ###########################################

df1 = load_df1()
df6 = load_df6()
df16 = load_df16()
df17 = load_df17()
df26 = load_df26()

################################   charts   ##############################################


###############################___________________DF1_____________________#############################

df1['PERCENTAGE'] = df1.groupby('CHAIN')['NUM_WALLETS'].transform(lambda x: x / x.sum() * 100)

df1_fig1 = px.bar(df1, x='CHAIN', y='PERCENTAGE', color='TRANSACTION_CATEGORY',
             labels={'PERCENTAGE': 'Percentage of Total Wallets'},
             custom_data=['NUM_WALLETS'], 
             title='Repeating Uniswap Users')

df1_fig1.update_layout(xaxis_title='Chain',
                  yaxis_title='Percentage')
df1_fig1.update_traces(hovertemplate='%{y:.2f}%<br>Number of Wallets: %{customdata[0]:,.0f}')
df1_fig1.update_layout(hovermode="x unified")
df1_fig1.update_layout(legend_title="User Category")

###############################___________________DF6_____________________#############################

df_retail = df6[df6['CATEGORY'] == 'Retail User']
df_whale = df6[df6['CATEGORY'] == 'Whale']

# Bar chart for Retail Users count
df6_fig1 = px.bar(df_retail, x='CHAIN', y='USER_COUNT', color='CHAIN',
                    title='Retail Users Count',
                    labels={'USER_COUNT': 'User Count'})
df6_fig1.update_layout(hovermode="x unified")

# Bar chart for Whales count
df6_fig2 = px.bar(df_whale, x='CHAIN', y='USER_COUNT', color='CHAIN',
                   title='Whales Count [Logarithmic Scale]',
                   log_y=True,
                   labels={'USER_COUNT': 'User Count'})
df6_fig2.update_layout(hovermode="x unified")

# Bar chart for Retail Users txn per user
df6_fig3 = px.bar(df_retail, x='CHAIN', y='TXN_PER_USER', color='CHAIN',
                    title='Transactions per Retail User',
                    labels={'TXN_PER_USER': 'Transactions per User'})
df6_fig3.update_layout(hovermode="x unified")

# Bar chart for Whales txn per user
df6_fig4 = px.bar(df_whale, x='CHAIN', y='TXN_PER_USER', color='CHAIN',
                   title='Transactions per Whale',
                   labels={'TXN_PER_USER': 'Transactions per User'})
df6_fig4.update_layout(hovermode="x unified")

# Bar chart for Retail Users avg swap size
df6_fig5 = px.bar(df_retail, x='CHAIN', y='AVG_SWAP_SIZE', color='CHAIN',
                    title='Retail Users Average Swap Amount ($)',
                    labels={'AVG_SWAP_SIZE': 'Average Swap Amount'})
df6_fig5.update_layout(
    xaxis_title="CHAIN", yaxis_title="AVG_SWAP_AMOUNT")
df6_fig5.update_layout(hovermode="x unified")

# Bar chart for Whales avg swap size
df6_fig6 = px.bar(df_whale, x='CHAIN', y='AVG_SWAP_SIZE', color='CHAIN',
                   title='Whales Average Swap Amount ($)',
                   labels={'AVG_SWAP_SIZE': 'Average Swap Amount'})
df6_fig6.update_layout(
    xaxis_title="CHAIN", yaxis_title="AVG_SWAP_AMOUNT")
df6_fig6.update_layout(hovermode="x unified")

###############################___________________DF16_____________________#############################

df16_fig1 = px.histogram(df16,
                   x="CHAIN",
                   y="TXN_COUNT",
                   color="LABEL_SUBTYPE",
                   title="Top 5 Contract Types Used By Uniswap Users per Chain [Logarithmic Scale]",
                   log_y=True,
                   color_discrete_sequence=px.colors.qualitative.Dark24)
df16_fig1.update_layout(
    xaxis_title="CHAIN",
    yaxis_title="TXN_COUNT",
    legend_title="Contract Type")

df16_fig1.update_layout(hovermode="x unified")

###############################___________________DF17_____________________#############################

df17_fig1 = px.histogram(df17,
                   x="CHAIN",
                   y="TXN_COUNT",
                   color="PROJECT_NAME",
                   title="Top 5 Projects Used By Uniswap Users per Chain [Logarithmic Scale]",
                   log_y=True,
                   color_discrete_sequence=px.colors.qualitative.Dark24)
df17_fig1.update_layout(
    xaxis_title="CHAIN",
    yaxis_title="TXN_COUNT",
    legend_title="Project Name")
df17_fig1.update_layout(hovermode="x unified")

##########################___________________DF26_____________________######################
df26_fig1 = px.line(df26,
              x="WEEK",
              y="NEW_USERS",
              color="CHAIN",
              title="Weekly New Users On Uniswap")
df26_fig1.update_layout(hovermode="x unified")

############################################ ADDED ############################################

url22 = "https://flipsidecrypto.xyz/edit/queries/95beab6d-99e4-4133-ae87-f3f000c46258"
@st.cache_data
def load_df22():
    df22 = pd.read_json(f"https://api.flipsidecrypto.com/api/v2/queries/{url22.split('/')[-1]}/data/latest")
    return df22

df22 = load_df22()

df22_fig3 = px.line(df22,
              x="WEEK",
              y="TXN_PER_USER",
              color="CHAIN",
              title="Weekly Uniswap Transactions per User")
df22_fig3.update_layout(hovermode="x unified")


#################################################### LAYOUT ##############################################

st.plotly_chart(df26_fig1, theme="streamlit", use_container_width=True)

col_1a, col_1b = st.columns([2, 1.2])
with col_1a:
    st.plotly_chart(df22_fig3, theme="streamlit", use_container_width=True)
with col_1b:
    st.plotly_chart(df1_fig1, theme="streamlit", use_container_width=True)

st.info("Users with an average swap amount of less than 100,000 USD are classified as 'Retail Users', while those with 100,000 USD or more are 'Whales'.", icon="ℹ️")

col_2a, col_2b = st.columns(2)
with col_2a:
    st.plotly_chart(df6_fig1, theme="streamlit", use_container_width=True)
with col_2b:
    st.plotly_chart(df6_fig2, theme="streamlit", use_container_width=True)

col_3a, col_3b = st.columns(2)
with col_3a:
    st.plotly_chart(df6_fig3, theme="streamlit", use_container_width=True)
with col_3b:
    st.plotly_chart(df6_fig4, theme="streamlit", use_container_width=True)

col_4a, col_4b = st.columns(2)
with col_4a:
    st.plotly_chart(df6_fig5, theme="streamlit", use_container_width=True)
with col_4b:
    st.plotly_chart(df6_fig6, theme="streamlit", use_container_width=True)

col_5a, col_5b = st.columns(2)
with col_5a:
    st.plotly_chart(df16_fig1, theme="streamlit", use_container_width=True)
with col_5b:
    st.plotly_chart(df17_fig1, theme="streamlit", use_container_width=True)

insight_1 = '<p style="font-family:sans-serif; color:#4d372c; font-size: 16px;">Back in November 2018, Uniswap introduced its V1 contract on the Ethereum mainnet, setting the stage for a new kind of decentralized exchange. Fast forward five years, and Uniswap has been on quite a journey, constantly evolving with each new version. But it\'s not just Ethereum—it has spread its wings to different blockchains, attracting more users and becoming a hub for trading, swaps, and Total Value Locked (TVL).</p>'

st.markdown(insight_1, unsafe_allow_html=True)