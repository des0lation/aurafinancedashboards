from main import *
import statistics,requests, json, time

def gettotalvebal():
    infura_url = "https://mainnet.infura.io/v3/0159c1c270174247ab17c4839f766798"
    web3 = Web3(HTTPProvider(infura_url))
    contract_address = '0xC128a9954e6c874eA3d62ce62B468bA073093F25'
    contract_abi = json.loads(
        '[{"name":"Deposit","inputs":[{"name":"provider","type":"address","indexed":true},{"name":"value","type":"uint256","indexed":false},{"name":"locktime","type":"uint256","indexed":true},{"name":"type","type":"int128","indexed":false},{"name":"ts","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"Withdraw","inputs":[{"name":"provider","type":"address","indexed":true},{"name":"value","type":"uint256","indexed":false},{"name":"ts","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"Supply","inputs":[{"name":"prevSupply","type":"uint256","indexed":false},{"name":"supply","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"stateMutability":"nonpayable","type":"constructor","inputs":[{"name":"token_addr","type":"address"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_authorizer_adaptor","type":"address"}],"outputs":[]},{"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"name","inputs":[],"outputs":[{"name":"","type":"string"}]},{"stateMutability":"view","type":"function","name":"symbol","inputs":[],"outputs":[{"name":"","type":"string"}]},{"stateMutability":"view","type":"function","name":"decimals","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"admin","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"nonpayable","type":"function","name":"commit_smart_wallet_checker","inputs":[{"name":"addr","type":"address"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"apply_smart_wallet_checker","inputs":[],"outputs":[]},{"stateMutability":"view","type":"function","name":"get_last_user_slope","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"view","type":"function","name":"user_point_history__ts","inputs":[{"name":"_addr","type":"address"},{"name":"_idx","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"locked__end","inputs":[{"name":"_addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"checkpoint","inputs":[],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"deposit_for","inputs":[{"name":"_addr","type":"address"},{"name":"_value","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"create_lock","inputs":[{"name":"_value","type":"uint256"},{"name":"_unlock_time","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"increase_amount","inputs":[{"name":"_value","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"increase_unlock_time","inputs":[{"name":"_unlock_time","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"withdraw","inputs":[],"outputs":[]},{"stateMutability":"view","type":"function","name":"balanceOf","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"balanceOf","inputs":[{"name":"addr","type":"address"},{"name":"_t","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"balanceOfAt","inputs":[{"name":"addr","type":"address"},{"name":"_block","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"totalSupply","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"totalSupply","inputs":[{"name":"t","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"totalSupplyAt","inputs":[{"name":"_block","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"supply","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"locked","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"amount","type":"int128"},{"name":"end","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"epoch","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"point_history","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"bias","type":"int128"},{"name":"slope","type":"int128"},{"name":"ts","type":"uint256"},{"name":"blk","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"user_point_history","inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"uint256"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"bias","type":"int128"},{"name":"slope","type":"int128"},{"name":"ts","type":"uint256"},{"name":"blk","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"user_point_epoch","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"slope_changes","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"view","type":"function","name":"future_smart_wallet_checker","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"smart_wallet_checker","inputs":[],"outputs":[{"name":"","type":"address"}]}]')
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    totalveBAL = contract.functions.totalSupply().call()
    return totalveBAL

def getaurabal():
    contract_address_2 = '0x616e8BfA43F920657B3497DBf40D6b1A02D4608d'
    contract_abi_2 = json.loads(
        '[{"inputs":[{"internalType":"string","name":"_nameArg","type":"string"},{"internalType":"string","name":"_symbolArg","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"operator","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_operator","type":"address"}],"name":"setOperator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]')
    contract2 = web3.eth.contract(address=contract_address_2, abi=contract_abi_2)
    auraveBAL = contract2.functions.totalSupply().call()
    return auraveBAL


totalveBAL = gettotalvebal()
auraveBAL = getaurabal()
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

    vlaurabal = float(requests.post('https://graph.aura.finance/subgraphs/name/aura/aura-mainnet-v1',json=json_data).json()['data']['auraLocker']['lockedSupply'])/10**18
    return vlaurabal

total_vl_aura = getvlaura()

#Here I am declaring all the LST POOLs

bal_price = get_bal_price()
aurabal_price = get_aurabal_price()
lsts = ['stETH', 'wstETH', 'cbETH', 'staFiETH', 'ankrETH', 'rETH','sfrxETH']
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

def getgaugeweight(id):
    infura_url = "https://mainnet.infura.io/v3/0159c1c270174247ab17c4839f766798"
    web3 = Web3(HTTPProvider(infura_url))
    contract_address = '0xC128468b7Ce63eA702C1f104D55A2566b13D3ABD'
    contract_abi = json.loads('[{"name":"AddType","inputs":[{"name":"name","type":"string","indexed":false},{"name":"type_id","type":"int128","indexed":false}],"anonymous":false,"type":"event"},{"name":"NewTypeWeight","inputs":[{"name":"type_id","type":"int128","indexed":false},{"name":"time","type":"uint256","indexed":false},{"name":"weight","type":"uint256","indexed":false},{"name":"total_weight","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"NewGaugeWeight","inputs":[{"name":"gauge_address","type":"address","indexed":false},{"name":"time","type":"uint256","indexed":false},{"name":"weight","type":"uint256","indexed":false},{"name":"total_weight","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"VoteForGauge","inputs":[{"name":"time","type":"uint256","indexed":false},{"name":"user","type":"address","indexed":false},{"name":"gauge_addr","type":"address","indexed":false},{"name":"weight","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"name":"NewGauge","inputs":[{"name":"addr","type":"address","indexed":false},{"name":"gauge_type","type":"int128","indexed":false},{"name":"weight","type":"uint256","indexed":false}],"anonymous":false,"type":"event"},{"stateMutability":"nonpayable","type":"constructor","inputs":[{"name":"_voting_escrow","type":"address"},{"name":"_authorizer_adaptor","type":"address"}],"outputs":[]},{"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"voting_escrow","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"admin","inputs":[],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"gauge_exists","inputs":[{"name":"_addr","type":"address"}],"outputs":[{"name":"","type":"bool"}]},{"stateMutability":"view","type":"function","name":"gauge_types","inputs":[{"name":"_addr","type":"address"}],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"nonpayable","type":"function","name":"add_gauge","inputs":[{"name":"addr","type":"address"},{"name":"gauge_type","type":"int128"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"add_gauge","inputs":[{"name":"addr","type":"address"},{"name":"gauge_type","type":"int128"},{"name":"weight","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"checkpoint","inputs":[],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"checkpoint_gauge","inputs":[{"name":"addr","type":"address"}],"outputs":[]},{"stateMutability":"view","type":"function","name":"gauge_relative_weight","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"gauge_relative_weight","inputs":[{"name":"addr","type":"address"},{"name":"time","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"gauge_relative_weight_write","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"gauge_relative_weight_write","inputs":[{"name":"addr","type":"address"},{"name":"time","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"nonpayable","type":"function","name":"add_type","inputs":[{"name":"_name","type":"string"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"add_type","inputs":[{"name":"_name","type":"string"},{"name":"weight","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"change_type_weight","inputs":[{"name":"type_id","type":"int128"},{"name":"weight","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"change_gauge_weight","inputs":[{"name":"addr","type":"address"},{"name":"weight","type":"uint256"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"vote_for_many_gauge_weights","inputs":[{"name":"_gauge_addrs","type":"address[8]"},{"name":"_user_weight","type":"uint256[8]"}],"outputs":[]},{"stateMutability":"nonpayable","type":"function","name":"vote_for_gauge_weights","inputs":[{"name":"_gauge_addr","type":"address"},{"name":"_user_weight","type":"uint256"}],"outputs":[]},{"stateMutability":"view","type":"function","name":"get_gauge_weight","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"get_type_weight","inputs":[{"name":"type_id","type":"int128"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"get_total_weight","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"get_weights_sum_per_type","inputs":[{"name":"type_id","type":"int128"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"n_gauge_types","inputs":[],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"view","type":"function","name":"n_gauges","inputs":[],"outputs":[{"name":"","type":"int128"}]},{"stateMutability":"view","type":"function","name":"gauge_type_names","inputs":[{"name":"arg0","type":"int128"}],"outputs":[{"name":"","type":"string"}]},{"stateMutability":"view","type":"function","name":"gauges","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}]},{"stateMutability":"view","type":"function","name":"vote_user_slopes","inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"address"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"slope","type":"uint256"},{"name":"power","type":"uint256"},{"name":"end","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"vote_user_power","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"last_user_vote","inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"points_weight","inputs":[{"name":"arg0","type":"address"},{"name":"arg1","type":"uint256"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"bias","type":"uint256"},{"name":"slope","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"time_weight","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"points_sum","inputs":[{"name":"arg0","type":"int128"},{"name":"arg1","type":"uint256"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"bias","type":"uint256"},{"name":"slope","type":"uint256"}]}]},{"stateMutability":"view","type":"function","name":"time_sum","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"points_total","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"time_total","inputs":[],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"points_type_weight","inputs":[{"name":"arg0","type":"int128"},{"name":"arg1","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]},{"stateMutability":"view","type":"function","name":"time_type_weight","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"uint256"}]}]')
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    id = web3.toChecksumAddress(id)
    try:
        totalveBAL = contract.functions.gauge_relative_weight(id).call()
    except:
        totalveBAL = 0
    return totalveBAL

lst_pools['B-cbETH-wstETH-Stable-gauge'] = '0x01a9502c11f411b494c62746d37e89d6f7078657'


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
        weight_values.append(round(aurabal_price/10**18*totalveBAL*int(gauge_weight)/10**18,2))
        ve_bals.append(totalveBAL/10**18*int(gauge_weight)/10**18)
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

if "50rETH-50bb-euler-USD-gauge" in lst_pools.keys():
    del lst_pools["50rETH-50bb-euler-USD-gauge"]
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
extracted_lst_pools = ['B-stETH-STABLE-gauge','B-rETH-STABLE-gauge','B-ankrETH-WETH-Stable-gauge','B-staFiETH-WETH-Stable-gauge','wstETH-rETH-sfrxETH-BPT-gauge','B-cbETH-wstETH-Stable-gauge']
for i,weight in enumerate(weights_list):
    try:
        if list(lst_pools.keys())[i] in extracted_lst_pools:
            justlstsavg.append(pools_liquidity[i]/(100*weight))
    except:
        continue

#st.write(pools_liquidity)
#st.write("From the Pools Collect, each % of veBAL is on median generating",statistics.median(avgliqpervebal),"of liquidity")
#st.write("So we are rougly generating $1 million of liquidity per % of veBAL we are owning which has a market value of",0.01 * aurabal_price* totalveBAL/10**18)
st.write("Looking at just LST metastable pools",extracted_lst_pools,"we get an average of", statistics.mean(justlstsavg),"$ of liquidity per % of veBAL held by the pool")

veBAL_values = list(range(0, 11))
liquidity = [statistics.mean(justlstsavg) * i for i in veBAL_values]
fig = px.line(x=veBAL_values, y=liquidity, labels={'x': '% of veBAL', 'y': 'Liquidity'})
st.plotly_chart(fig)

investment = st.slider('Select an investment amount', min_value=1, max_value=10000000,value = 1000000, step=1000,format='%.2f')
st.empty()
tvl = st.slider('Select a TVL', min_value=1, max_value=100000000,value = 100000000 ,step=100000,format='%.2f')
st.empty()
bribes = st.slider("Bribing?",min_value = 0 , max_value = 20000,step = 1000,format='%.2f')
st.write("This would lead to a bribing expense of",bribes*52,"$ per year")
st.write("For each dollar of bribes you are getting",votes_per_dollar,"votes")
st.empty()
auralockpercentage = st.slider("How much of AURA minted each week is being deposited into vlAURA?",min_value = 0,max_value = 100,format='%.2f')
st.empty()
new_aura_investments = st.slider("How much AURA will be buy each week to combat vlAURA dilution",min_value = 0,max_value = 10000,format='%.2f')
vl_aura_amount = bribes*votes_per_dollar+investment/aura_price
voting_power = vl_aura_amount/(total_vl_aura+vl_aura_amount)*auraveBAL / 10 ** 18
vebal_percentage = 100*voting_power/(totalveBAL / 10 ** 18)
supported_liquidity = st.slider("Supported Liquidity", min_value = 1, max_value = tvl,step = 100000 ,value = int((vebal_percentage * statistics.mean(justlstsavg))),format='%.2f')
tvl_ratio = str("1" + ":" + str((int(tvl) -supported_liquidity) /supported_liquidity))
st.write('You invested:', investment, "netting you",vl_aura_amount,"vlAURA")
st.write("This will mean you own",100*vl_aura_amount/(total_vl_aura+vl_aura_amount),"% of vlAURA, a veBAL voting power of",voting_power, "or",vebal_percentage,"%")
st.write("This is projected to support",vebal_percentage * statistics.mean(justlstsavg),"dollars of liquidity, a tvl ratio of",tvl_ratio)

liq_aura_earned = []
aprs = []
running_total = 0
voting_power_loss = []
dilutions = []
auraDominance = 100 * auraveBAL / totalveBAL
#aura_revenue.append(balEarned * st.session_state.aura_share * bal_price) this is the bal earned by AURA in main.py

for i,auraearned in enumerate(aura_revenue):
    total_vl_aura = total_vl_aura + auraearned * auralockpercentage/100
    vl_aura_amount = vl_aura_amount + new_aura_investments
    voting_power = vl_aura_amount/total_vl_aura* totalveBAL / 10 ** 18 #vl Aura % held
    vebal_percentage = 100 * voting_power / (totalveBAL / 10 ** 18)
    running_total += auraearned * vebal_percentage/100
    dilutions.append((52*100*auraearned * auralockpercentage/100)/total_vl_aura)
    aprs.append(100*52*((aura_price*auraMinted[i] +auraDominance * 0.75 * float(dfmain['Bal Released'][i]) * bal_price) * vebal_percentage/100)/supported_liquidity)
    liq_aura_earned.append(running_total)

col1, col2 = st.columns(2)
weeks = dfmain['Weeks']

with col1:
    fig2 = px.line(x=weeks, y=liq_aura_earned, labels={'x': 'Weeks', 'y': 'Aura Earned by Liquidity Pool'})
    fig2.update_layout(xaxis_tickangle = 60)
    st.plotly_chart(fig2)
with col2:
    fig3 = px.line(x=weeks, y=aprs, labels={'x': 'Weeks', 'y': 'APR'})
    fig3.update_layout(xaxis_tickangle = 60)
    st.plotly_chart(fig3)

fig4 = px.line(x=weeks, y=dilutions, labels={'x': 'Weeks', 'y': 'Annualised Dilution'})
fig4.update_layout(xaxis_tickangle = 60)
st.plotly_chart(fig4)


