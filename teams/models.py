from accounts.models import CustomUser
from django.db import models

class TeamModels(models.Model):
    team_id = models.AutoField('チームID',primary_key=True)
    name = models.CharField('名前',max_length=24,)
    description = models.CharField('説明',max_length=100,)
    members = models.ManyToManyField(CustomUser, related_name='teams')
    creator = models.ForeignKey(CustomUser, related_name='created_teams', on_delete=models.PROTECT)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        id = str(self.team_id)
        return f"チームID {id}:{self.name}"
