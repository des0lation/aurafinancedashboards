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
    ve_bals = []
    weights = []
    weight_values = []
    st.write(len(lst_pools.keys()))
    for key in lst_pools.keys():
        time.sleep(1)
        gauge_weight = getgaugeweight(lst_pools[key])
        st.write(gauge_weight)
        weights.append(int(gauge_weight)/10**18)
        weight_values.append(aurabal_price/10**18*result*int(gauge_weight)/10**18)
        ve_bals.append(result/10**18*int(gauge_weight)/10**18)
    return weights, weight_values,ve_bals


json_data = {
    'query': 'query AllPools($skip: Int, $first: Int, $orderBy: Pool_orderBy, $orderDirection: OrderDirection, $where: Pool_filter, $block: Block_height) {\n  pool0: pools(\n    first: 1000\n    orderBy: $orderBy\n    orderDirection: $orderDirection\n    where: $where\n    block: $block\n  ) {\n    ...SubgraphPool\n  }\n  pool1000: pools(\n    first: 1000\n    skip: 1000\n    orderBy: $orderBy\n    orderDirection: $orderDirection\n    where: $where\n    block: $block\n  ) {\n    ...SubgraphPool\n  }\n  pool2000: pools(\n    first: 1000\n    skip: 2000\n    orderBy: $orderBy\n    orderDirection: $orderDirection\n    where: $where\n    block: $block\n  ) {\n    ...SubgraphPool\n  }\n}\n\nfragment SubgraphPool on Pool {\n  id\n  address\n  poolType\n  poolTypeVersion\n  factory\n  strategyType\n  symbol\n  name\n  swapEnabled\n  swapFee\n  protocolYieldFeeCache\n  protocolSwapFeeCache\n  owner\n  totalWeight\n  totalSwapVolume\n  totalSwapFee\n  totalLiquidity\n  totalShares\n  tokens(first: 100, orderBy: index) {\n    ...SubgraphPoolToken\n  }\n  swapsCount\n  holdersCount\n  tokensList\n  amp\n  priceRateProviders(first: 100) {\n    ...SubgraphPriceRateProvider\n  }\n  expiryTime\n  unitSeconds\n  createTime\n  principalToken\n  baseToken\n  wrappedIndex\n  mainIndex\n  lowerTarget\n  upperTarget\n  sqrtAlpha\n  sqrtBeta\n  root3Alpha\n  isInRecoveryMode\n}\n\nfragment SubgraphPoolToken on PoolToken {\n  id\n  symbol\n  name\n  decimals\n  address\n  balance\n  managedBalance\n  weight\n  priceRate\n  isExemptFromYieldProtocolFee\n  token {\n    ...TokenTree\n  }\n}\n\nfragment TokenTree on Token {\n  latestUSDPrice\n  pool {\n    ...SubgraphSubPool\n    tokens(first: 100, orderBy: index) {\n      ...SubgraphSubPoolToken\n      token {\n        latestUSDPrice\n        pool {\n          ...SubgraphSubPool\n          tokens(first: 100, orderBy: index) {\n            ...SubgraphSubPoolToken\n            token {\n              latestUSDPrice\n              pool {\n                ...SubgraphSubPool\n              }\n            }\n          }\n        }\n      }\n    }\n  }\n}\n\nfragment SubgraphSubPool on Pool {\n  id\n  totalShares\n  address\n  poolType\n  mainIndex\n}\n\nfragment SubgraphSubPoolToken on PoolToken {\n  address\n  balance\n  weight\n  priceRate\n  symbol\n  decimals\n  isExemptFromYieldProtocolFee\n}\n\nfragment SubgraphPriceRateProvider on PriceRateProvider {\n  address\n  token {\n    address\n  }\n}\n',
    'variables': {
        'orderBy': 'totalLiquidity',
        'orderDirection': 'desc',
        'where': {
            'swapEnabled': True,
            'totalShares_gt': 1e-12,
        },
    },
    'operationName': 'AllPools',
}

bal_pools = requests.post('https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2', json=json_data).json()['data']

data = get_all_weights()
weights_list = data[0]
weight_values = data[1]
ve_bals = data[2]

founds_symbols = []
bal_pools_keys = bal_pools.keys()
pools_liquidity = []

for key in bal_pools_keys:
    pools_x = bal_pools[key]
    for pool in pools_x:
        if str(pool['symbol']+'-gauge') in lst_pools.keys():
            founds_symbols.append(str(pool['symbol']+'-gauge'))
            pools_liquidity.append(pool['totalLiquidity'])

st.write(len(founds_symbols),len(lst_pools.keys()),len(lst_pools.values()),len(weights_list),len(ve_bals),len(weight_values),len(pools_liquidity))


df = pd.DataFrame({"Pool": lst_pools.keys(), "Address": lst_pools.values(),"veBAL Weights":weights_list,"veBAL":ve_bals, "veBAL value":weight_values,"Liquidity":pools_liquidity})
df = df.sort_values(by ="veBAL Weights", ascending=False)
df['Liquidity per veBAL'] = df['veBAL']/df['veBAL Weights']
df["veBAL Weights"] = df["veBAL Weights"] * 100

st.dataframe(df, width=None)


