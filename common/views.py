from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import UserForm
# Create your views here.
def signup(request):
    # 요청방법이 POST방식이라면
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # form안의 내용 저장
            form.save()
            # form태그의 username을 가져온다
            username = form.cleaned_data.get('username')
            # form태그의 password1을 가져온다
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # 요청정보와 함께 user정보를 넘김, 자동 로그인 처리과정
            login(request, user)
            # index로 가라(리다이렉트)
            # 'bbsnote:index'로 입력하게 되면 웹 서버의 주소가 '127.0.0.1:8000/bbsnote/'로 표시된다
            return redirect('index')
            # 회원가입이 완료되면 로그인 페이지로 이동
            # return redirect('common:login')
    # POST방식이 아니라면(GET방식) form에 내용없이 출력
    else:
        form = UserForm()
    # request를 받고, 렌더링할 템플릿 파일의 경로를 받고 UserForm객체를 singup템플릿에 전달하여 html로 랜더링
    return render(request, 'common/signup.html', {'form': form})
