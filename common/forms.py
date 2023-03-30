from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# UserForm클래스 선언
class UserForm(UserCreationForm):
    # 이메일 필드를 추가하고 라벨의 이름을 이메일로 선언, email객체에 저장, 선택값으로 정의된다
    # Meta클래스 위에 필드를 선언하면 필수값으로 받겓다고 정의하는 것이다.
    email = forms.EmailField(label="이메일")
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')