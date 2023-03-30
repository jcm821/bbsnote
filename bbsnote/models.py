from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# 게시글 모델
class Board(models.Model):
    # subject를 문자열 필드로 선언, 최대길이 200자
    subject = models.CharField(max_length=200)
    # content를 텍스트 필드로 선언
    content = models.TextField()
    # 작성자필드 선언, User를 참조하는 외래키이고, User객체가 삭제되면 같이 삭제되도록 설정
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 객체(게시글)가 처음 생성될때 자동으로 작성시간 설정
    create_date = models.DateTimeField(auto_now_add=True)
    # 객체(게시글)를 수정할 때마다 자동으로 시간 갱신, blank=True옵션을 통해 수정날짜에 빈값을 할당할 수도 있다
    update_date = models.DateTimeField(auto_now=True)

    # 객체가 문자열로 표현될 때 호출
    # 게시판에 글의 제목이 목록에 나오도록 설정
    def __str__(self):
        # [id] subject 형식으로 출력
        # id와 subject는 각각 객체의 id와 subject 속성값
        return f'[{self.id}] {self.subject}'

# 댓글 모델
class Comment(models.Model):
    # board를 외래키로 정의 on_delete=models.CASCADE는 Board객체가 삭제되면 Comment객체도 같이 삭제되도록 지정
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    # blank=True는 이 항목은 Null을 허용한다는 의미이다
    content = models.TextField()
    # 위의 게시글 모델과 동일하게 작성해준다
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # 좋아요 필드 생성, 비어있는 값을 허용하며 디폴트값으로 0
    # models에서 null옵션을 통해 필드값이 null/not null 허용유무 선택
    # 값을 ''와 같이 null이 아닌값으로 채우고자 할때 blank옵션을 사용(null입력을 방지하기 위함)
    # 즉, 빈 값을 허용하는 경우, default 값을 ""로, 즉 빈 문자열로 설정한다고 이해하면 될 듯 하다
    # like = models.IntegerField(blank=True, default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    # 댓글을 내림차순(최신순)으로 정렬
    class Meta:
        ordering = ['-create_date']

    def __str__(self):
        # 게시글의 번호와 그 게시글의 댓글임을 명시
        # 원하는 항목을 불러와서 커스터마이징 가능
        return f'[ {self.board.id}: {self.board.subject}] {self.content}'