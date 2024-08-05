from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import (
    TaskForm, SubTaskForm, SubTaskUpdataForm, TaskUpdataForm
)
from django.views.generic import (
    TemplateView, ListView, UpdateView, DeleteView, DetailView
)
from django.shortcuts import render, get_object_or_404, redirect
from .models import TasksModel, SubTasksModel
from teams.models import TeamModels
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db.models import Q
from django.http import HttpResponse
import re
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin




class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/index.html'

    def __init__(self):
        self.param = {
            'error':'',
            'tasks':None,
            'subtasks':None,
            'member_teams':None,
        }
    
    def get(self, request):
        id = self.request.user.id

        tasks_data = TasksModel.objects.filter(
            Q(manager = id ),
            ~Q(progress_status = '完了')
        ).order_by('end_date')[:4]


        subtasks_data = SubTasksModel.objects.filter(
            Q(manager = id ),
            ~Q(progress_status = '完了')
        ).order_by('end_date')[:4]


        user = request.user
        member_teams = TeamModels.objects.filter(
            members=user, is_delete=False
        ).order_by('team_id')


        self.param['tasks'] = tasks_data
        self.param['subtasks'] = subtasks_data
        self.param['member_teams'] = member_teams
        return self.render_to_response(self.param)


"""
タスク、サブタスクの追加
はじめ
"""
@login_required
def add(request):
    return render(request, 'tasks/add.html')

class AddTask(LoginRequiredMixin, TemplateView):
    template_name = 'tasks/_forms.html'

    def __init__(self):
        self.param = {
            'error':'',
            'title':'タスク新規作成',
            'back':'tasks:add',
            'urlName':'tasks:add_task',
            'forms':TaskForm,
        }
    
    def get(self, request):
        self.param['forms'] = TaskForm(user=request.user)
        return self.render_to_response(self.param)
    
    def post(self, request):
        form = TaskForm(request.POST, user=request.user)

        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.created_by = request.user
            new_task.save()

            url = reverse('tasks:message', kwargs={'type': 'new_task'})
            return redirect(url)

        self.param['forms'] = TaskForm(request.POST, user=request.user)
        return self.render_to_response(self.param)
    

class AddSubTask(LoginRequiredMixin, TemplateView):
    template_name='tasks/_forms.html'

    def __init__(self):
        self.param = {
            'error':'',
            'title':'サブタスク新規作成',
            'back':'tasks:add',
            'urlName':'tasks:add_subtask',
            'forms':SubTaskForm,
        }
    
    def get(self, request):
        return self.render_to_response(self.param)
    
    def post(self, request):
        form = SubTaskForm(request.POST)

        if form.is_valid():
            new_subtask = form.save(commit=False)
            new_subtask.created_by = request.user
            new_subtask.save()

            url = reverse('tasks:message', kwargs={'type': 'new_subtask'})
            return redirect(url)

        self.param['forms'] = SubTaskForm(request.POST)#前のポスト内容を残す
        return self.render_to_response(self.param)
"""
タスク、サブタスクの追加
(＊＊終わり＊＊)
"""



"""
ガンチャート、進捗度グラフ機能
"""
class ChartsView(LoginRequiredMixin, TemplateView):

    template_name='tasks/charts.html'

    def __init__(self):
        self.param = {
            'error':'',
            'date_range':None,
            'date_range_list':None,
            'gantt_chart_tasks':None,
            'gantt_chart_subtasks':None,
            'barchart':None,
            'barchart_bottom':None,
    }
        
    def get(self, request):
        now = timezone.localtime(timezone.now())
        two_weeks_ago = now - timedelta(weeks=2)
        two_weeks_later = now + timedelta(weeks=2)

        date_range =  f"{two_weeks_ago.year}年{two_weeks_ago.month}月{two_weeks_ago.day}日 〜 \
                        {two_weeks_later.year}年{two_weeks_later.month}月{two_weeks_later.day}日"

        id = self.request.user.id

        tasks_data = TasksModel.objects.filter(
            manager=id,
            start_date__lte=two_weeks_later,
            end_date__gte=two_weeks_ago,
        ).order_by('end_date')


        subtasks_data = SubTasksModel.objects.filter(
            manager=id,
            start_date__lte=two_weeks_later,
            end_date__gte=two_weeks_ago,
        ).order_by('end_date')

        weekdays_japanese = {'Monday':'月', 
                            'Tuesday':'火', 
                            'Wednesday':'水', 
                            'Thursday':'木', 
                            'Friday':'金', 
                            'Saturday':'土', 
                            'Sunday':'日'
                            }

        
        #現在を基準に前後二週間のデータを取得しリストに代入
        date_range_list = []

        for i in range(-14, 15):
            forday = now + timedelta(days=i)
            date_range_list.append([forday.day, weekdays_japanese[forday.strftime('%A')]])

        #タスクのガンチャート用のリストデータを作成
        #0:なし、1:あり、2:ありかつ今日
        gantt_chart_tasks = {}

        for task in tasks_data:
            for_task_flags = []

            for i in range(-14, 15):
                task_flag = 0
                forday = now + timedelta(days=i)
                if task.start_date <= forday and forday <= task.end_date:
                    task_flag = 1
                    if forday.year == now.year and \
                        forday.month == now.month and \
                        forday.day == now.day:
                        task_flag = 2

                for_task_flags.append(task_flag)

            keys = [task.task_id, task.name]
            key_tuple = tuple(keys)
            gantt_chart_tasks[key_tuple]= for_task_flags


        #サブタスクのガンチャート用のリストデータを作成
        #0:なし、1:あり、2:ありかつ今日
        gantt_chart_subtasks = {}

        for subtask in subtasks_data:
            for_subtask_flags = []

            for i in range(-14, 15):
                forday = now + timedelta(days=i)
                subtask_flag = 0
                if subtask.start_date <= forday and forday <= subtask.end_date:
                    subtask_flag = 1
                    if forday.year == now.year and \
                        forday.month == now.month and \
                        forday.day == now.day:
                        subtask_flag = 2

                for_subtask_flags.append(subtask_flag)

            keys = [subtask.id, subtask.name]
            key_tuple = tuple(keys)
            gantt_chart_subtasks[key_tuple] = for_subtask_flags


        #進捗度リストを作成
        barchart_list = {}
        barchart_list_bottom = []
        for i in range(100, 0, -10):
            barchart_list[i] = []

        for task_data in tasks_data:
            if task_data.progress_status == '取組み中':
                task_progress = self.task_progress(task_data.task_id)
                for i in range(100, 0, -10):
                    flag = 0
                    if i <= task_progress:
                        flag = 1
                    barchart_list[i].append(flag)
                task_info = [task_data.task_id, task_data.name]
                barchart_list_bottom.append(task_info)

        #それぞれのデータを代入
        self.param['date_range'] = date_range
        self.param['date_range_list'] = date_range_list
        self.param['gantt_chart_tasks'] = gantt_chart_tasks
        self.param['gantt_chart_subtasks'] = gantt_chart_subtasks
        self.param['barchart'] = barchart_list
        self.param['barchart_bottom'] = barchart_list_bottom
        return self.render_to_response(self.param)
    

    def task_progress(self, task_id):
        task = get_object_or_404(TasksModel, task_id=task_id)

        completed_subtasks_count = SubTasksModel.objects.filter(task_id=task, progress_status='完了').count()
        # print(completed_subtasks_count)

        total_subtasks_count = SubTasksModel.objects.filter(task_id=task).count()
        # print(total_subtasks_count)

        if total_subtasks_count > 0:
            progress_percent = (completed_subtasks_count / total_subtasks_count) * 100
        else:
            progress_percent = 0

        progress_percent_rounded = round(progress_percent)

        return progress_percent_rounded
"""
ガンチャート、進捗度グラフ機能
(＊＊終わり＊＊)
"""


"""
ホワイトボード管理
"""
class WhiteBoardView(LoginRequiredMixin, TemplateView):

    template_name='tasks/whiteboard.html'

    def __init__(self):
        self.param = {
            'error':'',
            'date_range':None,
            'tasks':None,
            'subtasks':None,
    }
        
    def get(self, request):
        now = timezone.localtime(timezone.now())
        two_weeks_ago = now - timedelta(weeks=2)
        two_weeks_later = now + timedelta(weeks=2)

        date_range =  f"{two_weeks_ago.year}年{two_weeks_ago.month}月{two_weeks_ago.day}日 〜 \
                        {two_weeks_later.year}年{two_weeks_later.month}月{two_weeks_later.day}日"

        id = self.request.user.id

        TasksData = TasksModel.objects.filter(
            manager=id,
            start_date__lte=two_weeks_later,
            end_date__gte=two_weeks_ago,
        ).order_by('end_date')

        SubTasksData = SubTasksModel.objects.filter(
            manager=id,
            start_date__lte=two_weeks_later,
            end_date__gte=two_weeks_ago,
        ).order_by('end_date')

        #デバッグ情報をコンソールに出力
        # print(f"Current Time: {now}")
        # for task in SubTasksData:
        #     print(f"Task: {task.name}, Start: {task.start_date}, End: {task.end_date}")

        self.param['date_range'] = date_range
        self.param['tasks'] = TasksData
        self.param['subtasks'] = SubTasksData
        return self.render_to_response(self.param)
        
"""
ホワイトボード管理
(＊＊終わり＊＊)
"""


"""
アップデート
"""
class TasksUpdate(LoginRequiredMixin, UpdateView):
    template_name='tasks/update.html'
    model = TasksModel
    form_class = TaskUpdataForm
    success_url = reverse_lazy('tasks:whiteboard')

class SubTasksUpdate(LoginRequiredMixin, UpdateView):
    template_name='tasks/update.html'
    model = SubTasksModel
    form_class = SubTaskUpdataForm
    success_url = reverse_lazy('tasks:whiteboard')

"""
アップデート
(＊＊終わり＊＊)
"""



"""
使い方
"""
@login_required
def how_use(request):
    return render(request, 'tasks/how_use.html')
"""
使い方
(＊＊終わり＊＊)
"""


"""
メッセージの表示
"""
@login_required
def message(request, type):
    title = 'もう一度やり直してください'
    text = ''
    label = 'ログインする'
    name = 'accounts:login'

    if type == 'signup':
        title = '登録が完了しました'
        text = 'ユーザーの新規登録が完了しました。以下のボタンからログインしてください。'
    elif type == 'new_task':
        title = '登録が完了しました'
        text = 'タスクの新規登録が完了しました。以下のボタンから戻ってください。'
        label = '戻る'
        name = 'tasks:add'
    elif type == 'new_subtask':
        title = '登録が完了しました'
        text = 'サブタスクの新規登録が完了しました。以下のボタンから戻ってください。'
        label = '戻る'
        name = 'tasks:add'
    elif type == 'permission_error':
        title = '編集権限がありません'
        text = 'もう一度やり直してください'
        label = 'ホームに戻る'
        name = 'tasks:index'

    view_url = reverse(name)
    context ={
        "title":title,
        "text":text,
        "label":label,
        "url": view_url,
        }
    return render(request, 'tasks/message.html', context )
"""
メッセージの表示
(＊＊終わり＊＊)
"""