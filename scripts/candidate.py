from political_sisterhood.candidate.models import Candidate
import pandas as pd
import os
import logging
import csv
logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run():
    data = pd.read_csv(os.path.join(ROOT_DIR, 'candidate.csv'), keep_default_na=False)
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        try:
            unique = row[0]
            first = row[1]
            last = row[2]
            full = row[3]
            party = row[4]
            Candidate.objects.create(unique_identifier=unique,
                                     first_name=first, last_name=last,
                                     full=full, party=party)
        except Exception as e:
            logger.warning(e, exc_info=True)
