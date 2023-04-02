import datetime
from main import *
from eth_utils import to_checksum_address

def get_pool_history(pool,timestamp):
    json_data = {
        'query': f'''
        query {{
            poolSnapshots(
                first: 1000,
                where: {{
                    pool: "{pool}",
                    timestamp_gt: {timestamp}
                }}
            ) {{
                pool {{
                    id
                }}
                liquidity
                timestamp
                amounts
                totalShares
                swapVolume
                swapFees
            }}
        }}
        ''',
    }
    response = requests.post('https://api.thegraph.com/subgraphs/name/balancer-labs/balancer-v2', json=json_data).json()
    return response['data']['poolSnapshots']

pool_dict = {
    'Balancer stETH Stable Pool':'0x32296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080',
    'Balancer rETH Stable Pool':'0x1e19cf2d73a72ef1332c882f20534b6519be0276000200000000000000000112',
    'Balancer cbETH-wstETH Stable Pool': '0x32296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080'
}

selected_option = st.selectbox('Select an option', list(pool_dict.keys()))

if selected_option:
    pool = pool_dict[selected_option]
    timestamp = 1628875520
    pool_data = get_pool_history(pool, timestamp)
    liquidity_list = []
    timestamp_list = []
    volume_list = [pool_data[0]['swapVolume']]
    for x, pool in enumerate(pool_data):
        liquidity_list.append(pool['liquidity'])
        timestamp_list.append(datetime.datetime.fromtimestamp(pool['timestamp']))
        try:
            volume_list.append(float(pool_data[x + 1]['swapVolume']) - float(pool_data[x]['swapVolume']))
        except:
            continue

    fig1 = px.line(x=timestamp_list, y=volume_list, labels={'x': 'Date', 'y': 'stETH/WETH Pool Volume'})
    fig1.update_layout(xaxis_tickangle=60)
    st.plotly_chart(fig1)
    fig2 = px.line(x=timestamp_list, y=liquidity_list, labels={'x': 'Date', 'y': 'stETH/WETH liquidity'})
    fig2.update_layout(xaxis_tickangle=60)
    st.plotly_chart(fig2)
