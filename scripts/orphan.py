from political_sisterhood.issue.models import Issue
import pandas as pd
import os
import logging
import csv
logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def run():
    data = pd.read_csv(os.path.join(ROOT_DIR, 'orphans.csv'), keep_default_na=False)
    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        try:
            issue_id = row[0]
            parent = row[1]
            og = Issue.objects.get(id=issue_id)
            try:
                exists = Issue.objects.get(name=parent)
            except:
                exists = Issue.objects.create(name=parent)
            og.parent = exists
            og.save()
        except Exception as e:
            logger.info(e, exc_info=True)
            logger.info(issue_id)
