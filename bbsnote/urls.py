from django.urls import path
# 현재 디렉토리의 views 모듈을 불러옴
from . import views

# 앱의 이름을 'bbsnote'로 선언, 이 이름은 URL 패턴의 네임스페이스로 사용
app_name = 'bbsnote'

urlpatterns = [
    # 첫번째 URL패턴이 빈 문자열과 매칭 후, views.index 뷰 함수와 매칭
    path('', views.index, name='index'),
    # 두번째 URL패턴이 정수가 들어갈거고, board_id와 매칭하며, 이후 views.detail 뷰 함수와 매칭
    path('<int:board_id>/', views.detail, name='detail'),
    # 세번째 URL패턴이 'comment/create/'문자열 다음에 정수형 변수인 board_id와 매칭
    # 이후 views.comment_create 뷰 함수 매칭하여 호출
    path('comment/create/<int:board_id>/', views.comment_create, name='comment_create'),
    # 'board/create/'경로에 들어오면 뷰 함수 board_create와 매칭하여 호출
    path('board/create/', views.board_create, name='board_create'),
    # 수정을 위한 url매핑
    path('board/modify/<int:board_id>/', views.board_modify, name='board_modify'),
    # 삭제를 위한 url매핑
    path('board/delete/<int:board_id>/', views.board_delete, name='board_delete'),
    # 댓글 수정을 위한 url매핑
    path('comment/modify/<int:comment_id>/', views.comment_modify, name='comment_modify'),
    # 댓글 삭제를 위한 url매핑
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
]