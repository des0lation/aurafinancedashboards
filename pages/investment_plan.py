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
for pool in pool_data:
    liquidity_list.append(pool['liquidity'])
    timestamp_list.append(datetime.datetime.fromtimestamp(pool['timestamp']))

data = {'timestamp': timestamp_list, 'liquidity': liquidity_list}

# create a pandas DataFrame from the data dictionary
df = pd.DataFrame(data)

# set the timestamp column as the index of the DataFrame
df.set_index('timestamp', inplace=True)

# plot the DataFrame using Streamlit's line_chart function
st.line_chart(df)

