import string

from main import *
import statistics,requests, json, time

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
sheet_url = "https://docs.google.com/spreadsheets/d/19tHankEKBCKLa3WSBf-X4LmAh0to9HhLV7Q8UBavHqg/gviz/tq?tqx=out:csv"
dfmain = pd.read_csv(sheet_url)

@st.cache_data()
def getvlaura():
    json_data = {
        'operationName': 'AuraV1',
        'variables': {
            'accountId': '',
            'hasAccount': False,
        },
        'query': 'query AuraV1($accountId: String!, $hasAccount: Boolean!) {\n  ...Block\n  poolAccounts(where: {staked_gt: 0, account: $accountId}) @include(if: $hasAccount) {\n    id\n    __typename\n  }\n  auraLocker(id: "auraLocker") {\n    ...AllAuraLocker\n    accounts(where: {account: $accountId}) @include(if: $hasAccount) {\n      id\n      balance\n      balanceLocked\n      balanceNextUnlockIndex\n      delegate {\n        id\n        __typename\n      }\n      userLocks {\n        id\n        amount\n        unlockTime\n        __typename\n      }\n      userData {\n        id\n        token {\n          ...AllToken\n          __typename\n        }\n        rewards\n        rewardPerTokenPaid\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Block on Query {\n  _meta {\n    block {\n      number\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment AllAuraLocker on AuraLocker {\n  id\n  address\n  lockedSupply\n  totalLocked: totalSupply\n  rewardData {\n    id\n    token {\n      ...AllToken\n      __typename\n    }\n    periodFinish\n    lastUpdateTime\n    rewardPerTokenStored\n    rewardRate\n    __typename\n  }\n  __typename\n}\n\nfragment AllToken on Token {\n  id\n  decimals\n  symbol\n  name\n  __typename\n}',
    }
    headers = {
        'authority': 'graph.aura.finance',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://app.aura.finance',
        'referer': 'https://app.aura.finance/',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }

    vlaurabal = float(requests.post('https://graph.aura.finance/subgraphs/name/aura/aura-mainnet-v1',headers=headers,json=json_data).json()['data']['auraLocker']['lockedSupply'])/10**18
    return vlaurabal

total_vl_aura = getvlaura()

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
if "50wstETH-50bb-euler-USD-gauge" in lst_pools.keys():
    del lst_pools["50wstETH-50bb-euler-USD-gauge"]
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
def get_all_weights(lst_pools):
    ve_bals = []
    weights = []
    weight_values = []
    if "50wstETH-50bb-euler-USD-gauge" in lst_pools.keys():
        del lst_pools["50wstETH-50bb-euler-USD-gauge"]
    for key in lst_pools.keys():
        time.sleep(1)
        gauge_weight = getgaugeweight(lst_pools[key])
        weights.append(int(gauge_weight)/10**18)
        weight_values.append(round(aurabal_price/10**18*result*int(gauge_weight)/10**18,2))
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

data = get_all_weights(lst_pools)
weights_list = data[0]
weight_values = data[1]
ve_bals = data[2]

bal_pools_keys = bal_pools.keys()

liq_dict = {}
for key in bal_pools_keys:
    pools_x = bal_pools[key]
    for pool in pools_x:
        if str(pool['symbol']+'-gauge') in lst_pools.keys():
            liq_dict[str(pool['symbol']+'-gauge')] = round(float(pool['totalLiquidity']),2)



pools_liquidity = []
#st.write(sorted(lst_pools.keys()))
#st.write(sorted(liq_dict.keys()))

if "B-wstETH-STABLE-C-gauge" in lst_pools.keys():
    del lst_pools["B-wstETH-STABLE-C-gauge"]

for key in lst_pools.keys():
    pools_liquidity.append(liq_dict[key])

liquidity_per_vebal = []
avgliqpervebal = []
for i in range(0,len(weights_list)):
    try:
        liquidity_per_vebal.append(round(float(pools_liquidity[i])/float(ve_bals[i]),2))
    except:
        liquidity_per_vebal.append(0)

for i, weight in enumerate(weights_list):
    try:
        avgliqpervebal.append(pools_liquidity[i] / (100 * weight))
    except:
        continue

df = pd.DataFrame({"Pool": lst_pools.keys(), "Address": lst_pools.values(),"veBAL Weights":weights_list,"veBAL":ve_bals, "veBAL value":weight_values,"Liquidity":pools_liquidity,"Liquidity per veBAL":liquidity_per_vebal})
df["veBAL Weights"] = df["veBAL Weights"] * 100
st.dataframe(df, width=None)

justlstsavg = []
extracted_lst_pools = ['B-stETH-STABLE-gauge','B-rETH-STABLE-gauge','B-cbETH-wstETH-Stable-gauge','B-ankrETH-WETH-Stable-gauge','B-staFiETH-WETH-Stable-gauge']
for i,weight in enumerate(weights_list):
    try:
        if list(lst_pools.keys())[i] in extracted_lst_pools:
            justlstsavg.append(pools_liquidity[i]/(100*weight))
    except:
        continue

#st.write(pools_liquidity)
#st.write("From the Pools Collect, each % of veBAL is on median generating",statistics.median(avgliqpervebal),"of liquidity")
#st.write("So we are rougly generating $1 million of liquidity per % of veBAL we are owning which has a market value of",0.01 * aurabal_price* result/10**18)
st.write("Looking at just LST metastable pools",extracted_lst_pools,"we get an average of", statistics.mean(justlstsavg))

veBAL_values = list(range(0, 11))
liquidity = [statistics.mean(justlstsavg) * i for i in veBAL_values]
fig = px.line(x=veBAL_values, y=liquidity, labels={'x': '% of veBAL', 'y': 'Liquidity'})
st.plotly_chart(fig)

investment = st.slider('Select an investment amount', min_value=1, max_value=10000000,value = 1000000, step=1000)
tvl = st.slider('Select a TVL', min_value=1, max_value=100000000,value = 100000000 ,step=100000)
vl_aura_amount = investment/aura_price
voting_power = vl_aura_amount/(total_vl_aura+vl_aura_amount)*result2 / 10 ** 18
vebal_percentage = 100*voting_power/(result / 10 ** 18)
supported_liquidity = int((vebal_percentage * statistics.mean(justlstsavg)))
tvl_ratio = str("1" + ":" + str((int(tvl) -supported_liquidity) /supported_liquidity))
st.write('You invested:', investment, "netting you",vl_aura_amount,"vlAURA")
st.write("This will mean you own",100*vl_aura_amount/(total_vl_aura+vl_aura_amount),"% of vlAURA, a veBAL voting power of",voting_power, "or",vebal_percentage,"%")
st.write("This is projected to support",vebal_percentage * statistics.mean(justlstsavg),"dollars of liquidity, a tvl ratio of",tvl_ratio)

liq_aura_earned = []
aprs = []
running_total = 0
for auraearned in aura_revenue:
    running_total += auraearned * vebal_percentage/100
    aprs.append(52*(aura_price*auraearned * vebal_percentage/100)/supported_liquidity)
    liq_aura_earned.append(running_total)

weeks = dfmain['Weeks']
fig2 = px.line(x=weeks, y=liq_aura_earned, labels={'x': 'Weeks', 'y': 'Aura Earned by Liquidity Pool'})
st.plotly_chart(fig2)

fig3 = px.line(x=weeks, y=liq_aura_earned, labels={'x': 'Weeks', 'y': 'APR'})
st.plotly_chart(fig3)




