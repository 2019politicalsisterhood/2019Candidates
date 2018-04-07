from political_sisterhood.candidate.models import Candidate
import pandas as pd
import os
import logging
import csv
logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run():
    data = pd.read_csv(os.path.join(ROOT_DIR, 'candidate_state.csv'), keep_default_na=False)
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        try:
            first = row[0]
            last = row[1]
            state = row[2]
            candidate = Candidate.objects.filter(first_name=first, last_name=last)
            if not candidate:
                print(first + " " +last)
            candidate.update(state=state)
        except Exception as e:
            logger.warning(e, exc_info=True)
