from political_sisterhood.candidate.models import Candidate, College
from political_sisterhood.issue.models import Issue, CandidateIssue
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
            iss1 = row[9]
            iss2 = row[10]
            iss3 = row[11]
            can = Candidate.objects.get(first_name=first, last_name=last)
            issue1, get = Issue.objects.get_or_create(name=iss1)
            issue2, get = Issue.objects.get_or_create(name=iss2)
            issue3, get = Issue.objects.get_or_create(name=iss3)
            CandidateIssue.objects.create(candidate=can, issue=issue1)
            CandidateIssue.objects.create(candidate=can, issue=issue2)
            CandidateIssue.objects.create(candidate=can, issue=issue3)
        except Exception as e:
            logger.info(index)
