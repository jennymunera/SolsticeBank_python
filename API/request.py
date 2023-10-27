# %%
# this cell enables relative path imports
import os
from dotenv import load_dotenv
load_dotenv()

#%%
_PROJECT_PATH: str = os.environ["_project_path"]
_CSV_DATA_FILENAME: str = os.environ["_csv_data_filename"]
SOLSTICE_BANK: str = os.environ["solstice_bank"]
#%%
import sys
from pathlib import Path
project_path = Path(_PROJECT_PATH)
sys.path.append(str(project_path))

# %%
# import all your modules here
import time
import json
import pandas as pd

import API.config_v2 as cfg
from API.library_ubidots_v2 import Ubidots as ubi

# %%
# set your constants here
baseline=cfg.BASELINE
study=cfg.STUDY

# %%
df_devices = ubi.get_available_devices_v2(label=SOLSTICE_BANK, level='group', page_size=1000)

#%%
df_devices = df_devices[df_devices['device_label'].isin(['bc49','bc-291-las-palmas','bc37','bc38'])]

df_vars = ubi.get_available_variables(list(df_devices['device_id']))

# %%
df_vars = df_vars[df_vars['variable_label'].isin(cfg.WHITELISTED_VAR_LABELS)]
VAR_IDS_TO_REQUEST = list(df_vars['variable_id'])
VAR_ID_TO_LABEL = dict(zip(df_vars['variable_id'], df_vars['variable_label']))

# %%
CHUNK_SIZE = 10
DATE_INTERVAL_REQUEST = {'start': baseline[0], 'end': study[1]}
df = None
lst_responses = []
n_vars = len(VAR_IDS_TO_REQUEST)
print(f"Making request for the following interval: Baseline:{baseline}, Study:{study}")
for idx in range(0, ubi.ceildiv(len(VAR_IDS_TO_REQUEST), CHUNK_SIZE)):
    idx_start = idx * CHUNK_SIZE
    idx_end = (idx + 1) * CHUNK_SIZE
    chunk = VAR_IDS_TO_REQUEST[idx_start:idx_end]
    response = ubi.make_request(
        chunk, 
        DATE_INTERVAL_REQUEST, 
    )
    print("RESPUESTA : ",response.json())
    if response.status_code == 204 or response.status_code >= 500:
        print(f"Empty response for chunk {idx}")
        time.sleep(10)
        response = ubi.make_request(
        chunk, 
        DATE_INTERVAL_REQUEST,)
    current_idx = idx_end+1
    if (current_idx > n_vars):
        current_idx = n_vars
    print(f"Progress: {100*(current_idx)/n_vars:0.1f}%")
    print(f"Response status code: {response.status_code}")
    if (response.status_code != 204) and  (len(response.json()['results']) >0 ):
        lst_responses.append(response)
    else: 
        print(f"Empty response for chunk {idx}")
df = ubi.parse_response(lst_responses, VAR_ID_TO_LABEL)


# %%
#len(response.json()['results'][0][0])


# %%
#df.to_csv(f"{_CSV_DATA_FILENAME}", index=False)