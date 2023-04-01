from main import *
import statistics,requests, json, time, datetime

pool = '0x32296969ef14eb0c6d29669c550d4a0449130230000200000000000000000080'
timestamp = 1628875520

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

pool_data = get_pool_history(pool,timestamp)

liquidity_list = []
timestamp_list = []
volume_list = []
for pool in pool_data:
    liquidity_list.append(pool['liquidity'])
    timestamp_list.append(datetime.datetime.fromtimestamp(pool['timestamp']))
    volume_list.append(pool['swapVolume'])

fig1 = px.line(x=timestamp_list, y=volume_list, labels={'x': 'Date', 'y': 'stETH/WETH liquidity'})
fig1.update_layout(xaxis_tickangle=60)
st.plotly_chart(fig1)
fig2 = px.line(x=timestamp_list, y=liquidity_list, labels={'x': 'Date', 'y': 'stETH/WETH liquidity'})
fig2.update_layout(xaxis_tickangle = 60)
st.plotly_chart(fig2)

