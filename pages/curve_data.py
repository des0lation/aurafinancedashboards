from main import *

json_data = {
    'pool': 'steth'
}

st_eth_data = requests.post('https://api.llama.airforce//curvepoolsnapshots', json=json_data).json()['data']

curve_emmissions_list = []
dollar_emmissions_list = []
for snapshot in st_eth_data['emmissionSnapshots']:
    emmissions_list.append(snapshot['crvAmount'])
    dollar_emmissions_list.append(snapshot['value'])








