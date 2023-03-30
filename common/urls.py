from django.contrib.auth import views as auth_views
from django.urls import path
# 현재 디렉토리의 views
from . import views

# 앱의 이름을 'common'으로 정의
app_name = 'common'

urlpatterns = [
    # 'login/'의 경로로 들어온다면, 장고가 제공하는 auth_views.LoginView를 사용하여 로그인 페이지를 표시하고 로그인 처리를 담당
    # 탬플릿 이름은 'common/login.html'에서 가져오며, 이름은 로그인으로 지정한다
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    # 'logout/'의 경로로 들어온다면, 장고가 제공하는 auth_views.LogoutView를 사용하여 로그아웃 페이지를 표시
    # 이름은 로그아웃으로 지정한다 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]