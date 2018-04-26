from political_sisterhood.candidate.models import Candidate, College
import pandas as pd
import os
import logging
import csv
logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run():
    data = pd.read_csv(os.path.join(ROOT_DIR, 'import.csv'), keep_default_na=False)
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        try:
            first = row[3]
            last = row[4]
            college = row[7]
            if college:
                college_lookup, create = College.objects.get_or_create(name=college)
                Candidate.objects.filter(first_name=first, last_name=last).update(college=college_lookup)
        except Exception as e:
            logger.warning(e, exc_info=True)
