from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'share'
urlpatterns = [
    path("",login_required(views.ShareTasksView.as_view()), name="share_tasks"),
]
