from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'tasks'
urlpatterns = [
    path('', login_required(views.IndexView.as_view()), name='index'),

    path('charts/', login_required(views.ChartsView.as_view()), name='charts'),
    path('whiteboard/', login_required(views.WhiteBoardView.as_view()), name='whiteboard'),

    path('tasks/<int:pk>/update/', login_required(views.TasksUpdate.as_view()), name='task_update'),
    path('subtasks/<int:pk>/update/', login_required(views.SubTasksUpdate.as_view()), name='subtask_update'),

    path('add/', login_required(views.add), name='add'),
    path('add/task/', login_required(views.AddTask.as_view()), name='add_task'),
    path('add/subtask/', login_required(views.AddSubTask.as_view()), name='add_subtask'),

    path('tasks/<int:id>/delete/', login_required(views.delete_task), name='delete_task'),
    path('subtasks/<int:id>/delete/', login_required(views.delete_subtask), name='delete_subtask'),

    path("use/",views.how_use, name="how_use"),
    path('message/<str:type>/', views.message, name='message'),
]
