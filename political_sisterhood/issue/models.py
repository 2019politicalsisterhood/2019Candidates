from django.db import models
from political_sisterhood.candidate.models import Candidate
from ckeditor.fields import RichTextField


# Create your models here.
class Issue(models.Model):
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class CandidateIssue(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="issues")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    desc = RichTextField(blank=True)

    @property
    def name(self):
        return self.issue.name

    def __str__(self):
        return "{} - {}".format(self.candidate, self.issue)