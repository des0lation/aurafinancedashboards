import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import requests, json
from web3 import Web3, HTTPProvider

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

col1, col2, col3 = st.columns(3)

sheet_url = "https://docs.google.com/spreadsheets/d/19tHankEKBCKLa3WSBf-X4LmAh0to9HhLV7Q8UBavHqg/gviz/tq?tqx=out:csv"
df = pd.read_csv(sheet_url)

# Making Smart Contract calls to auraBAL and veBAl to get aura finance dominance from onchain
infura_url = "https://mainnet.infura.io/v3/0159c1c270174247ab17c4839f766798"
web3 = Web3(HTTPProvider(infura_url))
contract_address = '0xC128a9954e6c874eA3d62ce62B468bA073093F25'
contract_abi = json.loads(
    '[{"name":"Deposit","inputs":[{"name":"provider","type":"address","indexed":true},{"name":"value","type":"uint256","indexed":false},{"name":"locktime","type":"uint256","indexed":true},{"name":"type","type":"int128","indexed":false},{"name":"ts","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"Withdraw","inputs":[{"name":"provider","type":"address","indexed":true},{"name":"value","type":"uint256","indexed":false},{"name":"ts","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"Supply","inputs":[{"name":"prevSupply","type":"uint256","indexed":false},{"name":"supply","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"stateMutability":"nonpayable","type":"constructor","inputs":[{"name":"token_addr","type":"address"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_authorizer_adaptor","type":"address"}],"outputs":[]},{"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"name","inputs":[],"outputs":[{"name":"","type":"string"}]},{"stateMutability":"view","type":"function","name":"symbol","inputs":[],"outputs":[{"name":"","type":"string"}]},{"stateMutability":"view","type":"function","name":"decimals","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"admin","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"nonpayable","type":"function","name":"commit_smart_wallet_checker","inputs":[{"name":"addr","type":"address"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"apply_smart_wallet_checker","inputs":[],"outputs":[]},{"stateMutability":"view","type":"function","name":"get_last_user_slope","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"view","type":"function","name":"user_point_history__ts","inputs":[{"name":"_addr","type":"address"},{"name":"_idx","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"locked__end","inputs":[{"name":"_addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"checkpoint","inputs":[],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"deposit_for","inputs":[{"name":"_addr","type":"address"},{"name":"_value","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"create_lock","inputs":[{"name":"_value","type":"uint256"},{"name":"_unlock_time","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"increase_amount","inputs":[{"name":"_value","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"increase_unlock_time","inputs":[{"name":"_unlock_time","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"withdraw","inputs":[],"outputs":[]},{"stateMutability":"view","type":"function","name":"balanceOf","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"balanceOf","inputs":[{"name":"addr","type":"address"},{"name":"_t","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"balanceOfAt","inputs":[{"name":"addr","type":"address"},{"name":"_block","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"totalSupply","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"totalSupply","inputs":[{"name":"t","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"totalSupplyAt","inputs":[{"name":"_block","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"supply","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"locked","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"amount","type":"int128"},{"name":"end","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"epoch","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"point_history","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"bias","type":"int128"},{"name":"slope","type":"int128"},{"name":"ts","type":"uint256"},{"name":"blk","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"user_point_history","inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"uint256"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"bias","type":"int128"},{"name":"slope","type":"int128"},{"name":"ts","type":"uint256"},{"name":"blk","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"user_point_epoch","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"slope_changes","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"view","type":"function","name":"future_smart_wallet_checker","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"smart_wallet_checker","inputs":[],"outputs":[{"name":"","type":"address"}]}]')
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
result = contract.functions.totalSupply().call()
contract_address_2 = '0x616e8BfA43F920657B3497DBf40D6b1A02D4608d'
contract_abi_2 = json.loads(
    '[{"inputs":[{"internalType":"string","name":"_nameArg","type":"string"},{"internalType":"string","name":"_symbolArg","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"operator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_operator","type":"address"}],"name":"setOperator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
contract2 = web3.eth.contract(address=contract_address_2, abi=contract_abi_2)
result2 = contract2.functions.totalSupply().call()
st.write("Total veBAL is", result / 10 ** 18)
st.write("Aura Finance owned veBAL is", result2 / 10 ** 18)
st.write("Aura Finance dominane is", 100 * result2 / result)


# Getting Asset Prices
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

# Create a new list of values for aura supply
total_supply = 58579243
aura_supply = []
default_value = 100 * result2 / result
aura_share = st.slider("Select projected AURA veBAL %share", min_value=0.0, max_value=100.0,step=0.1, format="%f") / 100
aura_revenue = []

# Revenue Daily Numbers
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

# Daily Users Numbers
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


@st.cache_resource
def get_bribes():
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
    return bribes


bribes = get_bribes()

bribed_votes = bribes['epoch']['bribed']
vote_pools = []
vote_amounts = []
remove_pools = ['MetaStable USDC/wUSDR', 'p-MetaStable USDC/wUSDR']

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

votes_per_dollar = sum(vote_amounts_sorted) / sum(bribe_amounts_sorted)

inflations = []
vl_aura = 13000000
emmission_per_vl_aura = []

st.write("These 6 pools have an average vote per dollar of", votes_per_dollar / 26)
st.write("vlAURA has a vote per dollar of", (26 * result2 / 10 ** 18) / (vl_aura * aura_price))

for balEarned in df['Bal Released']:
    auraUnitsMinted = aura_share * (((500 - (total_supply - 50000000) / 100000) * 2.5 + 700) / 500) * balEarned
    aura_revenue.append(balEarned * aura_share * bal_price)
    total_supply = total_supply + auraUnitsMinted
    vl_aura = vl_aura + 0.6 * auraUnitsMinted
    emmission_per_vl_aura.append(
        52 * (balEarned * aura_share * 0.75 + 0.75 * auraUnitsMinted * aura_price) / vl_aura)
    inflations.append(100 * 52 * auraUnitsMinted / total_supply)

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
inflation_line = px.line(df, x='Weeks', y='Aura Inflation', title="Aura Weekly Inflation Annualised")
emission_line = px.line(df, x='Weeks', y='vlAURA Emissions', title="$Emissions per $vlAURA Annualised")
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
