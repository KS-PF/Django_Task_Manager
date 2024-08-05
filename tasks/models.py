from django.db import models
from django.core.validators import RegexValidator
from accounts.models import CustomUser
from teams.models import TeamModels


class TasksModel(models.Model):
    task_id = models.AutoField('タスクID',primary_key=True)
    team_id = models.ForeignKey(TeamModels, on_delete=models.CASCADE, related_name = "affiliate_id")
    name = models.CharField('タスク名', max_length=40,null=False, blank=False)
    description = models.TextField('説明', max_length=200,null=False, blank=False)
    start_date = models.DateTimeField('開始', )
    end_date = models.DateTimeField('期日', )

    STATUS_CHOICES = [
        ('未着手', '未着手'),
        ('取組み中', '取組み中'),
        ('完了', '完了'),
    ]

    progress_status = models.CharField(
        '状態',
        max_length=4,
        choices=STATUS_CHOICES,
        default='未着手',
    )

    created_at = models.DateTimeField('作成日',auto_now_add=True)
    updated_at = models.DateTimeField('更新日',auto_now=True)
    manager  = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name = "project_manager")
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name = "project_creater")

    is_delete = models.BooleanField(default=False)

    def __str__(self):
        task_id = str(self.task_id)
        name = self.name
        return f"タスクID{task_id}:{name}"
    
    class Meta:
        db_table = 'Tasks'



class SubTasksModel(models.Model):
    task_id = models.ForeignKey(TasksModel, on_delete=models.CASCADE, related_name = "affiliate_id")
    name = models.CharField('タスク名', max_length=40,null=False, blank=False)
    description = models.TextField('説明', max_length=200,null=False, blank=False)
    start_date = models.DateTimeField('開始', )
    end_date = models.DateTimeField('期日', )
    
    STATUS_CHOICES = [
        ('未着手', '未着手'),
        ('取組み中', '取組み中'),
        ('完了', '完了'),
    ]

    progress_status = models.CharField(
        '状態',
        max_length=4,
        choices=STATUS_CHOICES,
        default='未着手',
    )

    created_at = models.DateTimeField('作成日',auto_now_add=True)
    updated_at = models.DateTimeField('更新日',auto_now=True)
    manager  = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name = "task_manager")
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name = "task_creater")

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'SubTasks'