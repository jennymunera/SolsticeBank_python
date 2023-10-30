# %%
# this cell enables relative path imports
import os
from dotenv import load_dotenv
import time
import json
import pandas as pd

from API.library_ubidots_v2 import Ubidots as ubi

SOLSTICE_BANK: str = os.environ["solstice_bank"]
load_dotenv()

LST_VAR = [
    "ilu-consumo-activa",
    "aa-consumo-activa",
    "front-consumo-activa",
    "front-tension-3",
    "front-tension-2",
    "front-tension-1"]

LST_DVC = ['bc49','bc-291-las-palmas','bc37','bc38']
    
# time = ['2023-10-20','2023-10-21']


def request(Time, LST_VAR, LST_DVC):
    df_devices = ubi.get_available_devices_v2(label=SOLSTICE_BANK, level='group', page_size=1000)
    df_devices = df_devices[df_devices['device_label'].isin(LST_DVC)]
    df_vars = ubi.get_available_variables(list(df_devices['device_id']))
    df_vars = df_vars[df_vars['variable_label'].isin(LST_VAR)]
    VAR_IDS_TO_REQUEST = list(df_vars['variable_id'])
    VAR_ID_TO_LABEL = dict(zip(df_vars['variable_id'], df_vars['variable_label']))
    DATE_INTERVAL_REQUEST = {'start': Time[0], 'end': Time[1]}
    df = None
    lst_responses = []
    
    response = ubi.make_request(
        VAR_IDS_TO_REQUEST, 
        DATE_INTERVAL_REQUEST)

    lst_responses.append(response)

    df = ubi.parse_response(lst_responses, VAR_ID_TO_LABEL)

    df.to_csv('API/datos.csv')

    return df

# %%

# request(time, LST_VAR, LST_DVC)
# %%
