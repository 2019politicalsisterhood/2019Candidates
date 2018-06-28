from political_sisterhood.races.models import Race, State
import pandas as pd
import os
import logging
from datetime import datetime
import csv
logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run():
    data = pd.read_csv(os.path.join(ROOT_DIR, 'new_races.csv'), keep_default_na=False)
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        try:
            state = row[1].strip()
            race_type = row[2]
            district = row[0]
            if row[3]:
                filing = row[3]
                filing = pd.to_datetime(filing)
            if row[4]:
                primary = row[4]
                primary = pd.to_datetime(primary)
            if row[5]:
                election = row[5]
                election = pd.to_datetime(election)
            state = State.objects.get(state=state)
            Race.objects.get_or_create(district=district,
                                       state=state,
                                       race_type=race_type,
                                       filing_date=filing,
                                       primary_date=primary,
                                       election_date=election)
        except Exception as e:
            error = "{}, {}".format(index, e)
            logger.warning(error)
