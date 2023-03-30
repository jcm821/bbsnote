from django import forms
# form .models import Board
from bbsnote.models import Board, Comment

class BoardForm(forms.ModelForm):
    class Meta:
        # model을 DB의 Board로 선언
        model = Board
        fields = ['subject', 'content']
        # # meta 클래스에는 widgets을 제공한다. 이를 통해 부트스트래핑을 적용하여 subject와 content의 레이아웃을 조절할 수 있다
        # 단, 개별적으로 수정해야되는 부분이 복잡하고 불편하므로
        # form.html파일에서 부트스트래핑 옵션을 작성 후 html파일에서 수정하는 방법을 추천한다
        # widgets = {
        #     'subject': forms.TextInput(attrs={'class':'form-control'}),
        #     'content': forms.Textarea(attrs={'class':'form-control', 'rows':10}),
        # }
        # # labels를 통해 컬럼명을 바꿔줄 수 있다
        # labels = {
        #     'subject': '제목',
        #     'content': '내용',
        # }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용'
        }