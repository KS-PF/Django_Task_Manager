from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'accounts'
urlpatterns = [
    path('login/',
        LoginView.as_view(
            redirect_authenticated_user=True,
            template_name='registration/login.html'
        ),
        name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("mypage/",login_required(views.user_page), name="mypage"),
]
