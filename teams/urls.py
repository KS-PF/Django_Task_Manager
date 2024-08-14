from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'teams'
urlpatterns = [
    path('', login_required(views.TeamListView.as_view()), name='team_list'),
    path('create/', login_required(views.CreateTeam.as_view()), name='team_create'),
    path('<int:pk>/edit/', views.team_edit, name='team_edit'),
    path('<int:id>/delete/', login_required(views.delete_team), name='delete_team'),

    path('message/<str:type>/', views.message, name='message'),
]
