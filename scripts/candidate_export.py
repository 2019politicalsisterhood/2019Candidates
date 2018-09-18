from political_sisterhood.candidate.models import Candidate
import csv
import os
import logging
import boto3

logger = logging.getLogger(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
AWS_ACCESS_KEY_ID = os.environ['DJANGO_AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['DJANGO_AWS_SECRET_ACCESS_KEY']
AWS_MEDIA_BUCKET = os.environ['DJANGO_AWS_STORAGE_BUCKET_NAME']
session = boto3.Session(
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        )


def run():
    with open('candidate_export.csv', mode='w') as candidate_export:
        csv_writer = csv.writer(candidate_export, delimiter=',',
                                quotechar='"')
        csv_writer.writerow(['Id', 'Candidate Name',
                             'Candidate Party', 'State',
                             'Race Title',
                             'Race Type',
                             'Issue 1', 'Issue 2',
                             'Issue 3'])
        for can in Candidate.objects.all():
            results = []
            race_type = ""
            race_title = ""
            issues = ""
            results.append(can.id)
            results.append(can.name)
            results.append(can.party)
            results.append(can.state)
            if can.race:
                race_title = can.race.title
                race_type = can.race.race_type
            results.append(race_title)
            results.append(race_type)
            for issue in can.issues.all():
                results.append(issue.name)
            csv_writer.writerow(results)
    s3 = session.resource('s3')
    s3.meta.client.upload_file('candidate_export.csv',
                               AWS_MEDIA_BUCKET,
                               'candidate_export.csv')
