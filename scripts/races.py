from political_sisterhood.races.models import Race, State
import pandas as pd
import os
import logging
import csv
logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run():
    data = pd.read_csv(os.path.join(ROOT_DIR, 'race.csv'))
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        try:
            state = row[0]
            name = row[1]
            race = row[2]
            filing = row[3]
            other = row[4]
            state = State.objects.get(state=state)
            Race.objects.get_or_create(state=state, district=name, race_type=race, filing_date=filing, other=other)
        except Exception as e:
            logger.warning(e)
