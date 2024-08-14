from django.urls import reverse_lazy
from django.views.generic import (TemplateView)
from django.shortcuts import render, get_object_or_404, redirect
from tasks.models import TasksModel, SubTasksModel
from teams.models import TeamModels
from django.utils import timezone
from django.utils.timezone import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q



class ShareTasksView(LoginRequiredMixin, TemplateView):

    template_name='share/task_list.html'

    def __init__(self):
        self.param = {
            'error':'',
            'date_range':None,
            'teams':None,
            'team_form':None,
            'select_form':None,
            'tasks':[],
            'subtasks':[],
    }
    

    def get(self, request):
        user = self.request.user

        member_teams = TeamModels.objects.filter(members=user, is_delete=False)
        
        # 各チームのメンバー情報を取得
        teams_with_members = []
        for team in member_teams:
            members = team.members.all()
            teams_with_members.append({
                'team': team,
                'members': members
            })

        now = timezone.localtime(timezone.now())
        two_weeks_ago = now - timedelta(weeks=2)
        two_weeks_later = now + timedelta(weeks=2)

        date_range =  f"{two_weeks_ago.year}年{two_weeks_ago.month}月{two_weeks_ago.day}日 〜 \
                        {two_weeks_later.year}年{two_weeks_later.month}月{two_weeks_later.day}日"
        
        for team in member_teams:
            # タスクのフィルタリング
            TasksData = TasksModel.objects.filter(
                Q(team_id=int(team.team_id)) &
                Q(start_date__lte=two_weeks_later) &
                Q(end_date__gte=two_weeks_ago) &
                ~Q(manager=user) &
                ~Q(progress_status='完了')
            ).order_by('end_date')

            self.param['tasks'].extend(TasksData)

            # サブタスクのフィルタリング
            SubTasksData = SubTasksModel.objects.filter(
                Q(task_id__team_id=int(team.team_id)) &
                Q(start_date__lte=two_weeks_later) &
                Q(end_date__gte=two_weeks_ago) &
                ~Q(manager=user) &
                ~Q(progress_status='完了') &
                ~Q(task_id__progress_status='完了') 
            ).order_by('end_date')

            self.param['subtasks'].extend(SubTasksData)


        self.param['date_range'] = date_range
        self.param['teams_with_members'] = teams_with_members
        return self.render_to_response(self.param)