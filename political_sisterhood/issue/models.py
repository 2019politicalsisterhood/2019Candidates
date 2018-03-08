from django.db import models
from political_sisterhood.candidate.models import Candidate
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor.fields import RichTextField


# Create your models here.
class Issue(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

    class MPTTMeta:
        order_insertion_by = ['name']

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