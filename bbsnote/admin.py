from django.contrib import admin
# 현재 디렉토리의 models.py에서 Board모델 가져오기
# *은 models에 존재하는 모든 모듈 호출
from .models import *
# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    # 관리자 페이지에서 검색을 진행시 제목(subject)과 내용(content)으로 검색 가능
    search_fields = ['subject', 'content']

# 관리자 페이지에 Board, BoardAdmin모델을 등록하고, 모델들을 위의 클래스로 정의된 방식으로 표시
admin.site.register(Board, BoardAdmin)
admin.site.register(Comment)

