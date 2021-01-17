from django.conf.urls import url
from .views import RegistUser, AppLogin

# ~/login/regist_user       => ~/root 경로 / 프로젝트 경로
urlpatterns = [
    url('register_user', RegistUser.as_view(), name='register_user'),
    url('app_login', AppLogin.as_view(), name='app_login'),
]
