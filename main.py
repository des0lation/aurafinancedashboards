import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import requests,json

st.set_page_config(page_title="Aura Dashboard", page_icon="bar_chart", layout="wide")
st.title("Aura Dashboard")

options = ["Home", "About", "Contact"]
selection = st.sidebar.selectbox("Select an option", options)

# Display content based on the user's selection
if selection == "Home":
    st.write("Welcome to the Home page!")
elif selection == "About":
    st.write("This is the About page.")
else:
    st.write("Please contact us at contact@example.com")

sheet_url = "https://docs.google.com/spreadsheets/d/19tHankEKBCKLa3WSBf-X4LmAh0to9HhLV7Q8UBavHqg/gviz/tq?tqx=out:csv"
df = pd.read_csv(sheet_url)

# Create a new list of values for aura supply
total_supply = 58579243
aura_supply = []
aura_share = st.slider("Select projected AURA veBAL %share", min_value=0.0, max_value=100.0, value=50.0, step=0.1, format="%f")/100
aura_revenue = []
@st.cache_data()
def get_bal_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=balancer&vs_currencies=usd')
    bal_price = response.json()['balancer']['usd']
    return bal_price

@st.cache_data()
def get_aura_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=aura-finance&vs_currencies=usd')
    aura_price = response.json()['aura-finance']['usd']
    return aura_price

@st.cache_data()
def get_aurabal_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=aura-bal&vs_currencies=usd')
    aurabal_price = response.json()['aura-bal']['usd']
    return aurabal_price

bal_price = get_bal_price()
aura_price = get_aura_price()
aurabal_price = get_aurabal_price()

for balEarned in df['Bal Released']:
    auraUnitsMinted = aura_share * (((500 - (total_supply - 50000000) / 100000) * 2.5 + 700) / 500) * balEarned
    aura_revenue.append(balEarned*aura_share*bal_price)
    total_supply = total_supply + auraUnitsMinted
    aura_supply.append(total_supply)

# Add the new columns to the DataFrame
df['Aura Share'] = aura_share
df['Aura Supply'] = aura_supply
df['Aura Revenue'] = aura_revenue

# Create the Plotly figure objects
fig_supply = px.scatter(df, x="Weeks", y="Supply", title="Balancer vs Aura Supply")
aura_trace = px.scatter(df, x='Weeks', y='Aura Supply')
aura_trace.update_traces(marker=dict(color='#FF6EC7'))
fig_supply.add_trace(aura_trace.data[0])
fig_supply.update_layout(xaxis_tickangle=45)

fig_revenue = px.bar(df, x='Weeks', y='Aura Revenue', title='Aura Finance Weekly Revenue')

# Convert the figure objects to JSON-compatible formats
fig_supply_json = fig_supply.to_dict()
fig_revenue_json = fig_revenue.to_dict()


col1, col2 = st.columns(2)
# Display the plots in your Streamlit app
with col1:
    st.plotly_chart(fig_supply_json)
with col2:
    st.plotly_chart(fig_revenue_json)

col1,col2,col3 = st.columns(3)

with col1:
    st.write("Aura Price is", aura_price)
with col2:
    st.write("Balancer Price is", bal_price)
with col3:
    st.write("Aura Bal price is", aurabal_price)
