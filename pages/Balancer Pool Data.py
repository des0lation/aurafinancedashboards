import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import requests, json, time
from web3 import Web3, HTTPProvider
from main import get_bal_price,get_aurabal_price
from main import result

import requests

st.set_page_config(page_title="Aura Dashboard", page_icon="bar_chart", layout="wide")
json_data = {
    'query': 'query GaugeFactories {\r\n  gaugeFactories {\r\n    gauges {\r\n      symbol\r\n      id\r\n    }\r\n  }\r\n}',
    'variables': {},
    'operationName': 'GaugeFactories',
}

pools = requests.post(
    'https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-gauges',
    json=json_data,
)

#Here I am declaring all the LST POOLs

bal_price = get_bal_price()
aurabal_price = get_aurabal_price()
lsts = ['stETH', 'wstETH', 'cbETH', 'staFiETH', 'ankrETH', 'rETH']
st.write("We are finding all lst pools which contain")
st.write(lsts)

@st.cache_resource
def getlstpools(lsts):
    json_data = {
        'query': 'query GaugeFactories {\r\n  gaugeFactories {\r\n    gauges {\r\n      symbol\r\n      id\r\n    }\r\n  }\r\n}',
        'variables': {},
        'operationName': 'GaugeFactories',
    }
    pools = requests.post(
        'https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-gauges',
        json=json_data,
    )
    lst_pools = {}
    for i in pools.json()['data']['gaugeFactories'][0]['gauges']:
        if any(item in i['symbol'] for item in lsts):
            lst_pools[i['symbol']] = i['id']
    for i in pools.json()['data']['gaugeFactories'][1]['gauges']:
        if any(item in i['symbol'] for item in lsts):
            lst_pools[i['symbol']] = i['id']
    return lst_pools

lst_pools = getlstpools(lsts)

@st.cache_resource
def getgaugeweight(id):
    infura_url = "https://mainnet.infura.io/v3/0159c1c270174247ab17c4839f766798"
    web3 = Web3(HTTPProvider(infura_url))
    contract_address = '0xC128468b7Ce63eA702C1f104D55A2566b13D3ABD'
    contract_abi = json.loads('[{"name":"AddType","inputs":[{"name":"name","type":"string","indexed":false},{"name":"type_id","type":"int128","indexed":false}],"anonymous":false,"type":"event"},{"name":"NewTypeWeight","inputs":[{"name":"type_id","type":"int128","indexed":false},{"name":"time","type":"uint256","indexed":false},{"name":"weight","type":"uint256","indexed":false},{"name":"total_weight","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"NewGaugeWeight","inputs":[{"name":"gauge_address","type":"address","indexed":false},{"name":"time","type":"uint256","indexed":false},{"name":"weight","type":"uint256","indexed":false},{"name":"total_weight","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"VoteForGauge","inputs":[{"name":"time","type":"uint256","indexed":false},{"name":"user","type":"address","indexed":false},{"name":"gauge_addr","type":"address","indexed":false},{"name":"weight","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"NewGauge","inputs":[{"name":"addr","type":"address","indexed":false},{"name":"gauge_type","type":"int128","indexed":false},{"name":"weight","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"stateMutability":"nonpayable","type":"constructor","inputs":[{"name":"_voting_escrow","type":"address"},{"name":"_authorizer_adaptor","type":"address"}],"outputs":[]},{"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"voting_escrow","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"admin","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"gauge_exists","inputs":[{"name":"_addr","type":"address"}],"outputs":[{"name":"","type":"bool"}]},{"stateMutability":"view","type":"function","name":"gauge_types","inputs":[{"name":"_addr","type":"address"}],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"nonpayable","type":"function","name":"add_gauge","inputs":[{"name":"addr","type":"address"},{"name":"gauge_type","type":"int128"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"add_gauge","inputs":[{"name":"addr","type":"address"},{"name":"gauge_type","type":"int128"},{"name":"weight","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"checkpoint","inputs":[],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"checkpoint_gauge","inputs":[{"name":"addr","type":"address"}],"outputs":[]},{"stateMutability":"view","type":"function","name":"gauge_relative_weight","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"gauge_relative_weight","inputs":[{"name":"addr","type":"address"},{"name":"time","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"gauge_relative_weight_write","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"gauge_relative_weight_write","inputs":[{"name":"addr","type":"address"},{"name":"time","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"add_type","inputs":[{"name":"_name","type":"string"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"add_type","inputs":[{"name":"_name","type":"string"},{"name":"weight","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"change_type_weight","inputs":[{"name":"type_id","type":"int128"},{"name":"weight","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"change_gauge_weight","inputs":[{"name":"addr","type":"address"},{"name":"weight","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"vote_for_many_gauge_weights","inputs":[{"name":"_gauge_addrs","type":"address[8]"},{"name":"_user_weight","type":"uint256[8]"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"vote_for_gauge_weights","inputs":[{"name":"_gauge_addr","type":"address"},{"name":"_user_weight","type":"uint256"}],"outputs":[]},{"stateMutability":"view","type":"function","name":"get_gauge_weight","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"get_type_weight","inputs":[{"name":"type_id","type":"int128"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"get_total_weight","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"get_weights_sum_per_type","inputs":[{"name":"type_id","type":"int128"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"n_gauge_types","inputs":[],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"view","type":"function","name":"n_gauges","inputs":[],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"view","type":"function","name":"gauge_type_names","inputs":[{"name":"arg0","type":"int128"}],"outputs":[{"name":"","type":"string"}]},{"stateMutability":"view","type":"function","name":"gauges","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"vote_user_slopes","inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"address"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"slope","type":"uint256"},{"name":"power","type":"uint256"},{"name":"end","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"vote_user_power","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"last_user_vote","inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"points_weight","inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"uint256"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"bias","type":"uint256"},{"name":"slope","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"time_weight","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"points_sum","inputs":[{"name":"arg0","type":"int128"},{"name":"arg1","type":"uint256"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"bias","type":"uint256"},{"name":"slope","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"time_sum","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"points_total","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"time_total","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"points_type_weight","inputs":[{"name":"arg0","type":"int128"},{"name":"arg1","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"time_type_weight","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]}]')
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    id = web3.toChecksumAddress(id)
    try:
        result = contract.functions.gauge_relative_weight(id).call()
    except:
        result = 0
    return result
@st.cache_data
def get_all_weights():
    weights = []
    weight_values = []
    for key in lst_pools.keys():
        time.sleep(1)
        weights.append(int(getgaugeweight(lst_pools[key]))/10**18)
        weight_values.append(aurabal_price/10**18*result*int(getgaugeweight(lst_pools[key]))/10**18)
    return weights, weight_values

data = get_all_weights()
weights_list = data[0]
weight_values = data[1]
df = pd.DataFrame({"Pool": lst_pools.keys(), "Address": lst_pools.values(),"veBAl Weights":weights_list, "veBAL value":weight_values})
df = df.sort_values(by ="veBAl Weights", ascending=False)
df.loc[4] = df.loc[3] * 100
st.dataframe(df, width=None)
