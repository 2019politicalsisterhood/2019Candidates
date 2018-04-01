from political_sisterhood.races.models import Race, State
import pandas as pd
import os
import logging
import csv
logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run():
    data = pd.read_csv(os.path.join(ROOT_DIR, 'states.csv'))
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        try:
            state = row[0]
            seal = row[1]
            State.objects.get_or_create(state=state, seal=seal)
        except Exception as e:
            logger.warning(e)
