from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.BooleanField(default=False, verbose_name='Is Task Done?')
    created = models.DateTimeField(auto_now_add=True)
    assigned = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='+')
    done_by = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name='+')
    done_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(str(self.id), self.name)
