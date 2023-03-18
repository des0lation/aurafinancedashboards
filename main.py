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

col1,col2,col3 = st.columns(3)

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

@st.cache_data()
def get_emperdol():
    resp = requests.get("https://aura-balancer-apr.onrender.com/llama-airforce").json()['emissionsPerUsd']
    return resp

#Revenue Daily Numbers
headers = {
    'authority': 'gateway.thegraph.com',
    'accept': 'application/json, multipart/mixed',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://thegraph.com',
    'referer': 'https://thegraph.com/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

json_data = {
    'query': 'query MyQuery {\n  vaultDailySnapshots(first: 1000) {\n    dailyTotalRevenueUSD\n    totalValueLockedUSD\n    dailySupplySideRevenueUSD\n    dailyProtocolSideRevenueUSD\n    timestamp\n  }\n}',
    'operationName': 'MyQuery',
}

response = requests.post(
    'https://gateway.thegraph.com/api/15a8b7b2f17ddd2f71d8fac4f91391f5/deployments/id/QmZsrUK6WXHFL82D7RMD5cuSjNrdU7dukg386Z4rWfwuVR',
    headers=headers,
    json=json_data,
)

#Daily Users Numbers
headers = {
    'authority': 'gateway.thegraph.com',
    'accept': 'application/json, multipart/mixed',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://thegraph.com',
    'referer': 'https://thegraph.com/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

json_data = {
    'query': 'query MyQuery {\n  usageMetricsDailySnapshots(first: 1000) {\n    dailyActiveUsers\n    timestamp\n  }\n}',
    'operationName': 'MyQuery',
}

users = requests.post(
    'https://gateway.thegraph.com/api/15a8b7b2f17ddd2f71d8fac4f91391f5/deployments/id/QmZsrUK6WXHFL82D7RMD5cuSjNrdU7dukg386Z4rWfwuVR',
    headers=headers,
    json=json_data,
)


headers = {
    'authority': 'api.llama.airforce',
    'accept': 'application/json',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://llama.airforce',
    'referer': 'https://llama.airforce/',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

json_data = {
    'platform': 'hh',
    'protocol': 'aura-bal',
}

bribes = requests.post('https://api.llama.airforce//bribes', headers=headers, json=json_data).json()

bribed_votes = bribes['epoch']['bribed']
vote_pools = []
vote_amounts = []
remove_pools = ['MetaStable USDC/wUSDR','p-MetaStable USDC/wUSDR']

bribed_amounts = bribes['epoch']['bribes']
bribe_pools = []
bribe_amounts = []
for bribe in bribed_amounts:
    if 'MetaStable' in bribe['pool'] and bribe['pool'] not in remove_pools:
        bribe_pools.append(bribe['pool'])
        bribe_amounts.append(bribe['amountDollars'])
        try:
            vote_amounts.append(bribed_votes[bribe['pool']])
        except:
            vote_amounts.append(0)



# Sort the bribe and vote amounts in descending order
bribe_sorted = sorted(zip(bribe_pools, bribe_amounts), key=lambda x: x[1], reverse=True)
vote_sorted = sorted(zip(bribe_pools, vote_amounts), key=lambda x: x[1], reverse=True)

# Unzip the sorted values into separate lists
bribe_pools_sorted, bribe_amounts_sorted = zip(*bribe_sorted)
vote_pools_sorted, vote_amounts_sorted = zip(*vote_sorted)



# Create the sorted bar charts
bribe_bar = px.bar(x=bribe_pools_sorted, y=bribe_amounts_sorted, title="Bribes", text=bribe_amounts_sorted)
bribe_bar.update_traces(texttemplate='%{text:.2s}', textposition='inside', marker_color='green')
vote_bar = px.bar(x=vote_pools_sorted, y=vote_amounts_sorted, title="Bribed Votes", text=vote_amounts_sorted)
vote_bar.update_traces(texttemplate='%{text:.2s}', textposition='inside', marker_color='orange')




col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(vote_bar)

with col2:
    st.plotly_chart(bribe_bar)


bal_price = get_bal_price()
aura_price = get_aura_price()
aurabal_price = get_aurabal_price()
emm_per_dollar = get_emperdol()

with col1:
    st.write("Aura Price is", aura_price)
with col2:
    st.write("Balancer Price is", bal_price)
with col3:
    st.write("Aura Bal price is", aurabal_price)


st.write("Currently Emmissions per $ is", emm_per_dollar)

inflations = []
vl_aura = 13000000
emmission_per_vl_aura = []

for balEarned in df['Bal Released']:
    auraUnitsMinted = aura_share * (((500 - (total_supply - 50000000) / 100000) * 2.5 + 700) / 500) * balEarned
    aura_revenue.append(balEarned*aura_share*bal_price)
    total_supply = total_supply + auraUnitsMinted
    vl_aura = vl_aura + 0.6 * auraUnitsMinted
    emmission_per_vl_aura.append(52 * (balEarned*aura_share*bal_price * 0.75 + auraUnitsMinted * aura_price)/(vl_aura*aura_price) )
    inflations.append(100 * 52 * auraUnitsMinted/total_supply)

    aura_supply.append(total_supply)

# Add the new columns to the DataFrame
df['Aura Share'] = aura_share
df['Aura Supply'] = aura_supply
df['Aura Revenue'] = aura_revenue
df['Aura Inflation'] = inflations
df['vlAURA Emissions'] = emmission_per_vl_aura

# Create the Plotly figure objects
fig_supply = px.scatter(df, x="Weeks", y="Supply", title="Balancer vs Aura Supply")
aura_trace = px.scatter(df, x='Weeks', y='Aura Supply')
inflation_line = px.line(df, x= 'Weeks', y = 'Aura Inflation',title = "Aura Weekly Inflation Annualised")
emission_line = px.line(df, x= 'Weeks', y = 'vlAURA Emissions',title = "$Emissions per $vlAURA Annualised")
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
    st.plotly_chart(inflation_line)
with col2:
    st.plotly_chart(fig_revenue_json)
    st.plotly_chart(emission_line)



